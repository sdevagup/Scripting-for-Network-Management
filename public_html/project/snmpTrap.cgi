#!/usr/bin/python
#
#	Program Description: detect link failure - up/down status from SNMP Trap
print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<link rel='stylesheet' href='https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'>")
print("<link rel='stylesheet' href='style.css'>")
print("<title>Fault Management via SNMP Trap</title>")
print("</head>")
print("<body>")

from datetime import date,datetime

year = str(date.today().year)  # current year

fd = open("/home/net484/share/snmpTrap.log", "r")
trapData = fd.readlines()

flag = 0
print('<div style="width:800px; margin:0 auto;">')
print('<h1>Fault Management via SNMP Trap</h1>')
print('<table border=2 class="table table-striped">')
print('<tr> <TH>Date</TH><TH>Time</TH><TH>Device</TH><TH>Interface</TH><TH>Status</TH></tr>')

values = []
for line in trapData:
    inline = line.rstrip('\n')
    items = inline.split()

    if items[0].find(year) == 0:  # check SNMP trap of the current year
        trapDate = items[0]
        trapTime = items[1]
        ip = items[2].split('(')[0]  # get only the ip address
        if len(items) > 8 and items[7] == 'v1,':
            flag = 1
        else:
            flag = 0
    elif flag == 1 and items[0] == 'iso.3.6.1.4.1.9.1.359':
        trap = "%s %s" % (items[1], items[2])
        flag = 2
    elif flag == 2 and inline.find('iso') > 0:
        n = len(items)
        i = 0
        while i < n:
            if items[i].find('iso.3.6.1.2.1.2.2.1.2.') == 0:
                i += 3
                ifDescr = items[i].replace('"', '')
                flag = 3
            elif items[i].find('iso.3.6.1.2.1.2.2.1.1.') == 0:
                i += 3
                ifIndex = items[i]
            elif items[i].find('iso.3.6.1.2.1.2.2.1.3.') == 0:
                i += 3
                ifType = items[i]
            i += 1
        # end (while)
        if flag == 3:
            trap_date_time=trapDate+' '+trapTime
            date_time_obj =datetime.strptime(trap_date_time, '%Y-%m-%d %H:%M:%S')
            values.append([date_time_obj,trapDate, trapTime, ip, ifDescr, trap,])
            flag = 0
values.sort(key=lambda x:x[0],reverse=True)
values=values[:50]
for row in values:
    if row[5]=='Link Up':
        claz='good'
    else:
        claz='bad'
    print("<tr> <td>%s</td> <td>%s</td> <td>%s</td> <td>%s</td> <td class='%s'>%s</td> </tr>" % (
            row[1], row[2], row[3], row[4], claz,row[5]))
fd.close()

print("</table>")
print('</div>')
print("</body>")
print("</html>")
