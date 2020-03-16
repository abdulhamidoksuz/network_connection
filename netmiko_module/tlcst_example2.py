from tlcst_netmiko import connection
import time 

connect = connection('onur.aksoy', 'Ekim.2019', 'cisco_ios')
connect.read_ip_list()
connect.read_commands()
for i in connect.ip_list:
    changed_int_count = 0
    connect.login_enable(i)
    connect.command('show run', expect=connect.name+'#')
    for j in connect.output.split('!'):
        if 'interface FastEthernet' in j or 'interface GigabitEthernet' in j:
            if 'authentication host-mode' in j:
                changed_int_count += 1
                connect.command('conf t')
                connect.command(j.strip().split('\n')[0])
                connect.command('authentication event fail action next-method')
                connect.command('authentication control-direction in')
                connect.command('end')
    connect.command('wr')
    with open(f'{connect.log_dir}general.txt', 'a') as f:
        f.write('\t'.join([connect.name,  i,str(changed_int_count)])+'\n')
    connect.log_save()