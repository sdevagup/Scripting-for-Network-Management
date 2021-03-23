#!/usr/bin/python 
#**************************************************************
from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import cgi, cgitb
cgitb.enable()
import snmpwalk

#*********************************************************
#  main program
#*********************************************************
print "Content-type:text/html\n\n"
print "<html>"
print "<head>"
print "<title>Interface Table</title>"
print "</head>"
print "<body>"
print "<H1 align=center>Interface Table</H1>"

#---------------------------------------
# Get the input from the HTML FORM:
#---------------------------------------
form = cgi.FieldStorage()
if len(form.keys()) == 0:    # local testing
   host  = "192.168.1.101"
else:
   host = form.getvalue('host')

community = 'public'
cmdGen = cmdgen.CommandGenerator()    # create the object for SNMP API

#*******************************************
#  ifIndex (key is string) and (value is integer).  But they look the same
#*******************************************
oid1 = "1.3.6.1.2.1.2.2.1.1"         #ifIndex
ifTable = {}
ret = snmpwalk.snmpwalk(host, community, oid1, 0, ifTable)

#**************************************
#    interface description (ifDescr)
#**************************************
oid2 = "1.3.6.1.2.1.2.2.1.2"    # ifDescr
ifDescr = {}
ret = snmpwalk.snmpwalk(host, community, oid2, 0, ifDescr)

oid3 = "1.3.6.1.2.1.2.2.1.5"         # ifSpeed
ifSpeed = {}
ret = snmpwalk.snmpwalk(host, community, oid3, 0, ifSpeed)

oid4 = "1.3.6.1.2.1.2.2.1.6"         # ifPhysAddress
ifMACAddress = {}
ret = snmpwalk.snmpwalk(host, community, oid4, 2, ifMACAddress)

oid5 = "1.3.6.1.2.1.2.2.1.7"         # ifAdminStatus
ifAdminStatus = {}
ret = snmpwalk.snmpwalk(host, community, oid5, 0, ifAdminStatus)

oid6 = "1.3.6.1.2.1.2.2.1.8"         # ifOperStatus
ifOperStatus = {}
ret = snmpwalk.snmpwalk(host, community, oid6, 0, ifOperStatus)

#******************************************
# get the IP address information
#******************************************
oid7="1.3.6.1.2.1.4.20.1.2"	# ipAdEntIfIndex
ipIfIndex = {}
ret = snmpwalk.snmpwalk(host, community, oid7, 0, ipIfIndex)

oid8="1.3.6.1.2.1.4.20.1.1"	# IP Address (ipAdEntAddr)
tmpTbl8   = {}
ipAddress = {}
ret = snmpwalk.snmpwalk(host, community, oid8, 1, tmpTbl8)
for x in tmpTbl8:      # x is oid (string)
   if x in ipIfIndex:  # ipIfIndex[x] is integer (IfIndex)
      i = ipIfIndex[x]
      if i in ipAddress:
         ipAddress[i] = ipAddress[i] + "<br>" + tmpTbl8[x]
      else:
         ipAddress[i] = tmpTbl8[x]
   else:
      print "<H3>Program Assert (ipAdEntAddr): %s (%s) </H3>" % (x, tmpTbl8[x])

oid9="1.3.6.1.2.1.4.20.1.3"	# Network Mask
tmpTbl9 = {}
ipNetMask = {}
ret = snmpwalk.snmpwalk(host, community, oid9, 1, tmpTbl9)
for x in tmpTbl9:
   if x in ipIfIndex:
      i = ipIfIndex[x]
      if i in ipNetMask:
         ipNetMask[i] = ipNetMask[i] + "<br>" + tmpTbl9[x]
      else:
         ipNetMask[i] = tmpTbl9[x]
   else:
      print "<H3>Program Assert (ipAdEntNetMask): %s (%s) </H3>" % (x, tmpTbl9[x])


#*************************************************
#  show Interface table
#************************************************
print "<H2 align=center>Interface Table of host = %s</H2>\n" % host
print "<Table align=center border=2>"
print "<TH>ifIndex</TH>"
print "<TH>ifDescription</TH>"
print "<TH>ifSpeed</TH>"
print "<TH>MAC Address</TH>"
print "<TH>ifAdminStatus</TH>"
print "<TH>ifOperStatus</TH>"
print "<TH>IP Address</TH>"
print "<TH>Network Mask</TH>"

statusName = ('unknown', 'up', 'down', 'undefined (3)', 'undefined (4)', 'undefined (5)','undefined (6)')
for x, i in sorted(ifTable.items(), key=lambda x:(x[1], x[0])):
   i = ifTable[x]    # x is string and i is interger
   print "<TR>"
   print "<TD> %s (%d) </TD>" % (x, i)
   print "<TD> %s </TD>" % (ifDescr[x])
   print "<TD> %s </TD>" % (ifSpeed[x])
   print "<TD> %s </TD>" % (ifMACAddress[x])
   print "<TD align=center> %s </TD>" % ( statusName[ifAdminStatus[x]] )
   print "<TD align=center> %s </TD>" % ( statusName[ifOperStatus[x]] ) 
   if i in ipAddress:
      print "<TD> %s </TD>" % (ipAddress[i])
      print "<TD> %s </TD>" % (ipNetMask[i])
   else:
      print "<TD> none </TD>" 
      print "<TD> none </TD>"
   print "</TR>"
print "</Table>"


print "</body>"
print "</html>"
