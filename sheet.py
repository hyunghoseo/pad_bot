import csv
with open('dump.csv') as f:
	dump = dict(filter(None, csv.reader(f)))


dumplist = []
for key, value in dump.iteritems():
	temp = key
	dumplist.append(temp)

