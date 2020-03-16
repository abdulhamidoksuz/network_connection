from classes import takeinput,wcaccess,abr
import os

def inputtodict():
    print('-' * 20)
    inputs = takeinput()
    returndict = dict()
    for i in inputs:
        returndict[i.split('\t')[0]] = list()
    for i in inputs:
        values = i.split('\t')
        returndict[values[0]].append(values)
    return returndict

desktoppath = os.environ['USERPROFILE'].replace('\\','/')+'/Desktop/'
inputs = inputtodict()
for key,listeler in inputs.items():
    access = wcaccess()
    ports = set()
    sdps = set()
    abrset = set()
    abrs = {
        '30': [abr(), False, 'SGC_MTA_ABR_12-1'],
        '31': [abr(), False, 'SGS_JFL_ABR_12-1'],
        '32': [abr(), False, 'NGA_PRO_ABR_12-1'],
        '40': [abr(), False, 'SGC_MTA_ABR_12-2'],
        '41': [abr(), False, 'SGS_JFL_ABR_12-2'],
        '42': [abr(), False, 'NGA_PRO_ABR_12-2'],
        '50': [abr(), False, 'NGA_PSI_ABR_12-1'],
        '60': [abr(), False, 'NGA_PSI_ABR_12-2'],
    }
    abrsdp = str(int(listeler[0][1].split('.')[-1])*10)
    for i in abrs.values():
        i[0].sdp(abrsdp, listeler[0][0], listeler[0][1], 'bgp')

    if 'SRA' in key[-10:]: access.qos('SRA')
    if 'SAR' in key[-10:]: access.qos('SAR')

    for liste in listeler:
        access.customer(liste[3], liste[6])
        vplsabr1, vplsabr2 = 'NA', 'NA'
        if '-MT' in liste[-2]:
            vplsabr1,vplsabr2 = '30', '41'
            sdps.add(vplsabr1)
            sdps.add(vplsabr2)
            abrs[vplsabr1][0].customer(liste[3], liste[6])
            abrs[vplsabr1][0].epipe(liste[3], liste[3], liste[6], 'lag-101', liste[4], abrsdp)
            abrs[vplsabr2][0].customer(liste[3], liste[6])
            abrs[vplsabr2][0].epipe(liste[3], liste[3], liste[6], 'lag-102', liste[4], abrsdp)
            abrs[vplsabr1][1] = True
            abrs[vplsabr2][1] = True

        elif 'JFL'in liste[-2]:
            vplsabr1, vplsabr2 = '31', '40'
            sdps.add(vplsabr1)
            sdps.add(vplsabr2)
            abrs[vplsabr1][0].customer(liste[3], liste[6])
            abrs[vplsabr1][0].epipe(liste[3], liste[3], liste[6], 'lag-101', liste[4], abrsdp)
            abrs[vplsabr2][0].customer(liste[3], liste[6])
            abrs[vplsabr2][0].epipe(liste[3], liste[3], liste[6], 'lag-102', liste[4], abrsdp)
            abrs[vplsabr1][1] = True
            abrs[vplsabr2][1] = True

        elif 'PSI' in liste[-2]:
            vplsabr1, vplsabr2 = '50', '42'
            sdps.add(vplsabr1)
            sdps.add(vplsabr2)
            abrs[vplsabr1][0].customer(liste[3], liste[6])
            abrs[vplsabr1][0].epipe(liste[3], liste[3], liste[6], 'lag-101', liste[4], abrsdp)
            abrs[vplsabr2][0].customer(liste[3], liste[6])
            abrs[vplsabr2][0].epipe(liste[3], liste[3], liste[6], 'lag-102', liste[4], abrsdp)
            abrs[vplsabr1][1] = True
            abrs[vplsabr2][1] = True
        elif 'PRO' in liste[-2]:
            vplsabr1, vplsabr2 = '32', '60'
            sdps.add(vplsabr1)
            sdps.add(vplsabr2)
            abrs[vplsabr1][0].customer(liste[3], liste[6])
            abrs[vplsabr1][0].epipe(liste[3], liste[3], liste[6], 'lag-101', liste[4], abrsdp)
            abrs[vplsabr2][0].customer(liste[3], liste[6])
            abrs[vplsabr2][0].epipe(liste[3], liste[3], liste[6], 'lag-102', liste[4], abrsdp)
            abrs[vplsabr1][1] = True
            abrs[vplsabr2][1] = True

        access.vpls(liste[3], liste[6], liste[5], liste[-1], liste[4], vplsabr1, vplsabr2)
        ports.add(liste[-1])

    for sdp in sdps:
        if sdp == '30': access.sdp('30','SGC_MTA_ABR_12-1','10.172.0.3','bgp')
        if sdp == '31': access.sdp('31','SGS_JFL_ABR_12-1','10.174.0.3','bgp')
        if sdp == '32': access.sdp('32','NGA_PRO_ABR_12-1','10.53.0.3','bgp')
        if sdp == '40': access.sdp('40','SGC_MTA_ABR_12-2','10.172.0.4','bgp')
        if sdp == '41': access.sdp('41','SGS_JFL_ABR_12-2','10.174.0.4','bgp')
        if sdp == '42': access.sdp('42','NGA_PRO_ABR_12-2','10.53.0.4','bgp')
        if sdp == '50': access.sdp('50','NGA_PSI_ABR_12-1','10.53.0.5','bgp')
        if sdp == '60': access.sdp('60','NGA_PSI_ABR_12-2','10.53.0.6','bgp')
    for port in ports:
        access.port(port,'ACC:Management_and_EBU:OP', '9122')

    os.mkdir(desktoppath+key)
    with open(desktoppath+key+'/'+key+'.cfg', 'a') as f:
        f.write(access.output())
    for abrwrite in abrs.values():
        if abrwrite[1] == True:
            with open(desktoppath+key+'/'+abrwrite[-1]+'.cfg', 'a') as f:
                f.write(abrwrite[0].output())
