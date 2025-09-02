import csv, pymupdf
#from pprint import pprint
from os.path import isfile, join
from os import listdir

def print_developed_by():
	print("------------------------------------------------------------------------------")
	print("-- Developed by Robert Lengberg in 2025 using the pyMuPDF library.          --")
	print("-- Intended for use with OKAB waybills to import packages using MEXIEC.     --")
	print("------------------------------------------------------------------------------")

print_developed_by()

src_path = "./pdf/"
out_path = "./csv/"
files = [f for f in listdir(src_path) if isfile(join(src_path, f))]

for file in files:

	document = pymupdf.open(src_path+file)
	file_name = file[0:-4]
	data = {"packages": {}, "consumed": {}, "header": {}}
	i = 1

	if (file[-4:] != '.pdf'):
		print(f"\t{file} needs to have .pdf extension. Skipping file...")
		continue # skip current iteration and jump to next

	# This string is expected on the first page of the PDF.
	# Jump to next iteration otherwise.
	if document.is_pdf and "OKAB Sweden AB" in document.get_page_text(0):
		print(f"\tProcessing {file}")
	else:
		print(f"\t{file} is not matching the expected PDF structure. Skipping file...")
		print(f"\tIf this is a waybill from OKAB, please verify that it is not a printed & scanned version.")
		continue #skip current iteration and jump to next

	for page in document:
		tabs = page.find_tables()

		if len(tabs.tables) < 1:
			continue

		for tab in tabs.tables:

			for l in tab.extract():

				for s in l:

					if s is None:
						continue

					# find order number and position
					search = "Ordernummer (line)\n"
					if search in s:
						# extract the parts we want
						order = s[len(search):-1].replace(" ", "").replace("(", "-").split("-")

						# verify that we got exactly 2 parts and that they are both numeric.
						if len(order) == 2 and order[0].isnumeric() and order[1].isnumeric():
							data["header"]["order_no"] = order[0]
							data["header"]["order_pos"] = int(order[1])
							print(f"\t...found order position {data["header"]["order_no"]}-{data["header"]["order_pos"]}.")
						else:
							print(f"\t...order position with unknown format found {order}, skipping...")
							continue


					#find the tare weight per package
					search = "Tara\n"
					if search in s:
						begin_at = len(search)
						data["header"]["tare"] = s[begin_at:begin_at+len(s)-begin_at]
						if len(data["header"]["tare"]) > 0:
							print(f"\t...found tare weight: {data["header"]["tare"]} kg/package.")
						else:
							print(f"\t...no tare weight found in document, skipping...")

						

				# gather all new packages
				if len(l) == 7 and l[0].isnumeric() and len(l[0]) == 14:
					if len(data["packages"]) < 1:
						print(f"\t...found packages to be created.")
					data["packages"][i] = {
						"type": "P",
						"id": l[0],
						"sheets": l[3],
						"gross_wt": l[4],
						"net_wt": l[5],
					}
					i += 1
					

				# gather all consumed packages
				if len(l) == 6 and l[3].isnumeric() and len(l[3]) == 14:
					if len(data["consumed"]) < 1:
						print(f"\t...found source material to be consumed.")
					data["consumed"][i] = {
						"type": "I",
						"id": l[3],
						"new_length": 0
					}
					i += 1

	if len(data["packages"]) > 0 and len(data["header"]) == 3:
		if len(data["consumed"]) < 1:
			print(f"\t...WARNING! No source material found. Check waybill!")
			print(f"\t\tSource material used for this order will not be")
			print(f"\t\tautomatically consumed when importing this file!")
		else:
			print(f"\t...found {len(data["packages"])} packages to be created.")
			print(f"\t...found {len(data["consumed"])} reels to be consumed.")

		with open(out_path+str(data["header"]["order_no"])+"-"+str(data["header"]["order_pos"])+".csv", 'w', encoding='utf-8', newline='') as f:
			csvw = csv.writer(f, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
			
			csvw.writerow([
				'Type', 'Id', 'Order No', 'Order Pos', 'Net wt', 'Gross wt', 'Tare', 'Sheets'
			])
			for seq in data["packages"]:
				csvw.writerow([
					data["packages"][seq]["type"],
					data["packages"][seq]["id"],
					data["header"]["order_no"],
					data["header"]["order_pos"],
					data["packages"][seq]["net_wt"],
					data["packages"][seq]["gross_wt"],
					data["header"]["tare"],
					data["packages"][seq]["sheets"],
				])

			for seq in data["consumed"]:
				csvw.writerow([
					data["consumed"][seq]["type"],
					data["consumed"][seq]["id"],
					data["consumed"][seq]["new_length"],

				])

		print(f"\tProcessed {file}, output sent to {out_path[2:]}{file_name}.csv")
	else:
		print(f"\t... no header data and/or data for packages to be created.")

	print(f"\n")

print_developed_by()
input("You can now close the window (press enter or use the X)")