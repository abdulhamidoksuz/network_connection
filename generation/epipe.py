from classes import access, exceltodict
#port mapping fonksiyonu lazim

def sdpdict(services):
    tempdict = dict()
    sdpids = {
        '3':[1,30,31,32,33,34,35],
        '4':[1,40,41,42,43,44,45],
        '5':[1,50,51,52,53,54,55],
        '6':[1,60,61,62,63,64,65]
    }
    for servicedict in services:
        tempdict[servicedict['Destination_Nokia_Node_Name']] = [servicedict['Destination_Nokia_System_IP']]
    for _,iplist in tempdict.items():
        lastoctet = iplist[0].split('.')[-1]
        iplist.append(sdpids[lastoctet][sdpids[lastoctet][0]])
        sdpids[lastoctet][sdpids[lastoctet][0]] += 1
    return tempdict

Twampoctet = {'16': '208', '17': '209', '18': '210', '19': '211', '32': '212', '33': '213', '34': '214', '35': '215', '48': '216', '49': '217', '50': '218', '51': '219', '64': '220', '65': '221', '66': '222', '67': '223', '80': '224', '81': '225', '82': '226', '83': '227', '96': '228', '97': '229', '98': '230', '99': '231', '112': '232', '113': '233', '114': '234', '115': '235', '128': '236', '129': '237', '130': '238', '131': '239', '144': '240', '145': '241', '146': '242', '147': '243', '160': '244', '161': '245', '162': '246', '163': '247', '176': '248', '177': '249', '178': '250', '179': '251', '192': '252', '193': '253', '194': '254', '195': '255', '0': 'xxxx', '1': 'xxxx', '2': 'xxxx', '3': 'xxxx', '4': 'xxxx', '5': 'xxxx', '6': 'xxxx', '7': 'xxxx', '8': 'xxxx', '9': 'xxxx', '10': 'xxxx', '11': 'xxxx', '12': 'xxxx', '13': 'xxxx', '14': 'xxxx', '15': 'xxxx', '20': 'xxxx', '21': 'xxxx', '22': 'xxxx', '23': 'xxxx', '24': 'xxxx', '25': 'xxxx', '26': 'xxxx', '27': 'xxxx', '28': 'xxxx', '29': 'xxxx', '30': 'xxxx', '31': 'xxxx', '36': 'xxxx', '37': 'xxxx', '38': 'xxxx', '39': 'xxxx', '40': '207', '41': 'xxxx', '42': 'xxxx', '43': 'xxxx', '44': 'xxxx', '45': 'xxxx', '46': 'xxxx', '47': 'xxxx', '52': 'xxxx', '53': 'xxxx', '54': 'xxxx', '55': 'xxxx', '56': 'xxxx', '57': 'xxxx', '58': 'xxxx', '59': 'xxxx', '60': 'xxxx', '61': 'xxxx', '62': 'xxxx', '63': 'xxxx', '68': 'xxxx', '69': 'xxxx', '70': 'xxxx', '71': 'xxxx', '72': 'xxxx', '73': 'xxxx', '74': 'xxxx', '75': 'xxxx', '76': 'xxxx', '77': 'xxxx', '78': 'xxxx', '79': 'xxxx', '84': 'xxxx', '85': 'xxxx', '86': 'xxxx', '87': 'xxxx', '88': 'xxxx', '89': 'xxxx', '90': 'xxxx', '91': 'xxxx', '92': 'xxxx', '93': 'xxxx', '94': 'xxxx', '95': 'xxxx', '100': 'xxxx', '101': 'xxxx', '102': 'xxxx', '103': 'xxxx', '104': 'xxxx', '105': 'xxxx', '106': 'xxxx', '107': 'xxxx', '108': 'xxxx', '109': 'xxxx', '110': 'xxxx', '111': 'xxxx', '116': 'xxxx', '117': 'xxxx', '118': 'xxxx', '119': 'xxxx', '120': 'xxxx', '121': 'xxxx', '122': 'xxxx', '123': 'xxxx', '124': 'xxxx', '125': 'xxxx', '126': 'xxxx', '127': 'xxxx', '132': 'xxxx', '133': 'xxxx', '134': 'xxxx', '135': 'xxxx', '136': 'xxxx', '137': 'xxxx', '138': 'xxxx', '139': 'xxxx', '140': 'xxxx', '141': 'xxxx', '142': 'xxxx', '143': 'xxxx', '148': 'xxxx', '149': 'xxxx', '150': 'xxxx', '151': 'xxxx', '152': 'xxxx', '153': 'xxxx', '154': 'xxxx', '155': 'xxxx', '156': 'xxxx', '157': 'xxxx', '158': 'xxxx', '159': 'xxxx', '164': 'xxxx', '165': 'xxxx', '166': 'xxxx', '167': 'xxxx', '168': 'xxxx', '169': 'xxxx', '170': 'xxxx', '171': 'xxxx', '172': 'xxxx', '173': 'xxxx', '174': 'xxxx', '175': 'xxxx', '180': 'xxxx', '181': 'xxxx', '182': 'xxxx', '183': 'xxxx', '184': 'xxxx', '185': 'xxxx', '186': 'xxxx', '187': 'xxxx', '188': 'xxxx', '189': 'xxxx', '190': 'xxxx', '191': 'xxxx', '196': 'xxxx', '197': 'xxxx', '198': 'xxxx', '199': 'xxxx', '200': 'xxxx', '201': 'xxxx', '202': 'xxxx', '203': 'xxxx', '204': 'xxxx', '205': 'xxxx', '206': 'xxxx', '207': 'xxxx', '208': 'xxxx', '209': 'xxxx', '210': 'xxxx', '211': 'xxxx', '212': 'xxxx', '213': 'xxxx', '214': 'xxxx', '215': 'xxxx', '216': 'xxxx', '217': 'xxxx', '218': 'xxxx', '219': 'xxxx', '220': 'xxxx', '221': 'xxxx', '222': 'xxxx', '223': 'xxxx', '224': 'xxxx', '225': 'xxxx', '226': 'xxxx', '227': 'xxxx', '228': 'xxxx', '229': 'xxxx', '230': 'xxxx', '231': 'xxxx', '232': 'xxxx', '233': 'xxxx', '234': 'xxxx', '235': 'xxxx', '236': 'xxxx', '237': 'xxxx', '238': 'xxxx', '239': 'xxxx', '240': 'xxxx', '241': 'xxxx', '242': 'xxxx', '243': 'xxxx', '244': 'xxxx', '245': 'xxxx', '246': 'xxxx', '247': 'xxxx', '248': 'xxxx', '249': 'xxxx', '250': 'xxxx', '251': 'xxxx', '252': 'xxxx', '253': 'xxxx', '254': 'xxxx'}
servicesexcel = exceltodict('C:/Users/oksuz/Desktop/service.xlsx', 'Sheet2')
#portallo = exceltodict('C:/Users/oksuz/Desktop/epipe.xlsx', 'SGC')
asnumber = {'NGA': '65300', 'SGC': '64521', 'SGS': '64531'}
print('asdasda')
for nename,servicesinfo in servicesexcel.items():
    accessoutput = access()
    sdps = sdpdict(servicesinfo)
    #port
    accessoutput.port('1/3/12', 'ACC:EBU:MAN', 9000)
    #QOS
    if 'SRA' in nename[-10:]:
        accessoutput.qos('SRA')
    elif 'SAR' in nename[-10:]:
        accessoutput.qos('SAR')
    #policy
    accessoutput.policy(servicesinfo[0]['Source_Region'])
    #sdp
    for abr, abrlist in sdps.items():
        if servicesinfo[0]['Destination_ISIS_Instance'] == servicesinfo[0]['ISIS_instance']:
            accessoutput.sdp(abrlist[1], abr[4:], abrlist[0], 'mpls')
        else:
            accessoutput.sdp(abrlist[1], abr[4:], abrlist[0], 'bgp')
    #customer
    for service in servicesinfo:
        accessoutput.customer(abrlist[1],'Description')
    #epipe
    for service in servicesinfo:
        pass
    #twamp
    twampoctetlist = servicesinfo[0]['System_IP'].split('.')
    twampip = '.'.join([twampoctetlist[0], twampoctetlist[1], Twampoctet[twampoctetlist[2]], twampoctetlist[3]])
    accessoutput.twamp(servicesinfo[0]['Source_Region'], asnumber[servicesinfo[0]['Source_Region']], servicesinfo[0]['System_IP'], twampip)
    print(accessoutput.portstr)
    print(accessoutput.qosstr)
    print(accessoutput.policystr)
    print(accessoutput.sdpstr)
    print(accessoutput.twampstr)










