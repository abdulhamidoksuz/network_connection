from netmiko import ConnectHandler
import os, time

class connection:
    def __init__(self, username, password, device_type):
        self.username = username
        self.password = password
        self.device_type = device_type
        self.name = 'Null'
        self.successfull = False
        self.output = str()
        self.lastoutput = str()
        self.ip_list = list()
        self.commands = list()
        self.desktop_path = os.environ['USERPROFILE'].replace('\\','/')+'/Desktop/'
        self.log_time = '-'.join([str(value) for index, value in enumerate(time.localtime()) if index < 6])
        self.log_dir = f'{self.desktop_path}automation/logs/{self.log_time}/'
        os.mkdir(self.log_dir)

    def login(self, ip):
        self.output = str()
        self.lastoutput = str()
        try:
            self.net_connect = ConnectHandler(device_type=self.device_type, host=ip, username=self.username, password=self.password)
            self.successfull = True
            self.name = self.net_connect.find_prompt().replace('#', '')
            print(ip + '\tConnected')
        except:
            self.successfull = False
            with open(f'{self.log_dir}Not_Reachable.txt', 'a') as f:
                f.write(ip+'\n')
            print(ip+'\tNot_Connected')
    def enable(self):
        if self.successfull:
            self.net_connect.enable()
            self.name = self.net_connect.find_prompt().replace('#', '')

    def login_enable(self, ip):
        self.output = str()
        self.lastoutput = str()
        try:
            self.net_connect = ConnectHandler(device_type=self.device_type, host=ip, username=self.username, password=self.password)
            self.successfull = True
        except:
            self.successfull = False
            with open(f'{self.log_dir}Not_Reachable.txt', 'a') as f:
                f.write(ip+'\n')
            print(ip + '\tNot_Connected')
        if self.successfull:
            self.net_connect.enable()
            self.name = self.net_connect.find_prompt().replace('#', '')
            print(ip + '\tConnected')


    def command(self, cmd, expect=r'[#>$?]'):
        if self.successfull:
            self.lastoutput =cmd + "\n" + self.net_connect.send_command(cmd, strip_prompt=False, expect_string=expect)
            self.output += self.lastoutput

    def logout(self):# DENEMEK GEREKLI ##########################################
        self.net_connect.disconnect()
        self.successfull = False

    def read_ip_list(self):
        with open(f'{self.desktop_path}automation/ip_list.txt', 'r') as f:
            self.ip_list = f.read().split('\n')

    def read_commands(self):
        with open(f'{self.desktop_path}automation/commands.txt', 'r') as f:
            self.commands = f.read().split('\n')

    def log_save(self):
        if self.successfull:
            with open(f'{self.log_dir}{self.name}.txt', 'w') as f:
                f.write(self.output)

    def run_commands(self):
        for ip in self.ip_list:
            self.login_enable(ip)
            if self.successfull:
                for command in self.commands:
                    self.command(command)
                self.log_save()

