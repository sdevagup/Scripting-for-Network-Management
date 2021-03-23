#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb
import sys
import datetime as dt
from datetime import datetime

def report(report_type,sdate,edate):
    op = report_type
    if op == "1":
        opcode = 1
    elif op == "2":
        opcode = 2
    elif op == "3":
        opcode = 3
    else:
        print('<p>report type invalid %s</p>'%report_type)
    fmt = "%Y-%m-%d"
    d1 = datetime.strptime(sdate, fmt).date()  # start date
    d2 = datetime.strptime(edate, fmt).date()  # end date

    # For hw05 cgi script, once you are able to get the arguments correctly from the html form, you
    # can use the follow section of code, up to and before the printing of data.
    # initialization of Dictionary

    session = {}  # number of top sessions based on daily, hourly, or raw
    user = {}  # number of active users in the session
    uptime = {}  # uptime since last reboot (not used)
    sysLoad = {}  # systerm load
    peak = {}  # peak load

    delta = d2 - d1

    prefix = "/home/achung/cron/top/"
    for i in range(delta.days + 1):
        x = (d1 + dt.timedelta(days=i))
        mmdd = x.strftime('%m-%d')  # change the format from yyyy-mm-dd to mm-dd
        topFile = prefix + "top." + mmdd
        fd = open(topFile)
        topData = fd.readlines()

        lineNo = 0  # not used, for debugging only
        for line in topData:
            if line.startswith('top'):
                inline = line.rstrip('\n')  # remove '\n' at the end of line
                data = inline.split()
                n = len(data)
                (hour, min, sec) = data[2].split(':')

                # ******* set the key for Dictionary tables
                if opcode == 1:  # daily data
                    key = mmdd
                elif opcode == 2:
                    key = mmdd + ":" + hour  # hourly data
                elif opcode == 3:
                    key = mmdd + ":" + hour + ":" + min  # raw data
                else:
                    print ("Program Assert: unknow opcode=", opcode)
                    return
                if key in session:
                    session[key] += 1
                else:  # intialize all Dictionary tables
                    session[key] = 1
                    user[key] = 0
                    uptime[key] = ''
                    sysLoad[key] = 0.0
                    peak[key] = 0.0

                if n == 14:
                    uptime[key] = data[4] + data[5] + data[6]
                    user[key] += int(data[7])
                    pt = 11
                elif n == 15:  # event occur between 00:00 and 00:59
                    uptime[key] = data[4] + data[5] + data[6] + data[7]
                    user[key] += int(data[8])
                    pt = 12
                else:
                    print("data abnormalities")  # there are additional cases not implemented yet
                    continue

                # print lineNo, n, load1, load2, load3
                load01 = float(data[pt].rstrip(','))  # not used, keept it for debugging
                load05 = float(data[pt + 1].rstrip(','))
                load15 = float(data[pt + 2])
                sysLoad[key] += load15  # average is based on 15-min load average
                if key in peak:
                    # data is collected at 15-min interval, so it is possible that load15>load05
                    if (peak[key] < load01): peak[key] = load01
                    if (peak[key] < load05): peak[key] = load05
                    if (peak[key] < load05): peak[key] = load15

                # print "DEBUF", lineNo, key, load01, load05, load15
                lineNo += 1
        # end one top file
    # end  all top files
    print ('<table border=2>')
    print("<tr> <th>%8s</th> <th>%7s</th>  <th>%6s</th> <th>%6s</th> <th>%6s</th> </tr>" % ("Time", "Session", "User", "Load Avg", "Peak"))

    for key in sorted(session.keys()):
        n = session[key]
        if (n < 1):
            print("Program Assert: n=", n)
            sys.exit(1)
        avgUser = user[key] / n
        avgOccupancy = sysLoad[key] / n
        print("<tr> <td>%8s</td> <td>%7d</td>  <td>%6.1f</td> <td>%6.2f</td> <td>%6.2f</td> </tr>" % (key, session[key], avgUser, avgOccupancy, peak[key]))
    print ('</table>')
print "Content-type:text/html\n"
print "<html>"
print "<head>"
print "<link rel='stylesheet' href='http://140.192.40.5/~net484s02/project/style.css'>"
print "<title>report</title>"
print "</head>"
print "<body>"

#**************************************************
# Get data from fields, use cgi.FieldStorage to create the form object
#**************************************************
# Create instance of FieldStorage 
form   = cgi.FieldStorage() 
userID = form.getvalue('user')
password   = form.getvalue('password')
StartingDate = form.getvalue('sdate')
EndingDate  = form.getvalue('edate')
ReportType  = form.getvalue('rtype')

userfile = "/home/net484/student/net484s02/public_html/hw05/user.data"
fd = open(userfile, "r")   # attach the data to the file
lines=fd.readlines()
try:
    print('<div style="width:800px; margin:0 auto;">')
    print('<h1>System Load Report</h1>')
    if ReportType=='1':
        reportstr='daily'
    elif ReportType=='2':
        reportstr='hourly'
    else:
        reportstr='raw'
    print('<p>user %s Report Type %s'%(userID,reportstr))
    report(ReportType,StartingDate,EndingDate)
    print('</div>')
except Exception as e:
    print('<p>Exception occured</p>')
    print(e)


print "</body>"
print "</html>"