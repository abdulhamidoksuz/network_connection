import openpyxl
import os

def excel(way, sheet_name):
    wb = openpyxl.load_workbook(filename=way)
    sheet = wb[sheet_name]
    excellist = list()
    for row in sheet.iter_rows():
        line = []
        for cell in row:
            line.append(cell.internal_value)
        excellist.append(line)
    return excellist


def exceltodict(way, sheetname, key):
    excellist = excel(way, sheetname)
    returndict = dict()
    for node in excellist[1:]:
        returndict[node[key]] = list()
    for node in excellist[1:]:
        temp = dict()
        for index, info in enumerate(node):
            temp[excellist[0][index]] = info
        returndict[node[key]].append(temp)
    return returndict

def portallofiles(desktoppath):
    portallofileslist = list()
    for i in os.listdir(desktoppath):
        if 'allocation' in i.lower() and '~$' not in i.lower():
            portallofileslist.append(i)
    return portallofileslist

def takeinput():
    print('yapistir')
    t = list()
    while True:
        line = input()
        if line:
            t.append(line)
        else:
            print('----------')
            break
    return t

searchlist = takeinput()
desktoppath = '/'.join([os.environ['USERPROFILE'].replace('\\','/'),'Desktop'])+'/'
allportallo = list()
portallofileslist = portallofiles(desktoppath)

for i in portallofileslist:
    file = excel(desktoppath+i,'System_IPs')
    for j in file:
        allportallo.append(j)
print('done')
for i in allportallo:
    if isinstance(i[0], str):
        for j in searchlist:
            if j in i[0]:
                print('\t'.join([j,i[0],i[1],i[7],i[14]]))
