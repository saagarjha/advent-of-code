#!/usr/bin/env swift

import Foundation

struct Leaderboard: Decodable {
	struct Member: Decodable {
		struct Star: Decodable {
			let getStarTs: Int
		}

		let name: String?
		let completionDayLevel: [String: [String: Star]]
	}

	let members: [String: Member]
}

let decoder = JSONDecoder()
decoder.keyDecodingStrategy = .convertFromSnakeCase
let leaderboard = try decoder.decode(Leaderboard.self, from: FileHandle.standardInput.readToEnd()!)

let dateFormatter = DateFormatter()
dateFormatter.dateStyle = .none
dateFormatter.timeStyle = .medium
dateFormatter.timeZone = .init(identifier: "America/New_York")
for day in 1...25 {
	let completed = leaderboard.members.values.compactMap { member in
		member.completionDayLevel["\(day)"].flatMap {
			(member.name, $0)
		}
	}
	guard !completed.isEmpty else {
		continue
	}
	for part in 1...2 {
		print("Day \(day) part \(part):")
		let solves = completed.compactMap { (name, level) in
			level["\(part)"].flatMap {
				(name, $0.getStarTs)
			}
		}.sorted {
			$0.1 < $1.1
		}
		for solve in solves {
			print("\((solve.0 ?? "")!.padding(toLength: 20, withPad: " ", startingAt: 0)) \(dateFormatter.string(from: Date(timeIntervalSince1970: TimeInterval(solve.1))))")
		}
		print()
	}
	print()
}
