#!/usr/bin/python
#
#  use Cisco Discovery Protocol (CDP) to identify neighbors
 
import os
import telnetlib
import cgi, cgitb
import sys

#*********************************************************
#  main program
#*********************************************************
print "Content-type:text/html\n\n"
print "<html>"
print "<head>"
print "<title>TDC384/484 hw06 - Telnet Exercise (CDP) </title>"
print "</head>"
print "<H2 align=center>TDC384/484 hw06 - Telnet Exercise (show cdp neighbor)</H2>"

form     = cgi.FieldStorage()
if len(form.keys()) == 0:    # local testing
   host  = "192.168.1.1"
else:
   host  = form.getvalue('host')
print "<center> Device=%s </center>" % (host)

username  = "user"
password1 = "user"
password2 = "cisco"

TIMEOUT = 3
tn = telnetlib.Telnet(host, timeout=TIMEOUT)

ret = tn.read_until("Username: ", TIMEOUT)
if ret.find('Username') > 0:    # that is "found"
   tn.write(username + "\n")
   tn.read_until("Password: ", TIMEOUT)
   tn.write(password1 + "\n")
elif ret.find('Password') > 0:    # that is "found"
   tn.write(password1 + "\n")
else:
   tn.write(password1 + "\n")     # this line is not needed

# enable: from user mode to privilege mode
tn.write("enable\n")
tn.read_until("Password:")
tn.write(password2+"\n")

tn.write("terminal length 0"+"\n")  # no limit for terminal length
tn.write("show cdp neighbor"+"\n")
tn.write("exit"+"\n")
result = tn.read_all()
tn.close()

print "<table align=center border=2>"
print "<th>Neighbor Device</th>"
print "<th>Remote Port</th>"
print "<th>Local Port</th>"
print "<th>Neighbor Platform</th>"


flag = 0
for line in result.split('\n'):
   items = line.split()
   if flag == 0 and line.startswith('Device'):
      flag = 1
      continue
   if flag == 1:
      l = len(line)
      if l > 72:
         device     = line[0:9]
         myport     = line[17:25]
         holdtime   = line[36:39]
         capability = line[49:52]
         platform   = line[58:67]
         remote     = line[68:(l-1)]  # the last char is EOL
         # print "%s %s %s %s %s %s" % (device, interface, holdtime, capability, platform, myport)
         print "<TR>"
         print "<TD> %s </TD>" % (device)
         print "<TD> %s </TD>" % (remote)
         print "<TD> %s </TD>" % (myport)
         print "<TD> %s </TD>" % (platform)
         print "</TR>"

print "</table>"
print "</body>"
print "</html>"
