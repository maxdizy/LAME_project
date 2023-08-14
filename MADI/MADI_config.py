import os
import io
import sys
import json
import string
from django.http import HttpResponse
from PyPDF2 import PdfReader, PdfWriter
from mailmerge import MailMerge
from datetime import date
from .MADI_NLP import getPNs, keywords
from django.conf import settings
from django.core.files.storage import Storage
from LAME.settings import get_file, push_json

def readIRF(f, CN):
    #read pdf and get field
    reader = PdfReader(f)
    page = []
    for i in range(len(reader.pages)-1):
        page.append(reader.pages[i].extract_text())
    fields = reader.get_form_text_fields()
    dict(fields)

    database = json.load(get_file('data/database.json'))
    
    #find PNs
    potROEDs = []
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
                potROEDs.append({'caseNo' : case, 'partNos' : ', '.join(database[case][0]), 'keyWords' : ', '.join(database[case][1])})

    #find if potential ROED
    ROED = False
    if len(potROEDs) != 0: ROED = True

    #update database
    database.update({CN: [PNs, KWs]})

    URL = '/var/www/LAME_project/media/' + str(CN) + '-' + str(fields['Tail Row1']) + '-' + IRFTitle + '.docx'
    #URL = r'C:\Users\e443176\Documents\CLASSIFIED\case-tests\\' + str(CN) + '-' + str(fields['Tail Row1']) + '-' + IRFTitle + '.docx'

    #push potROED
    push_json('data/potROED', potROEDs)

    #push database
    push_json('data/database.json', database)

    return fields['Tail Row1'], IRFTitle, description, affected, fields['IRF'], ROED, potROEDs, URL

def writeERF(CN, AC, SD, D, PN, IRF, ROED, new_ROED_file, potROED, dart, mod, URL):
    #pull ERF Template
    if mod:
        document = MailMerge(io.BytesIO(get_file('data/MADI ERF Template for Mod.docx').read()))
    else:
        document = MailMerge(io.BytesIO(get_file('data/MADI ERF Template.docx').read()))
    #setup basic fields
    tails = {'601': '5626', '602': '5627', '603': '5635', '604': '5636', '605': '5637', '606' : '5649', '607': '5650', '608': '5651', '609': '5652', '610': '5664', '611': '5665', '612': '5666', '613': '5667', '614': '5687', '615': '5688', '616': '5689', '617': '5690'}
    cat = 'Choose an item.'
    ref = ''
    response = '''Disposition #1:
                General notes (add as required):
                '''
    MPList = ''
    if dart : dartRes='Yes'
    else: dartRes='No'

    #setup ROED fields
    if new_ROED_file != None:
        cat = 'Category 5 : Repeat Non-Standard Repairs'
        ref = new_ROED_file.name + '; 	Previous Similar Repair\n'
        try:
            ERFreader = PdfReader(new_ROED_file)
            ERFtext = ''
            for i in range(len(ERFreader.pages)-1):
                ERFtext += ERFreader.pages[i].extract_text()
            response = ERFtext[ERFtext.find('LM Response'):ERFtext.find('LM Technical Approval')]
            MPList = ERFtext[ERFtext.find('Material / Parts List'):ERFtext.find('Authoring and authorization')]
        except:
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
        DART=dartRes,
        Insert = MPList,
        Footer=CN,
        Choose=cat)

    #push populated ERF
    document.write(URL)
    #os.startfile(filLoc)

def writeDart(AC, D, PN, dartPath, CN):
    #create DART form
    reader = PdfReader(io.BytesIO(get_file("data/DART template.pdf").read()))
    fields = reader.get_form_text_fields()

    writer = PdfWriter()
    page = reader.pages[0]
    writer.add_page(page)

    writer.update_page_form_field_values(
        writer.pages[0], {"Aircraft Serial No": AC, "Statement of Condition": D, "Part Numbers": PN}
        )
    writer.write(dartPath)

#workFlow('1')