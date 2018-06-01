import os
import sys
import xml.etree.ElementTree as ET
import re

def get_yellow_fields(ds_fn):
	with open(ds_fn) as ds:
		txt = ds.read()
		yf = [m.group(1) for m in re.finditer("style=\'BACKGROUND-COLOR: #ffff00\'\>(.+?)\</SPAN\>", txt, re.DOTALL) if m]
		return yf

def get_dd(ds_fn):
	with open(ds_fn) as ds:
		txt = ds.read()
		dd = re.search('[Dd]ischarge [Dd]iagnos.*?\<SPAN .+?\>(.+?)\</SPAN\>', txt, re.DOTALL)
		if not dd:
			return ""

		print "dd"
		return dd.group(1).split()

def get_text(ds_fn, name):
	with open(ds_fn) as ds:
		txt = ds.read()
		pattern = name + '\:.*?\<[Pp]\>(.+?)\</[Pp]\>'
		pro = re.search(pattern, txt, re.DOTALL)
		if not pro:
			return ""
		return pro.group(1).split()

def get_complaint(ds_fn):
	return get_text(ds_fn, "[Cc]hief [Cc]omplaint")

def get_procedure(ds_fn):
	return get_text(ds_fn, "[Mm]ajor [Ss]urgical or [iI]nvasive [pP]rocedure")

def get_gender(ds_fn):
	with open(ds_fn) as ds:
		txt = ds.read()
		gender = re.search('[Ss]ex\:\s*?([FM])', txt)
		if not gender:
			return ""
		sign = gender.group(1)
		if sign == "M":
			return ["male", "masculine", "man", "boy"]
		if sign == "F":
			return ["female", "feminine", "woman", "girl"]
		return ""

def get_age(ds_fn):
	with open(ds_fn) as ds:
		txt = ds.read()
		dob = re.search('[Dd]ate [Oo]f [Bb]irth\:\s+\[\*\*(\d+?)-.+?\*\*\]', txt)
		dods = re.search('[Dd]ischarge [Dd]ate\:\s+\[\*\*(\d+?)-.+?\*\*\]', txt)
		if not dob or not dods:
			return ""
		age = int(dods.group(1)) - int(dob.group(1))
		if age <= 10:
			return ["infant", "baby", "child"]
		if age <= 20:
			return ["child", "adolescent", "teenager"]
		if age <= 60:
			return ["adult"]
		return ["senior", "elderly", "elder"]

def baseline(ds_fn):
	return []

res = {}

def fill_equery(tree, method):
	root = tree.getroot()
	for weight in ["1.0", "0.75", "0.5", "0.25"]:
		for topic in root:
			ds = topic.find("discharge_summary").text
			ds_fn = os.path.join(ds_dir, ds) + ".html"
			words = method(ds_fn)

			equery = topic.find("equery")
			if equery is None:
				ET.SubElement(topic, "equery")

			txt = topic.find("title").text
			if len(words) > 0:
				add = " ".join([w + "^" + weight for w in words])
				if method.__name__ == "get_age" or method.__name__ == "get_gender":
					add = "{" + add + "}"
				txt = txt + " " + add
			topic.find("equery").text = txt

		fn = str(topics_fn[:-4]) + "." + method.__name__ + "." + weight + ".xml"
		tree.write(fn)

		os.system("./../../bin/trec_terrier.sh -r -Dtrec.model=DirichletLM -Dtrec.topics=" + fn)
		os.system("trec_eval -q -m all_trec ../../etc/clef2014t3.qrels.test.graded.txt my.res | grep \"ndcg_cut_10 \" > trec")

		with open("trec") as trec:
			for line in trec.readlines():
				parts = line.strip().split()
				if len(parts) >= 3:
					if parts[1] not in res.keys():
						res[parts[1]] = []
					res[parts[1]].append((method.__name__ + "." + weight, parts[2]))


if len(sys.argv) <= 2:
	print "Usage:\nscript.py discharge_summaries_dir topics_fn"
	sys.exit()

ds_dir = sys.argv[1]
topics_fn = sys.argv[2]

tree = ET.parse(topics_fn)

for m in [baseline, get_age, get_gender, get_procedure, get_complaint, get_dd]:
	fill_equery(tree, m)

vs = {}

with open("result.txt", "w") as res_fn:
	for item in sorted(res.items(), key=lambda x: 0 if x[0] == "all" else int(x[0][10:])):
		res_fn.write(item[0] + "\n")
		print item[0]
		baseline = max([float(x[1]) if x[0].strip().startswith("baseline") else 0.0 for x in item[1]])
		for x in item[1]:
			if float(x[1]) > baseline:
				if x[0] not in vs.keys():
					vs[x[0]] = []
				vs[x[0]].append((item[0], float(x[1]) - baseline))

		vals_list = sorted(item[1], key=lambda x: float(x[1]), reverse=True)
		for vals in vals_list:
			res_fn.write("\t" + vals[0] + "\t" + vals[1] + "\n")
		res_fn.write("\n")

	for v in sorted(vs.items(), key=lambda x: max([y[1] for y in x[1]]), reverse=True):
		res_fn.write(v[0] + "\n")
		for y in sorted(v[1], key=lambda x: x[1], reverse=True):
			res_fn.write("\t" + y[0] + "\t" + str(y[1]) + "\n")



