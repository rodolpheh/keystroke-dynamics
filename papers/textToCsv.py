import csv
import argparse

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Transform a list of links to papers from a text file to a csv')
	parser.add_argument('--lo', dest='lo', action='store_true',
		                help='LibreOffice mode')
	parser.add_argument('--fr', dest='fr', action='store_true',
						help='If LibreOffice is in french')

	args = parser.parse_args()
	linkFunction = "LIEN.HYPERTEXTE" if args.fr else "HYPERLINK"

	docs = []
	with open("sources", 'r') as f:
		doc = {}
		count = 0
		for line in f.readlines():
			line = line.strip()
			if len(line) == 0:
				count = 0
				doc["comments"] = '\n'.join(doc["comments"])
				docs.append(doc)
				continue
			if count == 0:
				doc = {}
				doc["comments"] = []
				doc["address"] = line
			if count == 1:
				doc["authors"] = line
			if count == 2:
				doc["title"] = ("=" + linkFunction + "(\"" + doc["address"] + "\"; \"" + line + "\")") if args.lo else line
			if count == 3:
				doc["year"] = int(line)
			if count > 3:
				doc["comments"].append(line)
			count += 1

	with open("sources.csv", 'w') as f:
		headers = ["authors", "title", "year", "comments"]
		if not args.lo:
			headers.insert(0, "address")
		else:
			[doc.pop("address") for doc in docs]
		sourcesWriter = csv.DictWriter(f, delimiter='|', fieldnames=headers)
		sourcesWriter.writeheader()
		for doc in docs:
			sourcesWriter.writerow(doc)

	print("Done")
