import AppKit

func solvesFromScoreboard() async throws -> String {
	let data = try await URLSession.shared.data(from: URL(string: "https://adventofcode.com/\(year)/stats")!).0
	let string = (String(data: data, encoding: .utf8) ?? "") as NSString
	let regex = try NSRegularExpression(pattern: #"">\s*\#(day)\s*<span class="stats-both">\s*([0-9]+)</span>\s*<span class="stats-firstonly">\s*([0-9]+)<"#, options: [])
	let matches = regex.matches(in: string as String, options: [], range: NSRange(location: 0, length: string.length))
	guard let match = matches.first,
		match.numberOfRanges == 3
	else {
		return ""
	}
	let goldString = string.substring(with: match.range(at: 1))
	let silverString = string.substring(with: match.range(at: 2))
	if let gold = Int(goldString.trimmingCharacters(in: .whitespaces)),
		let silver = Int(silverString.trimmingCharacters(in: .whitespaces))
	{
		return "**: \(gold) *: \(gold + silver)"
	} else {
		return "\(goldString) \(silverString)"
	}
}

class Buffer {
	let lock: UnsafeMutablePointer<os_unfair_lock>

	var _text: String = ""
	var text: String {
		os_unfair_lock_lock(lock)
		defer {
			os_unfair_lock_unlock(lock)
		}
		return _text
	}

	func append(_ content: String) {
		os_unfair_lock_lock(lock)
		defer {
			os_unfair_lock_unlock(lock)
		}
		_text.append(content)
	}

	init() {
		lock = .allocate(capacity: 1)
		// Note: technically wrong
		lock.initialize(to: os_unfair_lock())
	}

	deinit {
		lock.deallocate()
	}
}

@MainActor
class OutputViewController: NSViewController {
	var outputTextView: NSTextView!
	var sample: Bool!
	var process: Process!
	var lines = 0

	override func loadView() {
		let scrollView = NSTextView.scrollablePlainDocumentContentTextView()
		outputTextView = (scrollView.documentView as? NSTextView?)!
		outputTextView.font = NSFont.monospacedSystemFont(ofSize: 10, weight: .regular)
		outputTextView.usesFindBar = true
		outputTextView.isIncrementalSearchingEnabled = true
		view = scrollView
	}

	override func viewDidAppear() {
		super.viewDidAppear()
		outputTextView.scrollRangeToVisible(NSRange(location: outputTextView.string.utf16.count, length: 0))
	}

	func updateOutput() {
		let process = Process()
		process.launchPath = root.deletingLastPathComponent().deletingLastPathComponent().appendingPathComponent("repl.py").path
		process.arguments = [root.appendingPathComponent("script.py").path]
		process.currentDirectoryURL = root
		if sample {
			process.environment = ["AOC_SAMPLE": "1"]
		}
		let pipe = Pipe()
		process.standardOutput = pipe
		process.standardError = pipe
		Task { @MainActor in
			let result = await Task { @MainActor () -> String in
				try process.run()
				self.process?.terminate()
				self.process = process
				return try await Task { () -> String in
					let buffer = Buffer()
					let updateTask = Task { @MainActor in
						while true {
							outputTextView.string = buffer.text
							outputTextView.scrollRangeToVisible(NSRange(location: outputTextView.string.utf16.count, length: 0))
							try await Task.sleep(nanoseconds: 2_000_000_000)
						}
					}
					defer {
						updateTask.cancel()
					}
					lines = 0
					for try await byte in pipe.fileHandleForReading.bytes {
						buffer.append(String(UnicodeScalar(byte)))
						if byte == 0x0a {
							lines += 1
						}
					}
					return buffer.text
				}.value
			}.result
			let output: String
			switch result {
				case .success(let string):
					output = string
				case .failure(let error):
					output = error.localizedDescription
			}
			outputTextView.string = output
			outputTextView.scrollRangeToVisible(NSRange(location: outputTextView.string.utf16.count, length: 0))
		}
	}
}

@MainActor
class ViewController: NSViewController {
	var start: Date!
	var source: DispatchSourceFileSystemObject!
	var timeLabel: NSTextField!
	var timeLabelTask: Task<Void, Error>!
	var labelUpdateTask: Task<Void, Error>!
	var tabViewController: NSTabViewController!
	var sampleOutputViewController: OutputViewController!
	var realOutputViewController: OutputViewController!
	var currentOutputViewController: OutputViewController {
		tabViewController.tabViewItems[tabViewController.selectedTabViewItemIndex].viewController as! OutputViewController
	}
	var outputInfoLabel: NSTextField!
	var copyButton: NSButton!

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
		timeLabel.addGestureRecognizer(NSClickGestureRecognizer(target: self, action: #selector(resetStart(_:))))
		view.addSubview(timeLabel)

		var components = DateComponents()
		components.year = year
		components.month = 12
		components.day = day - 1
		components.hour = 21
		components.minute = 0
		components.timeZone = TimeZone.init(abbreviation: "America/New_York")
		start = Calendar(identifier: .gregorian).date(from: components)!
		let formatter = DateComponentsFormatter()

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

		outputInfoLabel = NSTextField(labelWithString: "0 lines")
		outputInfoLabel.translatesAutoresizingMaskIntoConstraints = false
		view.addSubview(outputInfoLabel)

		copyButton = NSButton(title: "Copy Last", target: self, action: #selector(copyLast(_:)))
		copyButton.controlSize = .large
		copyButton.translatesAutoresizingMaskIntoConstraints = false
		copyButton.keyEquivalent = "\r"
		view.addSubview(copyButton)

		labelUpdateTask = Task {
			var solves = ""
			for i in 0..<(.max) {
				if i % 2 == 0 {
					solves = (try? await solvesFromScoreboard()) ?? solves
				}
				timeLabel.stringValue = "\(solves) \(formatter.string(from: Date().timeIntervalSince(start))!)"
				outputInfoLabel.stringValue = "\(currentOutputViewController.lines) lines"
				try await Task.sleep(nanoseconds: 1_000_000_000)
			}
		}

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
			tabViewController.view.widthAnchor.constraint(greaterThanOrEqualToConstant: 375),
			tabViewController.view.heightAnchor.constraint(greaterThanOrEqualToConstant: 500),
			outputInfoLabel.leadingAnchor.constraint(equalToSystemSpacingAfter: view.leadingAnchor, multiplier: 1),
			copyButton.leadingAnchor.constraint(greaterThanOrEqualToSystemSpacingAfter: outputInfoLabel.trailingAnchor, multiplier: 1),
			copyButton.firstBaselineAnchor.constraint(equalTo: outputInfoLabel.firstBaselineAnchor),
			copyButton.topAnchor.constraint(equalToSystemSpacingBelow: tabViewController.view.bottomAnchor, multiplier: 1),
			view.trailingAnchor.constraint(equalToSystemSpacingAfter: copyButton.trailingAnchor, multiplier: 1),
			view.bottomAnchor.constraint(equalToSystemSpacingBelow: copyButton.bottomAnchor, multiplier: 1),
		])
		self.view = view

		source = DispatchSource.makeFileSystemObjectSource(fileDescriptor: script, eventMask: .all, queue: .main)
		source.setEventHandler { [unowned self] in
			update()
		}
		source.resume()
		update()
	}

	@IBAction func resetStart(_ sender: Any?) {
		start = Date()
	}

	@IBAction func copyLast(_ sender: Any?) {
		tabViewController.selectedTabViewItemIndex = 1
		guard let last = currentOutputViewController.outputTextView.string.split(separator: "\n").last else {
			return
		}
		NSPasteboard.general.declareTypes([.string], owner: nil)
		NSPasteboard.general.setData(Data(last.utf8), forType: .string)
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
let session = String(data: try! Data(contentsOf: root.deletingLastPathComponent().deletingLastPathComponent().appendingPathComponent("session")), encoding: .utf8)!

let window = Window(contentViewController: ViewController())
window.styleMask.remove(.titled)
window.backgroundColor = .clear
window.isMovableByWindowBackground = true
let screen = NSScreen.main!.visibleFrame
let offset: CGFloat = 16
window.setFrameOrigin(NSPoint(x: screen.maxX - offset - window.frame.width, y: screen.maxY - 4 * offset - window.frame.height))
window.level = .floating
window.collectionBehavior = .canJoinAllSpaces
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

var watchdogCheckin = true
let watchdogQueue = DispatchQueue(label: "watchdog")
let watchdogTimer = DispatchSource.makeTimerSource(queue: watchdogQueue)
watchdogTimer.schedule(deadline: .now(), repeating: .seconds(5))
watchdogTimer.setEventHandler {
	guard watchdogCheckin else {
		execve(CommandLine.arguments.first!, CommandLine.unsafeArgv, environ)
		exit(1)
	}
	watchdogCheckin = false
}
watchdogTimer.activate()
let responsivenessTimer = Timer(fire: Date(), interval: 1, repeats: true) { _ in
	watchdogQueue.sync {
		watchdogCheckin = true
	}
}
RunLoop.main.add(responsivenessTimer, forMode: .common)

NSApp.run()
