import os
import sys
import xml.etree.ElementTree as ET
import re
import itertools
import codecs
import string
import subprocess


def get_metric_vals(res_fn):
	if metric == 'ndcg':
		os.system("trec_eval -q -m all_trec clef2013t3.qrels.test.graded.txt " + res_fn + " | grep \"ndcg_cut_10 \" > trec1")
	else:
		os.system("trec_eval -q clef2013t3.qrels.test.binary.txt " + res_fn + " | grep \"P_10 \" > trec1")

	res = {}
	with open("trec1") as trec:
		for line in trec.readlines():
			parts = line.strip().split()
			if len(parts) >= 3:
				res[parts[1]] = float(parts[2])
	return res

def ds(topic):
	ds = topic.find("discharge_summary").text
	ds_fn = os.path.join(ds_dir, ds)[:-4] + ".html"
	# ds_fn = os.path.join(ds_dir, ds) + ".html"
	with open(ds_fn) as ds:
		return ds.read()

def get_doc_text(fn):
	if fn in index:
		proc = subprocess.Popen("python html2text.py " + index[fn] + " utf-8", shell=True, stdout=subprocess.PIPE)
		doc_text = proc.communicate()[0]
		return doc_text
	else:
		print "This name aren't presented in index.\n"
		return None



if len(sys.argv) <= 3:
	print "Usage:\nscript.py <p|ndcg> discharge_summaries_dir topics_fn"
	sys.exit()

metric = sys.argv[1]
ds_dir = sys.argv[2]
topics_fn = sys.argv[3]

dirs = ['files1', 'files2', 'files3', 'files4', 'files5', 'files6', 'files7', 'files8']
index = {}

for rootDir in dirs:
	print rootDir + " processing..."
	for dirName, subdirList, fileList in os.walk(rootDir):
		for fname in fileList:
			index[fname] = os.path.join(dirName,fname)

print "index built: " +str(len(index)) + " items"

methods = [
	("_baseline", [baseline]), 
	("_description", [baseline, get_desc]), 
	("_age", [baseline, get_age]), 
	("_gender", [baseline, get_gender]), 
	("_surg_procedure", [baseline, get_procedure]), 
	("_chief_complaint", [baseline, get_complaint]), 
	("_diseases", [baseline, get_diseases])
	# "_age_desc":[baseline, get_age, get_desc]
]

for (name, ms) in methods:
	print name + ": " + " ".join([m.__name__ for m in ms])

# var = raw_input("Methods has done! Press Enter")

tree = ET.parse(topics_fn)
root = tree.getroot()
topics = {}

for topic in root:
	tid = topic.find("id")
	topics[tid] = topic


for (name, ms) in methods:
	if name != "_baseline":
		name = name + "_0.303"
	fn = name + ".xml.res"

#qtest2014.1 Q0 uptod4830_12_033995 99 12.331082508380014 DirichletLM.mu=2400.0
	with codecs.open(fn, "w", encoding="utf-8") as tfn:
		for line in tfn.readlines():
			qid, a, docid, rank, score, m = line.strip().split()
			doc_text = get_doc_text(docid)
			print docid + " len " + str(len(doc_text))

