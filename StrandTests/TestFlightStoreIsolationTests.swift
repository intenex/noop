import Foundation
import XCTest
@testable import Strand

final class TestFlightStoreIsolationTests: XCTestCase {
    #if os(macOS)
    private let home = URL(fileURLWithPath: "/Users/noop-isolation-fixture", isDirectory: true)

    func testTestFlightPinsItsOwnContainerEvenBeforeSandboxResolution() {
        let appSupport = home.appendingPathComponent("Library/Application Support")
        let result = StorePaths.macOSProductionContainerAppSupport(
            defaultingTo: appSupport, bundleIdentifier: "com.benyu.noop",
            isTestFlightDistribution: true, homeDirectory: home)
        XCTAssertEqual(result.path,
            "/Users/noop-isolation-fixture/Library/Containers/com.benyu.noop/Data/Library/Application Support")
        XCTAssertNotEqual(result, appSupport)
        XCTAssertFalse(result.path.contains("com.noopapp.noop"))
    }

    func testAlreadySandboxedPathIsNotNestedAgain() {
        let container = home.appendingPathComponent("Library/Containers/com.benyu.noop/Data")
        let appSupport = container.appendingPathComponent("Library/Application Support")
        XCTAssertEqual(StorePaths.macOSProductionContainerAppSupport(
            defaultingTo: appSupport, bundleIdentifier: "com.benyu.noop",
            isTestFlightDistribution: true, homeDirectory: container), appSupport)
    }

    func testUpstreamProductionStillPinsItsOriginalContainer() {
        let appSupport = home.appendingPathComponent("Library/Application Support")
        XCTAssertEqual(StorePaths.macOSProductionContainerAppSupport(
            defaultingTo: appSupport, bundleIdentifier: "com.noopapp.noop",
            isTestFlightDistribution: false, homeDirectory: home).path,
            "/Users/noop-isolation-fixture/Library/Containers/com.noopapp.noop/Data/Library/Application Support")
    }

    func testNonDistributionDevelopmentPathIsPreserved() {
        let appSupport = home.appendingPathComponent("Library/Application Support")
        XCTAssertEqual(StorePaths.macOSProductionContainerAppSupport(
            defaultingTo: appSupport, bundleIdentifier: "com.example.dev",
            isTestFlightDistribution: false, homeDirectory: home), appSupport)
    }
    #endif
}
