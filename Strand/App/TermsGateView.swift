import SwiftUI
import StrandDesign

/// First-run acknowledgment gate (clickwrap). Shown over EVERYTHING — before onboarding, pairing, or
/// any Bluetooth access — until the current `Terms.currentVersion` is accepted, and again if the
/// terms materially change. The user must tick the (un-pre-checked) box and tap Accept; the accepted
/// version is then stored locally, the on-device equivalent of a consent record. See `Terms` / `TERMS.md`.
struct TermsGateView: View {
    let onAccept: () -> Void
    /// One flag per `Terms.attestations` entry; every one must be ticked before Accept enables.
    @State private var checks: [Bool] = Array(repeating: false, count: Terms.attestations.count)
    @State private var showingPreview = false

    private var allChecked: Bool { checks.allSatisfy { $0 } }

    var body: some View {
        ZStack {
            StrandPalette.surfaceBase.ignoresSafeArea()

            VStack(spacing: 0) {
                VStack(spacing: 6) {
                    Text("Before you use NOOP")
                        .font(StrandFont.title1)
                        .foregroundStyle(StrandPalette.textPrimary)
                    Text("Please read the points below, then confirm each statement.")
                        .font(StrandFont.subhead)
                        .foregroundStyle(StrandPalette.textSecondary)
                        .multilineTextAlignment(.center)
                }
                .padding(.top, 36)
                .padding(.bottom, 22)

                ScrollView {
                    VStack(alignment: .leading, spacing: 18) {
                        ForEach(Terms.points, id: \.0) { point in
                            VStack(alignment: .leading, spacing: 4) {
                                Text(point.0)
                                    .font(StrandFont.headline)
                                    .foregroundStyle(StrandPalette.textPrimary)
                                Text(point.1)
                                    .font(StrandFont.footnote)
                                    .foregroundStyle(StrandPalette.textSecondary)
                                    .fixedSize(horizontal: false, vertical: true)
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                        }

                        Rectangle()
                            .fill(StrandPalette.hairline)
                            .frame(height: 1)
                            .padding(.vertical, 2)

                        Text("Please confirm each of these:")
                            .font(StrandFont.subhead)
                            .foregroundStyle(StrandPalette.textSecondary)

                        ForEach(Array(Terms.attestations.enumerated()), id: \.offset) { idx, line in
                            Toggle(isOn: Binding(get: { checks[idx] }, set: { checks[idx] = $0 })) {
                                Text(line)
                                    .font(StrandFont.footnote)
                                    .foregroundStyle(StrandPalette.textPrimary)
                                    .fixedSize(horizontal: false, vertical: true)
                            }
                            #if os(macOS)
                            .toggleStyle(.checkbox)   // iOS falls back to the default switch toggle
                            #endif
                        }

                        Text("The full terms are in TERMS.md, shipped with NOOP. This is not legal advice.")
                            .font(StrandFont.footnote)
                            .foregroundStyle(StrandPalette.textTertiary)
                            .padding(.top, 2)
                    }
                    .padding(.horizontal, 30)
                    .padding(.bottom, 18)
                }
                #if os(iOS)
                // #697/#horizontal-swipe parity, see ScreenScaffold. Shown before onboarding/pairing,
                // on top of everything, so this is the very first screen a new install sees.
                .scrollBounceBehavior(.basedOnSize, axes: .horizontal)
                #endif

                Rectangle()
                    .fill(StrandPalette.hairline)
                    .frame(height: 1)

                if ProjectInfo.isTestFlightDistribution {
                    Button("Preview with sample data") { showingPreview = true }
                        .buttonStyle(.bordered)
                        .padding(.top, 16)
                        .accessibilityHint("Explore a read-only sample without connecting a sensor or accepting the terms.")
                }

                Button(action: onAccept) {
                    Text("Accept & Continue")
                        .font(StrandFont.headline)
                        .frame(maxWidth: .infinity)
                        .padding(.vertical, 9)
                }
                .buttonStyle(.borderedProminent)
                .tint(StrandPalette.accent)
                .disabled(!allChecked)
                .keyboardShortcut(.defaultAction)
                .padding(26)
            }
            .frame(maxWidth: 560, maxHeight: 720)
        }
        .sheet(isPresented: $showingPreview) { TestFlightPreviewView() }
    }
}

/// A read-only, synthetic preview for new users and beta reviewers. It holds no repository,
/// never seeds the personal database, and cannot pair, import, export, or contact a provider.
private struct TestFlightPreviewView: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    Label("Sample data", systemImage: "sparkles")
                        .font(.headline).foregroundStyle(StrandPalette.accent)
                    Text("Your day, on your device")
                        .font(.largeTitle.bold())
                    Text("A preview of the readings and independent wellness estimates NOOP can organize. These values are fictional and are never saved to your library.")
                        .foregroundStyle(.secondary)
                    LazyVGrid(columns: [GridItem(.adaptive(minimum: 140), spacing: 14)], spacing: 14) {
                        sampleCard("Readiness", value: "78%", symbol: "heart.circle", detail: "Independent estimate")
                        sampleCard("Sleep", value: "7h 42m", symbol: "moon.zzz", detail: "Sample night")
                        sampleCard("Resting heart rate", value: "54 bpm", symbol: "waveform.path.ecg", detail: "Sample reading")
                        sampleCard("Heart rate variability", value: "68 ms", symbol: "heart.text.square", detail: "Sample RMSSD")
                    }
                    VStack(alignment: .leading, spacing: 12) {
                        Label("Explore your trends", systemImage: "chart.xyaxis.line")
                        Text("Review sleep, workouts, heart rate, and trends in the native app. Import your own exports, keep a local journal, and back up your library to a folder you choose.")
                            .foregroundStyle(.secondary)
                        Divider()
                        Label("Connect your own sensor", systemImage: "sensor.tag.radiowaves.forward")
                        Text("Close this preview, read the terms, then follow setup to pair your strap. WHOOP 4.0 is the established upstream path. WHOOP 5.0/MG support remains experimental and firmware-dependent.")
                            .foregroundStyle(.secondary)
                        Text("NOOP is independent of WHOOP. Estimates are for general wellness and are not medical measurements or WHOOP's proprietary scores.")
                            .font(.footnote).foregroundStyle(.secondary)
                    }
                    .padding(18)
                    .background(.quaternary, in: RoundedRectangle(cornerRadius: 18))
                    Link("Privacy and source", destination: ProjectInfo.privacyPolicy)
                }
                .padding(24)
                .frame(maxWidth: 720, alignment: .leading)
                .frame(maxWidth: .infinity)
            }
            .navigationTitle("NOOP Preview")
            .toolbar {
                ToolbarItem(placement: .confirmationAction) {
                    Button("Done") { dismiss() }
                }
            }
        }
        #if os(macOS)
        .frame(minWidth: 520, idealWidth: 640, minHeight: 560, idealHeight: 680)
        #endif
    }

    private func sampleCard(_ title: String, value: String, symbol: String, detail: String) -> some View {
        VStack(alignment: .leading, spacing: 10) {
            Image(systemName: symbol).font(.title2).foregroundStyle(StrandPalette.accent)
            Text(value).font(.title.bold()).minimumScaleFactor(0.7).lineLimit(1)
            Text(title).font(.headline)
            Text(detail).font(.caption).foregroundStyle(.secondary)
        }
        .frame(maxWidth: .infinity, minHeight: 150, alignment: .leading)
        .padding(16)
        .background(.quaternary, in: RoundedRectangle(cornerRadius: 18))
        .accessibilityElement(children: .combine)
    }
}
