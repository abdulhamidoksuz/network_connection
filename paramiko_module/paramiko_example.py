#!/usr/bin/env/python
# ne_login(ip) command(com) all_close() printout() issuccessfull() ne_name() output()
# excel_page(way, sheet_name)-->return list, sheet_number
from paramiko_module import para, excel_page
devices, a = excel_page('D:/Docs/python/script/poc3west.xlsx','Sheet1')
commands, a = excel_page('D:/Docs/python/script/poc3west.xlsx','commands')
west = para("west")
east = para("east")
for device in devices:
    if (device[2] == 'west'):
        west.ne_login(device[1])
        if west.issuccessfull():
            for command in commands:
                west.command(command[0])
            g = open("D:/Docs/python/script/haocheck/" + device[0] +"-"+device[3]+"-"+device[1] + ".txt", "a+b")
            g.write(west.out)
            g.close()
        else:
            print(device[0]+' ' + device[1] + 'fail to login')
    if (device[2] == 'east'):
        east.ne_login(device[1])
        if east.issuccessfull():
            for command in commands:
                east.command(command[0])
            g = open("D:/Docs/python/script/haocheck/" + device[0] +"-"+device[3]+"-"+device[1] + ".txt", "a+b")
            g.write(east.out)
            g.close()
        else:
            print(device[0]+' ' + device[1] + 'fail to login')
east.all_close()
west.all_close()
