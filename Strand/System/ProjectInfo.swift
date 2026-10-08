import Foundation

/// Project identity and attribution for the noncommercial TestFlight edition.
enum ProjectInfo {
    static let appName = "NOOP"
    static let tagline = "Your strap. Your data. Your machine. Local-first, no cloud."
    static let version = "0.1.0"
    /// Distribution identity for this noncommercial TestFlight fork.
    static var isTestFlightDistribution: Bool {
        Bundle.main.object(forInfoDictionaryKey: "NOOPDistribution") as? String == "TestFlight"
    }
    static let distributionSource = URL(string: "https://github.com/intenex/noop")!
    static let upstreamSource = URL(string: "https://github.com/ryanbr/noop")!
    static let privacyPolicy = URL(string: "https://github.com/intenex/noop/blob/main/docs/TESTFLIGHT-PRIVACY.md")!
    /// Feedback on this distribution goes to its distributor.
    static let contactEmail = "yu@benyu.org"

    /// Open-source reverse-engineering this is built on.
    static let attributions: [(repo: String, note: String)] = [
        ("johnmiddleton12/my-whoop", "WHOOP 4.0 BLE protocol"),
        ("b-nnett/goose", "WHOOP 5.0 BLE protocol"),
    ]
}
