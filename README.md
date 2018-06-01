# MedReportUserModeling
A complex of programs to model the user searching by medical documents. 

The main script to model users is ds_qu_expand.py.
It builds the user model by means of her medical report and makes test search requests to the Terrier search system.
That's why, for proper using this script you need to 
1. set up the search engine with a corpus of medical webpages indexed
2. prepare medical reports and test search queries in TREC format.

The data can be found at CLEF eHealth track: https://sites.google.com/site/clefehealth2014/.

After you have the data and the Terrier search engine working, use the script in following way:
'''
python ds_qu_expand.py medical_reports_dir queries_fn
'''
To detect the best Terrier ranking function use the besteval.py script.
