import sys
folder = "part" + sys.argv[1]
outfolder = "files" + sys.argv[1]


div = "#EOR"
i = 1

from os import listdir
from os import makedirs
from os.path import join, isdir

subf = join(outfolder, str(i/10000))
if not isdir(subf):
	makedirs(subf)

outfile = join(outfolder, "files" + str(sys.argv[1]) + ".txt")
with open(outfile, "w") as flist:
	fns = [ join(folder,f) for f in listdir(folder) ]	
	for fn in fns:
		with open(fn, 'r') as f:
			for doc in f.read().strip().split(div):
				subf = join(outfolder, str(i/10000))
				if not isdir(subf):
					makedirs(subf)

				outfn = join(subf, str(i) + ".html")
				flist.write(outfn + "\n")

				with open(outfn, "w") as fo:
					fo.write(doc)
				i += 1

