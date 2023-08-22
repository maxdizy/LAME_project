import json
#from .MADI_NLP import getPNs, keywords
import MADI_NLP

with open(r'data_old\sn_customerservice_case.json', 'r', encoding="utf8") as db:
            database = json.load(db)
cases = database['records']
database = {}
#create Database
for index, case in enumerate(cases):
    PNstemp = []
    KWstemp = []
    CN = case['number']
    CSD = case['short_description']
    CD = case['description']
    for PN in MADI_NLP.getPNs(CSD):
        if PN not in PNstemp:
            PNstemp.append(PN)
    for PN in MADI_NLP.getPNs(CD):
        if PN not in PNstemp:
            PNstemp.append(PN)
    for KW in MADI_NLP.keywords(CSD):
        if KW not in KWstemp:
            KWstemp.append(KW)
    for KW in MADI_NLP.keywords(CD):
        if KW not in KWstemp:
            KWstemp.append(KW)
    if len(PNstemp) != 0:
        database.update({CN: [PNstemp, KWstemp]})
    print("%.2f%% cases complete" % (index/len(cases) * 100))

with open("data_old/database_new.json", "w") as outfile:
    json.dump(database, outfile)