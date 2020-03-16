import openpyxl
import re

class access():
    def __init__(self):
        self.portstr = str()
        self.qosstr = str()
        self.policystr = str()
        self.sdpstr = str()
        self.customerstr = str()
        self.epipestr = str()
        self.twampstr = str()
        self.vplsstr = str()
    def port(self, port, des, mtu):
        temp = f"""

 /configure port {port}
     shutdown
     description "{des}"
     ethernet
         mode access
         encap-type dot1q 
         ssm
            no shutdown
         exit   
         mtu {mtu}
     exit
 exit
        """
        self.portstr += temp
    def qos(self, type):
        SRA = """
        
/configure qos
        sap-ingress 900 create
            description "Vodashop_SAP-Ingress-Policy_7750SR"
            queue 3 create
                packet-byte-offset subtract 22
            exit
            fc af create
                queue 3
            exit
            default-fc af
        exit
        sap-ingress 1000 create
            description "EBU-L3-Trusted-SAP-Ingress-Policy-7750SR"
            queue 1 create
                parent "EBU-Scheduler" level 1 cir-level 1
                packet-byte-offset subtract 22
            exit
            queue 3 create
                parent "EBU-Scheduler" level 3 cir-level 3
                packet-byte-offset subtract 22
            exit
            queue 4 profile-mode create
                parent "EBU-Scheduler" level 4 cir-level 4   
                packet-byte-offset subtract 22           
            exit
            queue 5 profile-mode create
                parent "EBU-Scheduler" level 6 cir-level 6
                packet-byte-offset subtract 22
            exit
            queue 6 profile-mode create
                parent "EBU-Scheduler" level 6 cir-level 6
                packet-byte-offset subtract 22
            exit
            queue 7 profile-mode create
                parent "EBU-Scheduler" level 7 cir-level 7
                packet-byte-offset subtract 22
            exit
            queue 11 multipoint create
            exit
            fc "af" create
                queue 3
            exit
            fc "be" create
                queue 1
            exit
            fc "ef" create
                queue 6
                profile in
            exit
            fc "h1" create
                queue 7
                profile in
            exit
            fc "h2" create
                queue 5
                profile in
            exit
            fc "l1" create
                queue 4
                profile in
            exit
            dscp be af23 af33 fc "be"
            dscp ef fc "ef"
            dscp nc1 fc "h1"
            dscp cs4 fc "h2"
            dscp af21 af31 fc "l1"
        exit
        sap-ingress 1001 create
            description "EBU-SAP-Ingress-Policy-7750SR"
            queue 1 create
            exit
            queue 5 profile-mode create
                packet-byte-offset subtract 22
            exit
            queue 11 multipoint create
            exit
            fc "h2" create
                queue 5
                profile in
            exit
            default-fc "h2"
        exit
        sap-ingress 1002 create
            queue 1 create
            exit
            queue 4 profile-mode create
            packet-byte-offset subtract 22
            exit
            queue 11 multipoint create
            exit
            fc l1 create
                queue 4
                profile in
            exit
            default-fc l1
        exit
exit all   

        """
        SAR = """
        
/configure qos
        sap-ingress 900 create
            description "Vodashop_SAP-Ingress-Policy_7705SAR"
            packet-byte-offset subtract 40
            queue 3 create
            exit
            fc af create
                queue 3
            exit
            default-fc af
        exit
        sap-ingress 1000 create
            description "EBU-L3-Trusted-SAP-Ingress-Policy-7705SAR"
            packet-byte-offset subtract 40
            queue 1 create
            exit
            queue 3 create
            exit
            queue 4 create
                rate max cir max
            exit
            queue 5 create
                rate max cir max
            exit
            queue 6 create
                rate max cir max
            exit
            queue 7 create
                rate max cir max
            exit
            fc "af" create
                queue 3
            exit
            fc "be" create
                queue 1
            exit
            fc "ef" create
                queue 6
            exit
            fc "h1" create
                queue 7
            exit
            fc "h2" create
                queue 5
            exit
            fc "l1" create
                queue 4
            exit
            dscp be af23 af33 fc "be"
            dscp ef fc "ef" priority high
            dscp nc1 fc "h1" priority high
            dscp cs4 fc "h2" priority high
            dscp af21 af31 fc "l1" priority high
        exit
        sap-ingress 1001 create
            description "EBU-SAP-Ingress-Policy-7705SAR"
            packet-byte-offset subtract 40
            queue 1 create
            exit
            queue 5 create
                rate max cir max
            exit
            fc "h2" create
                queue 5
            exit
            default-fc "h2"
        exit
        sap-ingress 1002 create            
            packet-byte-offset subtract 40
            queue 1 create
            exit
            queue 4 create
                rate max cir max
            exit
            fc l1 create
                queue 4
            exit
            default-fc l1
        exit
exit all

        """
        if type == 'SAR':
            self.qosstr += SAR
        elif type == 'SRA':
            self.qosstr += SRA
    def policy(self, region):
        temp = f"""
        
/configure router policy-options
begin
		policy-statement "Export_System" 
            entry 10
               action accept community add {region}_Region 
            exit
		exit
commit
exit all

        """
        self.policystr += temp
    def sdp(self, sdpid, ABR, farend, tunneltype):
        if tunneltype == 'bgp':
            temp = f"""
        
/configure service sdp {sdpid} mpls create
    description "to_{ABR}"
    far-end {farend}
    bgp-tunnel
        keep-alive
        shutdown
    exit
    no shutdown
exit                
        """
            self.sdpstr += temp
        elif tunneltype == 'mpls':
            temp = f"""

/configure service sdp {sdpid} mpls create
    description "to_{ABR}"
    far-end {farend}
    lsp "lsp01_to_{ABR[4:]}"
        keep-alive
        shutdown
    exit

    no shutdown
exit                
                    """
            self.sdpstr += temp
    def customer(self, id, des):
        temp = f"""

/configure service
        customer {id} create
            description "{des}"
            no contact
            no phone
        exit
    exit     

        """
        self.customerstr += temp
    def epipe(self, epipeid, customerid, des, sap, vlan, sdp):
        temp = f"""
        
/configure service
        epipe {epipeid} customer {customerid} create
            shutdown
            description "{des}"
            sap {sap}:{vlan} create
            shutdown
            ingress
                    qos 1001
                    queue-override
                        queue 5 create
                            #rate <service-rate> cir <service-rate>
                        exit
                    exit
                exit
                collect-stats
            exit
            spoke-sdp {sdp}:{epipeid} create
                no shutdown
            exit
        exit

        """
        self.epipestr += temp
    def twamp(self, region, asnumber, systemip, address):
        temp = f"""
/configure service vprn 40500 customer 700 create
            description "{region}-TWAMP-Lite-VPRN"
            autonomous-system {asnumber}
            route-distinguisher {systemip}:40500
            vrf-target target:{asnumber}:40500
            auto-bind-tunnel
                resolution any
            exit
            interface "Twamp-Lite_Loopback" create
                address  {address}/32
                loopback
            exit
            twamp-light
                reflector udp-port 64364 create
                    prefix 0.0.0.0/0 create
                    exit
                    no shutdown
                exit
            exit
            service-name "SGC-TWAMP-Lite-VPRN"
            no shutdown
        exit
    exit

        """
        self.twampstr += temp
    def vpls(self, vplsid, description, servicename, port, vlan, sdpid1, sdpid2):
        temp = f"""
/configure service vpls {vplsid} customer {vplsid} create
            description "{description}"
            service-mtu 1518
            service-name "{servicename}"
            fdb-table-size 2500
            stp
                shutdown
            exit
            sap {port}:{vlan} create
                ingress
                    qos 1002
                exit
                no shutdown
                collect-stats
            exit
            mesh-sdp {sdpid1}:{vplsid} create
                no shutdown
            exit
			mesh-sdp {sdpid2}:{vplsid} create
                no shutdown
            exit
            no shutdown

                """
        self.vplsstr += temp
    def output(self):
        return self.portstr+self.qosstr+self.policystr+self.sdpstr+self.customerstr+self.epipestr+self.twampstr+self.vplsstr

class wcaccess(access):
    def qos(self, type):
        SRA = """
/configure qos sap-ingress 1002 create #1002 for FTTx/Wireless services
            description "Broadband Internet FTTx/Wireless-SAP-Ingress-Policy-7750SR"
            queue 1 create
            exit
            queue 4 profile-mode create
            exit
            queue 11 multipoint create
            exit
            fc "l1" create
                queue 4
                profile in
            exit
            default-fc "l1"  

            """
        SAR = """
/configure qos sap-ingress 1002 create #1002 for FTTx/Wireless services
            description "Broadband Internet FTTx/Wireless-SAP-Ingress-Policy-7705"
            queue 1 create
            exit
            queue 4 create
            exit
            fc "l1" create
                queue 4
            exit
            default-fc "l1"
            default-priority high
            
            """
        if type == 'SAR':
            self.qosstr += SAR
        elif type == 'SRA':
            self.qosstr += SRA

class abr():
    def __init__(self):
        self.sdpstr = str()
        self.customerstr = str()
        self.epipestr = str()
    def customer(self, id, des):
        temp = f"""

/configure service
        customer {id} create
            description "{des}"
            no contact
            no phone
        exit
    exit     

        """
        self.customerstr += temp
    def epipe(self, epipeid, customerid, des, sap, vlan, sdp):
        temp = f"""

/configure service
        epipe {epipeid} customer {customerid} create
            shutdown
            description "{des}"
            service-mtu 1518
            service-name "{re.split(r"BNG[-_]", des)[-1]}"
            sap {sap}:{vlan} create
            shutdown
            ingress
                    qos 1001
                    queue-override
                        queue 5 create
                            #rate <service-rate> cir <service-rate>
                        exit
                    exit
                exit
                collect-stats
                no shutdown
            exit
            spoke-sdp {sdp}:{epipeid} create
                no shutdown
            exit
            no shutdown
        exit

        """
        self.epipestr += temp
    def sdp(self, sdpid, access, farend, tunneltype):
        if tunneltype == 'bgp':
            temp = f"""

/configure service sdp {sdpid} mpls create
    description "to_{access}"
    far-end {farend}
    bgp-tunnel
        keep-alive
        shutdown
    exit
    no shutdown
exit                
        """
            self.sdpstr += temp
        elif tunneltype == 'mpls':
            temp = f"""

/configure service sdp {sdpid} mpls create
    description "to_{access}"
    far-end {farend}
    lsp "lsp01_to_{access[4:]}"
        keep-alive
        shutdown
    exit

    no shutdown
exit                
                    """
            self.sdpstr += temp
    def output(self):
        return self.sdpstr+self.customerstr+self.epipestr

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
        returndict[node[0]] = list()
    for node in excellist[1:]:
        temp = dict()
        for index, info in enumerate(node):
            temp[excellist[0][index]] = info
        returndict[node[0]].append(temp)
    return returndict

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

if __name__ == '__main__':
    #a = access()
    #print(a.port('1/3/12', 'ACC:WER:EBU', 'optic', '9212'))
    pass