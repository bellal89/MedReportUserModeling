import sys
import os
from os.path import join
from multiprocessing import Pool

dirs = sys.argv[1:]
uid = "#UID:"

def process(rootDir): 
	for dirName, subdirList, fileList in os.walk(rootDir):
	    print dirName
	    for fname in fileList:
	        fn = join(dirName, fname)
	        print('	%s' % fn)
	        doc = open(fn, 'r')
	        line = doc.readline()
	        while line != '' and uid not in line:
	        	line = doc.readline()
	        doc.close()
	        docid = ""
	        if uid in line:
	        	docid = line.strip().split(":")[-1]
	        if docid != "":
	        	os.rename(fn, join(dirName, docid))

if __name__ == '__main__':
	p = Pool(len(dirs))
	print "Started pool of threads: " + str(len(dirs))
	print
	p.map(process, dirs)