import os
import io
import sys
import json
import string
from PyPDF2 import PdfReader, PdfWriter
from mailmerge import MailMerge
from datetime import date
import shutil
from .MADI_NLP import getPNs, keywords
from django.conf import settings
from django.core.files.storage import Storage
from LAME import settings

def readIRF(f, CN):
    #read pdf and get field
    reader = PdfReader(f)
    page = []
    for i in range(len(reader.pages)-1):
        page.append(reader.pages[i].extract_text())
    fields = reader.get_form_text_fields()
    dict(fields)

    database = json.load(settings.get_file('data/database.json'))
    
    #find PNs
    potROED = []
    IRFTitle = fields['IRF Title']
    description = fields['Text1']
    PNs = []
    KWs = []
    affected = ''
    for PN in getPNs(IRFTitle):
        if PN not in PNs:
            PNs.append(PN)
            if len(affected) > 0 : affected += ', '
            affected += str(PN)
    for PN in getPNs(description):
        if PN not in PN:
            PNs.append(PN)
            if len(affected) > 0 : affected += ', '
            affected += str(PN)
    for KW in keywords(IRFTitle):
        if KW not in KWs:
            KWs.append(KW)
    for KW in keywords(description):
        if KW not in KWs:
            KWs.append(KW)

    #find PN
    for PN in PNs:
        for case in database:
            if PN in database[case][0]:
                potROED.append(case)

    #find if potential ROED
    ROED = False
    if len(potROED) != 0: ROED = True

    #update database
    database.update({CN: [PNs, KWs]})

    #push potROED
    settings.push_json('data/potROED', potROED)
    #json.dump(potROED, settings.push_file('data/potROED', potROED))

    #push database
    settings.push_json('data/database.json', database)
    #json.dump(potROED, settings.push_file('data/database.json', database))

    return CN, fields['Tail Row1'], IRFTitle, description, affected, fields['IRF'], ROED, potROED

def writeERF(CN, AC, SD, D, PN, IRF, ROED, new_ROED_file, potROED, dart, mod, IRFfile):
    #pull ERF Template
    if mod:
        document = MailMerge(io.BytesIO(settings.get_file('data/MADI ERF Template for Mod.docx').read()))
    else:
        document = MailMerge(io.BytesIO(settings.get_file('data/MADI ERF Template.docx').read()))
    #setup basic fields
    tails = {'601': '5626', '602': '5627', '603': '5635', '604': '5636', '605': '5637', '606' : '5649', '607': '5650', '608': '5651', '609': '5652', '610': '5664', '611': '5665', '612': '5666', '613': '5667', '614': '5687', '615': '5688', '616': '5689', '617': '5690'}
    cat = 'Choose an item.'
    ref = ''
    response = '''Disposition #1:
                General notes (add as required):
                '''
    MPList = ''

    #setup ROED fields
    if ROED: 
        cat = 'Category 5 : Repeat Non-Standard Repairs'
        for case in potROED:
            ref += case + '; 	Previous Similar Repair\n'
        if new_ROED_file:
            with open('data/ROEDlocation.txt', 'r') as rf:
                    ROEDfile_path = rf.read()
                    ROEDfile_path = ROEDfile_path[2:-1]
                    print(ROEDfile_path)
            try:
                ERFreader = PdfReader(ROEDfile_path)
                ERFtext = ''
                for i in range(len(ERFreader.pages)-1):
                    ERFtext += ERFreader.pages[i].extract_text()
                response = ERFtext[ERFtext.find('LM Response'):ERFtext.find('LM Technical Approval')]
                MPList = ERFtext[ERFtext.find('Material / Parts List'):ERFtext.find('Authoring and auth`orization')]
            except:
                #MADI.show_big_error('Cannot read ROED file or file does not have proper format. \n ERF must have \'LM Response\' header under LM Response, \n\'LM Technical Approval\' dropdown, and \'Material / Parts List:\'')
                pass

    #populate fields
    document.merge(
        Case=CN + ' Rev.-',
        Select=AC + ' / ' + tails[AC],
        Short=SD,
        Description=D,
        Affected='PN ' + PN,
        Relevant='IRF ' + IRF + ' - Attached in ServiceFLO',
        Referances = ref,
        Date = '{:%y %b %d}'.format(date.today()),
        Disposition = response,
        Insert = MPList,
        Choose=cat)

    #push populated ERF
    ERFL = settings.get_file('data/ERFL.txt').read().decode()
    print(ERFL)
    SD = str(SD.translate(str.maketrans('','',string.punctuation)))
    folLoc = ERFL + '\\' + str(CN) + '-' + str(AC) + '-' + SD 
    try:
        os.makedirs(folLoc)
    except:
        print("Folder already exists; Pushing to folder.")
    filLoc = folLoc + '\\' + str(CN) + '-' + str(AC) + '-' + SD + '.docx'
    document.write(filLoc)
    os.startfile(filLoc)

    # #move IRF to folder
    # IRFpath = (settings.MEDIA_ROOT + '\\' + Storage.get_valid_name(Storage, IRFfile))
    # shutil.copy(IRFpath, folLoc)

    #create DART form
    if dart : createDart(AC, D, PN, folLoc, CN)

    #push to sharePoint
    #MADI_sharePoint.toSharepoint(filLoc)

def createDart(AC, D, PN, folLoc, CN):
    reader = PdfReader("data/DART Template.pdf")
    fields = reader.get_form_text_fields()

    writer = PdfWriter()
    page = reader.pages[0]
    writer.add_page(page)

    writer.update_page_form_field_values(
    writer.pages[0], {"Aircraft Serial No": AC, "Statement of Condition": D, "Part Numbers": PN}
    )

    #create form
    path = folLoc + "/DART-" + CN
    with open(path, "wb") as output_stream:
        writer.write(output_stream)
    print("HERE")
    os.startfile(path)

#workFlow('1')