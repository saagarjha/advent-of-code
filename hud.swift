import AppKit

func solvesFromScoreboard() async throws -> String {
	let data = try await URLSession.shared.data(from: URL(string: "https://adventofcode.com/\(year)/stats")!).0
	let string = (String(data: data, encoding: .utf8) ?? "") as NSString
	let regex = try NSRegularExpression(pattern: #"">\s*\#(day)\s*<span class="stats-both">\s*([0-9]+)</span>\s*<span class="stats-firstonly">\s*([0-9]+)<"#, options: [])
	let matches = regex.matches(in: string as String, options: [], range: NSRange(location: 0, length: string.length))
	guard let match = matches.first,
	match.numberOfRanges == 3 else {
		return ""
	}
	return "\(string.substring(with: match.range(at: 1))) \(string.substring(with: match.range(at: 2)))"
}

@MainActor
class OutputViewController: NSViewController {
	var outputTextView: NSTextView!
	var sample: Bool!
	var process: Process!

	override func loadView() {
		let scrollView = NSTextView.scrollablePlainDocumentContentTextView()
		outputTextView = (scrollView.documentView as? NSTextView?)!
		outputTextView.font = NSFont.monospacedSystemFont(ofSize: 10, weight: .regular)
		outputTextView.usesFindBar = true
		outputTextView.isIncrementalSearchingEnabled = true
		view = scrollView
	}

	func updateOutput() {
		process?.terminate()
		process = Process()
		process.launchPath = root.appendingPathComponent("script.py").path
		process.currentDirectoryURL = root
		if sample {
			process.environment = ["AOC_SAMPLE": "1"]
		}
		let pipe = Pipe()
		process.standardOutput = pipe
		process.standardError = pipe
		do {
			try process.run()
			DispatchQueue.global().async {
				let data = try? pipe.fileHandleForReading.readToEnd()
				let string = data.flatMap { String(data: $0, encoding: .utf8) }
				DispatchQueue.main.async {
					self.outputTextView?.string = string ?? ""
				}
			}
		} catch {
			outputTextView?.string = error.localizedDescription
		}
		outputTextView?.scrollRangeToVisible(NSRange(location: outputTextView.string.utf16.count, length: 0))
	}
}

@MainActor
class ViewController: NSViewController {
	var source: DispatchSourceFileSystemObject!
	var timeLabel: NSTextField!
	var timeLabelTask: Task<Void, Error>!
	var labelUpdateTask: Task<Void, Error>!
	var tabViewController: NSTabViewController!
	var sampleOutputViewController: OutputViewController!
	var realOutputViewController: OutputViewController!

	deinit {
		source.cancel()
	}

	override func loadView() {
		let view = NSView()

		let visualEffectView = NSVisualEffectView()
		visualEffectView.translatesAutoresizingMaskIntoConstraints = false
		visualEffectView.material = .windowBackground
		visualEffectView.wantsLayer = true
		visualEffectView.layer!.cornerRadius = 8
		view.addSubview(visualEffectView)

		let titleLabel = NSTextField(labelWithString: "Challenge \(root.lastPathComponent)")
		titleLabel.font = NSFont.systemFont(ofSize: 20)
		titleLabel.translatesAutoresizingMaskIntoConstraints = false
		view.addSubview(titleLabel)

		timeLabel = NSTextField(labelWithString: "")
		timeLabel.font = NSFont.monospacedDigitSystemFont(ofSize: 16, weight: .regular)
		timeLabel.textColor = .secondaryLabelColor
		timeLabel.translatesAutoresizingMaskIntoConstraints = false
		view.addSubview(timeLabel)

		var components = DateComponents()
		components.year = year
		components.month = 12
		components.day = day - 1
		components.hour = 21
		components.minute = 0
		// components.timeZone = TimeZone.init(abbreviation: "America/New_York")
		let start = Calendar(identifier: .gregorian).date(from: components)!
		let formatter = DateComponentsFormatter()
		labelUpdateTask = Task {
			var solves = ""
			for i in 0..<(.max) {
				if i % 5 == 0 {
					solves = (try? await solvesFromScoreboard()) ?? solves
				}
				timeLabel.stringValue = "\(solves) \(formatter.string(from: Date().timeIntervalSince(start))!)"
				try await Task.sleep(nanoseconds: 1_000_000_000)
			}
		}

		sampleOutputViewController = OutputViewController()
		sampleOutputViewController.sample = true
		_ = sampleOutputViewController.view
		realOutputViewController = OutputViewController()
		realOutputViewController.sample = false
		_ = realOutputViewController.view

		tabViewController = NSTabViewController()
		tabViewController.view.translatesAutoresizingMaskIntoConstraints = false
		tabViewController.addChild(sampleOutputViewController)
		tabViewController.addChild(realOutputViewController)
		view.addSubview(tabViewController.view)
		
		NSLayoutConstraint.activate([
			visualEffectView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
			visualEffectView.centerYAnchor.constraint(equalTo: view.centerYAnchor),
			view.widthAnchor.constraint(equalTo: visualEffectView.widthAnchor),
			view.heightAnchor.constraint(equalTo: visualEffectView.heightAnchor),
			titleLabel.leadingAnchor.constraint(equalToSystemSpacingAfter: view.leadingAnchor, multiplier: 1),
			titleLabel.topAnchor.constraint(equalToSystemSpacingBelow: view.topAnchor, multiplier: 1),
			timeLabel.leadingAnchor.constraint(greaterThanOrEqualToSystemSpacingAfter: titleLabel.trailingAnchor, multiplier: 1),
			view.trailingAnchor.constraint(equalToSystemSpacingAfter: timeLabel.trailingAnchor, multiplier: 1),
			titleLabel.firstBaselineAnchor.constraint(equalTo: timeLabel.firstBaselineAnchor),
			view.trailingAnchor.constraint(greaterThanOrEqualToSystemSpacingAfter: timeLabel.trailingAnchor, multiplier: 1),
			tabViewController.view.leadingAnchor.constraint(greaterThanOrEqualToSystemSpacingAfter: view.leadingAnchor, multiplier: 1),
			view.trailingAnchor.constraint(greaterThanOrEqualToSystemSpacingAfter: tabViewController.view.trailingAnchor, multiplier: 1),
			tabViewController.view.topAnchor.constraint(equalToSystemSpacingBelow: titleLabel.bottomAnchor, multiplier: 1),
			view.bottomAnchor.constraint(equalToSystemSpacingBelow: tabViewController.view.bottomAnchor, multiplier: 1),
			tabViewController.view.widthAnchor.constraint(greaterThanOrEqualToConstant: 400),
			tabViewController.view.heightAnchor.constraint(greaterThanOrEqualToConstant: 500),
		])
		self.view = view

		source = DispatchSource.makeFileSystemObjectSource(fileDescriptor: script, eventMask: .all, queue: .main)
		source.setEventHandler { [unowned self] in
			update()
		}
		source.resume()
		update()
	}

	func update() {
		let sampleLines = (try? String(contentsOf: root.appendingPathComponent("sample"), encoding: .utf8).split(separator: "\n").count) ?? 0
		let realLines = (try? String(contentsOf: root.appendingPathComponent("input"), encoding: .utf8).split(separator: "\n").count) ?? 0
		tabViewController.tabViewItem(for: sampleOutputViewController)!.label = "Sample (\(sampleLines) lines)"
		tabViewController.tabViewItem(for: realOutputViewController)!.label = "Real (\(realLines) lines)"
		sampleOutputViewController.updateOutput()
		realOutputViewController.updateOutput()
	}
}

class Window: NSWindow {
	override var canBecomeKey: Bool {
		true
	}

	override var canBecomeMain: Bool {
		true
	}
}

_ = NSApplication.shared

let root = URL(fileURLWithPath: CommandLine.arguments[1])
let year = Int(root.deletingLastPathComponent().lastPathComponent)!
let day = Int(root.lastPathComponent)!
let script = open(root.appendingPathComponent("script.py").path, O_EVTONLY)
let session = String(data: try! Data(contentsOf: root.deletingPathExtension().deletingLastPathComponent().deletingLastPathComponent().appendingPathComponent("session")), encoding: .utf8)!

let window = Window(contentViewController: ViewController())
window.styleMask.remove(.titled)
window.backgroundColor = .clear
window.isMovableByWindowBackground = true
let screen = NSScreen.main!.visibleFrame
let offset: CGFloat = 16
window.setFrameOrigin(NSPoint(x: screen.maxX - offset - window.frame.width, y: screen.maxY - 4 * offset - window.frame.height))
window.level = .floating
NSApp.setActivationPolicy(.accessory)
window.makeKeyAndOrderFront(nil)

extension NSMenuItem {
	convenience init(title: String, action: Selector? = nil, keyEquivalent: String = "", keyEquivalentModifierMask: NSEvent.ModifierFlags? = nil, tag: Int? = nil) {
		self.init(title: title, action: action, keyEquivalent: keyEquivalent)
		keyEquivalentModifierMask.flatMap {
			self.keyEquivalentModifierMask = $0
		}
		tag.flatMap {
			self.tag = $0
		}
	}
}

let submenu = NSMenu(title: "Edit")
submenu.items = [
	NSMenuItem(title: "Quit", action: #selector(NSApplication.terminate(_:)), keyEquivalent: "q"),
	NSMenuItem(title: "Undo", action: Selector(("undo:")), keyEquivalent: "z"),
	NSMenuItem(title: "Undo", action: Selector(("redo:")), keyEquivalent: "Z"),
	NSMenuItem(title: "Cut", action: #selector(NSText.cut(_:)), keyEquivalent: "x"),
	NSMenuItem(title: "Copy", action: #selector(NSText.copy(_:)), keyEquivalent: "c"),
	NSMenuItem(title: "Paste", action: #selector(NSText.paste(_:)), keyEquivalent: "v"),
	NSMenuItem(title: "Select All", action: #selector(NSText.selectAll(_:)), keyEquivalent: "a"),
	NSMenuItem(title: "Find…", action: #selector(NSResponder.performTextFinderAction(_:)), keyEquivalent: "f", tag: NSTextFinder.Action.showFindInterface.rawValue),
	NSMenuItem(title: "Find and Replace…", action: #selector(NSResponder.performTextFinderAction(_:)), keyEquivalent: "f", keyEquivalentModifierMask: [.command, .option], tag: NSTextFinder.Action.replaceAndFind.rawValue),
	NSMenuItem(title: "Find Next", action: #selector(NSResponder.performTextFinderAction(_:)), keyEquivalent: "g", tag: NSTextFinder.Action.nextMatch.rawValue),
	NSMenuItem(title: "Find Previous", action: #selector(NSResponder.performTextFinderAction(_:)), keyEquivalent: "G", tag: NSTextFinder.Action.previousMatch.rawValue),
	NSMenuItem(title: "Use Selection for Find", action: #selector(NSResponder.performTextFinderAction(_:)), keyEquivalent: "e", tag: NSTextFinder.Action.setSearchString.rawValue),
	NSMenuItem(title: "Jump to Selection", action: #selector(NSResponder.centerSelectionInVisibleArea(_:)), keyEquivalent: "j"),
]
let item = NSMenuItem(title: "Edit", action: nil, keyEquivalent: "")
item.submenu = submenu
let menu = NSMenu()
menu.items = [
	item
]
NSApp.mainMenu = menu

NSApp.run()
