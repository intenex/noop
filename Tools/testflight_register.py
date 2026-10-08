#!/usr/bin/env python3
"""Manually register this fork's Apple identifiers and existing capabilities."""
import json
from pathlib import Path
from testflight_api import collection, request

TARGETS = {
    "com.benyu.noop": ("NOOP TestFlight", "UNIVERSAL", ["HEALTHKIT", "APP_GROUPS"]),
    "com.benyu.noop.widgets": ("NOOP TestFlight Widgets", "IOS", ["APP_GROUPS"]),
    "com.benyu.noop.watch": ("NOOP TestFlight Watch", "IOS", ["HEALTHKIT", "APP_GROUPS"]),
    "com.benyu.noop.watch.complications": ("NOOP TestFlight Complications", "IOS", ["APP_GROUPS"]),
}


def main():
    result = {}
    for identifier, (name, platform, capabilities) in TARGETS.items():
        found = [row for row in collection(f"bundleIds?filter[identifier]={identifier}&limit=100")
                 if row["attributes"]["identifier"] == identifier]
        if len(found) > 1:
            raise RuntimeError(f"Ambiguous identifier: {identifier}")
        row = found[0] if found else request("bundleIds", "POST", {"data": {
            "type": "bundleIds", "attributes": {
                "identifier": identifier, "name": name, "platform": platform}}})["data"]
        bid = row["id"]
        current = {c["attributes"]["capabilityType"] for c in collection(
            f"bundleIds/{bid}/bundleIdCapabilities")}
        for capability in capabilities:
            if capability not in current:
                request("bundleIdCapabilities", "POST", {"data": {
                    "type": "bundleIdCapabilities", "attributes": {"capabilityType": capability},
                    "relationships": {"bundleId": {"data": {"type": "bundleIds", "id": bid}}}}})
        result[identifier] = bid
        print(identifier, bid, "registered", flush=True)
    destination = Path("build/release/bundle-ids.json")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
