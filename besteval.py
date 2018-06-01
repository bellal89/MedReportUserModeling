import os

models = ["BB2", "BM25", "BM25F", "DFIC", "DFIZ", "DFR_BM25", "DFRee", "DFReeKLIM", "DFRWeightingModel", "DirichletLM", "Dl", "DLH", "DLH13", "DPH", "Hiemstra_LM", "Idf", "IFB2", "In_expB2", "In_expC2", "InB2", "InL2", "Js_KLs", "LemurTF_IDF", "LGD", "MDL2", "ML2", "PerFieldNormWeightingModel", "PL2", "PL2F", "SingleFieldModel", "StaticFeature", "StaticScoreModifierWeightingModel", "Tf", "TF_IDF", "WeightingModel", "WeightingModelFactory", "WeightingModelLibrary", "XSqrA_M"]

with open ("models.txt", "w") as out:
	for model in models:
		os.system("./trec_terrier.sh -r -Dtrec.model=" + model)
		os.system("./trec_terrier.sh -e")

		with open("/home/beloboro/terrier-4.0/var/results/my.eval") as f:
			lines = f.readlines()
			for line in lines:
				if "10 :" in line:
					measure = line.strip().split(" : ")[-1]
					print model + ": " + measure
					out.write(model + ": " + measure + "\n")


