# NOOP native TestFlight edition

This is the free, noncommercial distribution fork at [intenex/noop](https://github.com/intenex/noop),
based on [ryanbr/noop](https://github.com/ryanbr/noop). Copyright, required notices, the PolyForm
Noncommercial license, and upstream acknowledgements are preserved in the repository and both apps.

App Store Connect listing: **NOOP: Sensor Companion**, app **6820716969**.
Both native platforms share **com.benyu.noop**, version **12.0.0 (436)**.
The iPhone app supports iOS 17 and later and includes iPad layouts, widgets, and the watch companion.
The native Mac app supports macOS 13 and later on Apple Silicon and Intel.

## Installing and starting

Install Apple's TestFlight app, accept an invitation or use the public beta link once Apple's
external review has approved a build, and install NOOP. Updates arrive through TestFlight;
each uploaded beta expires after 90 days. No weekly sideload signing is needed.

On the first screen, **Preview with sample data** opens a read-only synthetic preview without
an account or sensor. Sample values are never saved in the personal library. To use a real sensor,
read and accept the terms, follow setup, grant Bluetooth permission, and pair a strap you own.
Keep the official WHOOP app from competing for the Bluetooth connection while testing.
The [upstream iPhone guide](IOS.md) and [project README](../README.md) have device and import details.

WHOOP 4.0 is the established upstream path. WHOOP 5.0/MG support is experimental, incomplete,
and firmware-dependent. This distribution has no physical-strap acceptance evidence yet. It is
independent of WHOOP, and its wellness estimates are not proprietary WHOOP scores or medical measurements.

The app stores data locally and provides optional, user-controlled imports, exports, backups,
and provider integrations. No provider credentials or developer data server are supplied.
See the [privacy policy](TESTFLIGHT-PRIVACY.md) and [icon details](TESTFLIGHT-ICON.md).
The [third-party notices](THIRD-PARTY-NOTICES.md) are included in the TestFlight beta license agreement.

## Manual release procedure

`project.yml` is authoritative. Update the build number there and in the release verifier before
a new upload, regenerate with XcodeGen, and run the package and native test suites in `docs/BUILD.md`.
Use local archives rather than activating the fork's GitHub Actions workflows.

Archive `NOOPiOS` for generic iOS and `Strand` for generic macOS in Release using the configured
team and Xcode account. Both Mac architectures must be included. Export with `app-store-connect`,
`testFlightInternalTestingOnly=false`, and `manageAppVersionAndBuildNumber=false`.
If automatic export cannot use the account, use existing local Apple Distribution and Mac Installer
identities plus app-store provisioning profiles for the root app, widgets, watch, and complications.
Keep all signing keys, provisioning payloads, tester addresses, archives, and live API state outside Git.

Run `Tools/testflight_verify.py` against each archive and then the exported app bundles using
`--distribution`. Check the signed nested targets, HealthKit, App Group, orientations, privacy
manifests, required notices, icon, and universal Mac binary before uploading. Upload the preserved
IPA and signed installer package with Apple's tools. Network retries reuse these exact artifacts.

After upload, query App Store Connect until both builds are VALID. Configure `NOOP Internal` and
`NOOP External`, localized testing notes, beta review details, and the license agreement. Attach the
exact builds, invite authorized internal testers, submit external beta review, and verify the
tester-facing state. Upload, processing, internal availability, external approval, and installation
are separate gates; report each honestly.

`Tools/testflight_api.py` and `Tools/testflight_register.py` provide bounded, manual official-Apple
API access using Python 3 with `cryptography`. The API key stays in the user's private key directory and tokens are never printed.
These helpers do not run on a schedule or enable paid services.

## Hosted-job budget

The release is built, tested, signed, and uploaded locally. No hosted CI, deployment, AI, or recurring
job has been enabled by this edition. Added monthly hosted usage is **0**. The upstream workflow
files remain intact. After pushing the release source, GitHub registered 11 inherited workflows,
with zero runs, artifacts, and cache usage. No workflow was dispatched or enabled manually.
Do not enable premium runners,
schedules, external integrations, or paid overages without applying the hosted-job cost safety policy.

## Release evidence

Verified October 8, 2026. Both uploaded builds are **VALID** and **IN_BETA_TESTING** internally.
Both external submissions are **WAITING_FOR_BETA_REVIEW**. Public beta availability remains pending
Apple's approval; uploading and enabling a public link do not bypass beta review.

| Platform | Version / build | Internal availability | External availability | Installation evidence |
| --- | --- | --- | --- | --- |
| iOS / iPadOS | 12.0.0 / 436 | In beta testing | Waiting for beta review | Simulator build and first screen inspected; physical iPhone installation pending |
| Native macOS | 12.0.0 / 436 | In beta testing | Waiting for beta review | Installed through TestFlight on Apple Silicon; receipt, version, launch, and sample preview verified |

The external group is configured for both native builds with a 10,000-person public-link limit:
[NOOP public beta](https://testflight.apple.com/join/jwhWhweh). **This link is pending review and must
not be announced as publicly available yet.** The iOS build is not offered as a substitute for the
native Mac app or as an Apple Vision app.
The public landing page was inspected through computer use and displayed
"This beta isn't accepting any new testers right now," consistent with the pending review states.

Authorized internal invitations were verified in App Store Connect. A WhatsApp reply to the requested
recipient in the requested group was sent through computer use; it stated that the internal builds
were published, the invitation was ready, and the public beta was still awaiting Apple review.
Tester addresses, invitation links, and private chat content are not committed to this repository.

Eight package suites plus the native Mac suite executed **6,617 tests, four skipped, zero failures**.
The iOS simulator build succeeded. Signed archives and exported app bundles passed the release
verifier, including both Mac architectures, nested iOS targets, privacy manifests, required notices,
icon format, HealthKit, App Group, and iPad orientations. No live sensor pairing, physical iPhone
acceptance, or physical Intel Mac test has been performed.

Uploaded artifact SHA-256 values:

- iOS IPA: `ae36cd552023296e7fbf7779bf7ee29050d140d7abaeefcbfb41c1ac26bd825b`
- macOS installer: `887d991b881002b970b77ecfc6c3b0064100b5819e5c5ebccdac1a13a0b7dead`

Preserved archives, signed exports, test reports, signature/resource checks, and private API snapshots
are under ignored `build/release/`. Continue external approval verification using the existing
manual helper and exact uploaded build IDs; do not regenerate or upload a replacement merely to poll.
