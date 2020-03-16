from tlcst_netmiko import connection

connect = connection('username', 'password', 'cisco_ios')
connect.read_ip_list()
connect.read_commands()
for i in connect.ip_list:
    changed_int_count = 0
    connect.login_enable(i)
    connect.command('sho run', expect=connect.name+'#')
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
    print(changed_int_count)
    connect.log_save()