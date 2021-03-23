#!/usr/bin/python
#
#  show the MIB object content

import cgi
from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import snmpwalk

#*********************************************************
#  main program
#*********************************************************
print "Content-type:text/html\n\n"
print "<html>"
print "<head>"
print "<title>System Information</title>"
print "</head>"
print "<body>"

#---------------------------------------
# Get the input from the HTML FORM:
#---------------------------------------
form     = cgi.FieldStorage()
if len(form.keys()) == 0:    # local testing
   host  = "192.168.1.4"
else:
   host = form.getvalue('host')
mibOID = '1.3.6.1.2.1.1'
community = 'public'
port = 161

snmpTable = {}
snmpwalk.snmpwalk(host, community, mibOID, 0, snmpTable)

print "<H1 align=center>NET384/484 System Information for host=%s</H1>" % (host)
print "<table align=center border=2>"
for oid in sorted(snmpTable.keys()):
   print "<TR>"
   print "<TD>%s</TD>" % (oid)
   print "<TD>%s</TD>" % ( snmpTable[oid] )
   print "</TR>"

print "</table>"
print "</body>"
print "</html>"
