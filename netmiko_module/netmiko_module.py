import netmiko
from concurrent.futures import ThreadPoolExecutor
import openpyxl

class vdc:
    def __init__(self):
        self.output = str()
        self.temp = str()
        self.login_successfull = False
        try:
            self.server = netmiko.ConnectHandler(ip='192.168.99.100', device_type='linux', username='docker', password='tcuser')
        except:
            print('cannot connect to the server')
            print('***********************************************************************')

    def login(self, ip, username='username', password='password'):
        self.time_command(''.join(['ssh ', username, '@', ip]), time=2)
        if 'yes' in self.temp:
            self.command('yes')
            self.command(password)
            self.login_successfull = True
        elif 'password:' in self.temp:
            self.command(password)
            self.login_successfull = True
        else:
            self.command('\x1A')
            self.login_successfull = False

    def command(self, cmd, expect=r'[#\?$]'):
        self.temp = cmd + '\n' + self.server.send_command(cmd, expect_string=expect, strip_prompt=False)
        self.output += self.temp

    def time_command(self, cmd, time=2):
        self.temp = cmd + '\n' + self.server.send_command_timing(cmd, delay_factor=time/2, strip_prompt=False)
        self.output += self.temp


    def logout(self):
        self.command('exit all')
        self.command('logout')
        self.login_successfull = False

    def disconnect(self):
        self.server.disconnect()

def check(lis, index1):
    temp = True
    for index, i in enumerate(lis[index1:]):
        temp = temp * i
        if temp == False:
            return index+index1, False
    if temp == True:
        return index, True

def threaded_func(obj, lis, ne_script_run):
    index, bool = check(lis, 0)
    while bool == False:
        lis[index][-1] = True
        ne_info = lis[index]
        ne_script_run(obj, ne_info)
        index, bool = check(lis, index)
    print('all done')

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


if __name__ == '__main__':

    lis = ['uname','ls -al', 'ps']



