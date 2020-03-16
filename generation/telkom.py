import openpyxl
import os
import time
def excel(way, sheet_name):
    wb = openpyxl.load_workbook(filename=way)
    sheet = wb[sheet_name]
    excel = list()
    for row in sheet.iter_rows():
        line = []
        for cell in row:
            line.append(cell.internal_value)
        excel.append(line)
    return excel

def exceltodict(way, sheetname):
    excellist = excel(way, sheetname)
    returndict = dict()
    for node in excellist[1:]:
        returndict[node[4]] = list()
    for node in excellist[1:]:
        temp = dict()
        for index, info in enumerate(node):
            temp[excellist[0][index]] = info
        returndict[node[4]].append(temp)
    return returndict

Write = str()
asnumber = {'NGA': '65300', 'SGC': '64521', 'SGS': '64531'}
#time1 = time.time()
sheet2 = exceltodict('C:/Users/oksuz/Desktop/generate/Telkom/TELKOM_v5.xlsx','Descriptions')
#time2 = time.time()
#print(f"Done in {time2-time1}")
nodes = list()
while True:
    line = input()
    t = list()
    if line:
        for i in line.split('\t'):
            t.append(i)
        nodes.append(t)
    else:
        break
print(nodes)
#print(f"Done in {time.time()-time2}")
path = 'C:/Users/oksuz/Desktop/generate/Telkom/generated'
os.chdir(path)
for index,i in enumerate(nodes):
    if i[2] == '1400':
        REG = i[-1]#sheet2[i[4][:-3]][0]['REG']
        AS = asnumber[REG]
        try:
            DESCRIPTION = sheet2[i[4][:-3]][0]['INTERFACE_DESCRIPTION']
        except:
            DESCRIPTION = 'RAN_' + i[0].split()[0]+'_'+REG
        CADDRESS = i[4]
        UADDRESS = nodes[index+1][4]
        if 'SRA' in i[9][-10:]:
            TUNNEL = 'auto-bind-tunnel resolution any'
        if 'SAR' in i[9][-10:]:
            TUNNEL = 'auto-bind mpls'
        print('#',i[9])
        for ins in os.listdir(path+'/'+ i[9]):
            if 'ABR' not in ins and 'EBU' not in ins and 'FTTX' not in ins: accesspath = ins
        #print('accesspath= ', accesspath, i[9])
        with open(path+'/'+i[9]+'/' + accesspath) as f:
            temp = f.readlines()
        for j in temp:
            if '  community add ' in j:
                ISIS = j.split('"')[-2]
                break
        for j in temp:
            if 'route-distinguisher' in j:
                RD = j.split(' ')[-1].split(':')[0]
                break
        for index,j in enumerate(temp):
            if ('SINGLE_OM' in j or 'LTE' in j) and 'WBS' not in j:
                SAP = temp[index-2].split(' ')[2][:-1]#bunun icinde enter var--------------
                break

        output = f"""
###############  TELKOM ########################
/configure qos        
        sap-ingress 410 create #410 for Telkom LTE UserPlane Mobile services   
            description "Telkom-LTE_SAP-Ingress-Policy_7705SAR"
            queue 1 create
            exit
            queue 5 create
            exit
            queue 6 create
                rate max cir max
            exit
            fc "h2" create
                queue 5
            exit
            fc "be" create
                queue 1
            exit
            fc "ef" create
                queue 6
            exit
            dscp af41 fc "h2" 
            dscp be fc "be" 
            dscp ef fc "ef" priority high
        exit

/configure router policy-options
begin
community "TLK_LTE_User_VPRN_RT" members "target:{AS}:40009"
community "TLK_LTE_Control_VPRN_RT" members "target:{AS}:40010"
policy-statement "TLK_LTE_UP_VPRN_POC3/4_Import"
                entry 10
                    from
                        protocol bgp-vpn
                        community "TLK_LTE_User_VPRN_RT"
                    exit
                    action next-entry
                    exit
                exit
                entry 20
                    from
                        protocol bgp-vpn
                        community "Core_ISIS_Comm"
                    exit
                    action accept
                    exit
                exit
                entry 30
                    from
                        protocol bgp-vpn
                        community "TLK_LTE_User_VPRN_RT"
                    exit
                    action next-entry
                    exit
                exit
                entry 40
                    from
                        protocol bgp-vpn
                        community {ISIS}
                    exit
                    action accept
                    exit
                exit
exit
policy-statement "TLK_LTE_UP_VPRN_POC3/4_Export"
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "TLK_LTE_User_VPRN_RT" "{ISIS}"
                    exit
                exit
exit
policy-statement "TLK_LTE_CP_VPRN_POC3/4_Import"
                entry 10
                    from
                        protocol bgp-vpn
                        community "TLK_LTE_Control_VPRN_RT"
                    exit
                    action next-entry
                    exit
                exit
                entry 20
                    from
                        protocol bgp-vpn
                        community "Core_ISIS_Comm"
                    exit
                    action accept
                    exit
                exit
                entry 30
                    from
                        protocol bgp-vpn
                        community "TLK_LTE_Control_VPRN_RT"
                    exit
                    action next-entry
                    exit
                exit
                entry 40
                    from
                        protocol bgp-vpn
                        community {ISIS}
                    exit
                    action accept
                    exit
                exit
exit
policy-statement "TLK_LTE_CP_VPRN_POC3/4_Export"
                entry 10
                    from
                        protocol direct
                    exit
                    to
                        protocol bgp-vpn
                    exit
                    action accept
                        community add "TLK_LTE_Control_VPRN_RT" "{ISIS}"
                    exit
                exit
exit
commit
exit all 


/configure service customer 810 create
            description "TELKOM"
exit

/configure service vprn 40010 customer 810 create
    description "{REG}-LTE-Telkom_Mobile-Control-VPRN"
    vrf-import "TLK_LTE_CP_VPRN_POC3/4_Import"
    vrf-export "TLK_LTE_CP_VPRN_POC3/4_Export"
    autonomous-system  {AS}
    route-distinguisher {RD}:40010
    {TUNNEL}
    enable-bgp-vpn-backup ipv4
    interface  "TELKOM_MOCN_CP_1" create
        shutdown
        description "{DESCRIPTION}"
        address {CADDRESS}
        sap {SAP}:1400 create
            ingress
                qos 400
            exit
            collect-stats
        exit
    exit
    service-name "{REG}-TLK-LTE-CONTROL-VPRN"
    no shutdown
exit

/configure service vprn 40009 customer 810 create
    description "{REG}-LTE-Telkom_Mobile-User-VPRN"
    vrf-import "TLK_LTE_UP_VPRN_POC3/4_Import"
    vrf-export "TLK_LTE_UP_VPRN_POC3/4_Export"
    autonomous-system  {AS}
    route-distinguisher {RD}:40009
    {TUNNEL}
    enable-bgp-vpn-backup ipv4
    interface  "TELKOM_MOCN_UP_1" create
        shutdown
        description "{DESCRIPTION}"
        address {UADDRESS}
        sap {SAP}:1401 create
            ingress
                qos 410
            exit
            collect-stats
        exit
    exit
    service-name "{REG}-TLK-LTE-USER-VPRN"
    no shutdown
exit
###############  TELKOM END    ########################

"""
        Write += output
        with open(path + '/' + i[9] + '/' + accesspath, 'a') as f:
            f.write(output)
