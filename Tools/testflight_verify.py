#!/usr/bin/env python3
"""Inspect native NOOP archives or exported .app bundles before a manual upload."""
import argparse
import datetime
import json
import plistlib
import subprocess
from pathlib import Path

TEAM = "Z6FHNWFTWR"
BUNDLE = "com.benyu.noop"
GROUP = "group.com.benyu.noop"
VERSION = "12.0.0"
BUILD = "436"


def run(*args):
    return subprocess.check_output(args, stderr=subprocess.STDOUT)


def plist_output(*args):
    output = run(*args)
    start = output.find(b"<?xml")
    if start < 0:
        raise ValueError("Expected a property list from " + args[0])
    return plistlib.loads(output[start:])


def verify(path, platform, distribution):
    if path.suffix == ".xcarchive":
        path = path / "Products/Applications/NOOP.app"
    if not path.is_dir():
        raise ValueError(f"Missing app: {path}")
    bundles = [path] + sorted(p for p in path.rglob("*") if p.suffix in (".app", ".appex"))
    results = []
    for bundle in bundles:
        mac = (bundle / "Contents/Info.plist").exists()
        info_path = bundle / ("Contents/Info.plist" if mac else "Info.plist")
        info = plistlib.loads(info_path.read_bytes())
        identifier = info["CFBundleIdentifier"]
        if identifier != BUNDLE and not identifier.startswith(BUNDLE + "."):
            raise ValueError(f"Unexpected nested app identifier: {identifier}")
        assert info["CFBundleShortVersionString"] == VERSION, identifier + " version mismatch"
        assert info["CFBundleVersion"] == BUILD, identifier + " build mismatch"
        run("codesign", "--verify", "--strict", "--deep", str(bundle))
        identity = run("codesign", "-dv", "--verbose=4", str(bundle)).decode()
        assert "Identifier=" + identifier + "\n" in identity, identifier + " code signature identifier mismatch"
        assert "TeamIdentifier=" + TEAM + "\n" in identity, identifier + " code signature team mismatch"
        ent = plist_output("codesign", "-d", "--entitlements", ":-", str(bundle))
        signed_id = ent.get("application-identifier", ent.get("com.apple.application-identifier"))
        if not mac or signed_id is not None:
            assert signed_id == TEAM + "." + identifier, identifier + " entitlement identity mismatch"
        if not mac or "com.apple.developer.team-identifier" in ent:
            assert ent.get("com.apple.developer.team-identifier") == TEAM, identifier + " entitlement team mismatch"
        assert not ent.get("com.apple.developer.icloud-container-identifiers"), "Unexpected iCloud entitlement"
        resources = bundle / ("Contents/Resources" if mac else "")
        manifest = plistlib.loads((resources / "PrivacyInfo.xcprivacy").read_bytes())
        assert manifest["NSPrivacyTracking"] is False
        assert manifest["NSPrivacyCollectedDataTypes"] == []
        profile_path = bundle / ("Contents/embedded.provisionprofile" if mac else "embedded.mobileprovision")
        # A sandboxed Mac app with only unrestricted sandbox entitlements need not embed a profile.
        # Its distribution certificate, cryptographic signature, identifier, and team are still checked.
        profile = plist_output("security", "cms", "-D", "-i", str(profile_path)) if profile_path.exists() else None
        if profile:
            assert TEAM in profile["TeamIdentifier"], identifier + " profile team mismatch"
            assert profile["ExpirationDate"] > datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None)
        else:
            assert mac, identifier + " provisioning profile missing"
            assert not ent.get("com.apple.security.application-groups"), "Mac App Group requires a profile"
        if not mac:
            assert GROUP in ent.get("com.apple.security.application-groups", []), identifier + " app group missing"
            assert GROUP in profile["Entitlements"].get("com.apple.security.application-groups", [])
        if distribution:
            assert not ent.get("get-task-allow", ent.get("com.apple.security.get-task-allow", False)), "Debug entitlement"
            if profile:
                assert not profile.get("ProvisionedDevices"), "Device-limited profile"
                assert not profile.get("ProvisionsAllDevices", False), "Enterprise profile"
            assert "Authority=Apple Distribution:" in identity or "Authority=3rd Party Mac Developer Application:" in identity
        if bundle == path:
            assert info["NOOPDistribution"] == "TestFlight"
            assert info["ITSAppUsesNonExemptEncryption"] is False
            for notice in ("LICENSE", "NOTICE", "ATTRIBUTION.md", "DISCLAIMER.md", "TERMS.md"):
                assert (resources / notice).stat().st_size > 0, "Missing required notice: " + notice
            assert info.get("OURA_CLIENT_ID", "") == "", "Bundled Oura credential"
            assert info.get("OURA_CLIENT_SECRET", "") == "", "Bundled Oura credential"
            if platform == "macOS":
                assert ent.get("com.apple.security.app-sandbox") is True
                assert ent.get("com.apple.security.device.bluetooth") is True
                assert ent.get("com.apple.security.files.user-selected.read-write") is True
                executable = bundle / "Contents/MacOS" / info["CFBundleExecutable"]
                archs = run("lipo", "-archs", str(executable)).decode().split()
                assert set(archs) == {"arm64", "x86_64"}, "macOS universal architectures missing"
            else:
                assert ent.get("com.apple.developer.healthkit") is True
                assert ent.get("com.apple.developer.healthkit.background-delivery") is True
                for purpose in ("NSBluetoothAlwaysUsageDescription", "NSHealthShareUsageDescription", "NSHealthUpdateUsageDescription"):
                    assert info.get(purpose), "Missing privacy purpose: " + purpose
                assert set(info["UISupportedInterfaceOrientations~ipad"]) == {
                    "UIInterfaceOrientationPortrait", "UIInterfaceOrientationPortraitUpsideDown",
                    "UIInterfaceOrientationLandscapeLeft", "UIInterfaceOrientationLandscapeRight"}
                assert info["CFBundleIcons"]["CFBundlePrimaryIcon"].get("CFBundleIconFiles"), "Missing compiled icon"
        results.append({"bundleId": identifier, "version": VERSION, "build": BUILD,
                        "profile": profile["Name"] if profile else None, "distribution": distribution})
    if platform == "iOS":
        assert {r["bundleId"] for r in results} == {
            BUNDLE, BUNDLE + ".widgets", BUNDLE + ".watch", BUNDLE + ".watch.complications"}
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--platform", required=True, choices=["iOS", "macOS"])
    parser.add_argument("--distribution", action="store_true")
    args = parser.parse_args()
    print(json.dumps(verify(args.path, args.platform, args.distribution), indent=2))
