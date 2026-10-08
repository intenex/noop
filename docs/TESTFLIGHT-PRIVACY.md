# NOOP TestFlight edition privacy policy

Updated October 8, 2026. Distributor and feedback contact: Benjamin Yu, yu@benyu.org.

This free, noncommercial TestFlight edition is a distribution fork of
[ryanbr/noop](https://github.com/ryanbr/noop). It is independent of WHOOP.

## Local fitness data

Bluetooth readings, imported history, workouts, journal entries, and computed wellness estimates
are stored on the user's device. NOOP has no developer-operated data server, account system,
advertising, analytics SDK, or automatic developer collection of fitness data. No cloud destination
is configured by default. Users can export, back up, or delete their own local data in the app.
If a user selects a folder managed by iCloud Drive, Dropbox, or another sync provider for an export
or backup, that provider can upload the files under the user's account and its own privacy terms.
Uninstalling can remove local data; export a backup before uninstalling.

Bluetooth access is used to communicate with a sensor the user owns. Optional location and motion
access record workout routes and steps locally. Optional Apple Health permissions allow the user
to import selected data or enable writeback; permissions can be revoked in Apple's Health settings.
Microphone and speech access are optional for on-device question transcription. No audio is sent
to a developer server.

## Optional services

The AI Coach needs the user's own provider configuration and explicit consent. When enabled, its
configured provider receives the question and the metric context selected for that request. Cloud
providers apply their own privacy and billing terms; a local compatible model can keep requests
on the user's machine or local network. No API key or paid provider is supplied with this build.
Experimental one-way exports send data only to an endpoint the user explicitly configures.
Optional Oura cloud access uses the user's own credentials and Oura's service; no Oura OAuth
credentials are bundled with this edition. See the upstream
[privacy and security documentation](PRIVACY_SECURITY.md) for feature-level details.

## TestFlight and feedback

Apple distributes and updates this beta through TestFlight. Apple may collect beta usage and crash
information and shares TestFlight feedback with the distributor under its
[TestFlight privacy terms](https://www.apple.com/legal/privacy/data/en/test-flight/).
When users deliberately send feedback, an email, or a diagnostic export, the distributor receives
what they choose to include. Diagnostic exports can contain sensitive sensor information; review
them before sharing. Feedback is used to investigate the reported issue, is not sold or used for
advertising, and can be requested for deletion by contacting the address above. Public GitHub
issues are public; do not post personal health data or secrets there.

## Rights and limitations

Contact yu@benyu.org with privacy questions or deletion requests concerning submitted feedback.
The app's scores and inferred measurements are independent, experimental wellness estimates,
not WHOOP's proprietary scores or medical measurements. WHOOP 4.0 is the upstream-supported
path; WHOOP 5.0/MG support remains incomplete and firmware-dependent.
