#!/usr/bin/python
import cgi, cgitb

#****************************************************
#     getARPTable.py 
#	usage: python getARPTable.py <host>
#
#     Description: get the ARP table from remote host
#     Date: 12/02/2016
#     Author: James Yu

#     local Python module: snmpwalk
#***************************************************

from pysnmp.entity.rfc3413.oneliner import cmdgen
import snmpwalk
import sys
print ("Content-type:text/html\n")
print ("<html>")
print ("<head>")
print ("<title>ARP Table</title>")
print ("</head>")
print ("<body>")

form   = cgi.FieldStorage()
host= form.getvalue('host')

#*********************************************************
#  main program
#*********************************************************
community = 'public'

cmdGen = cmdgen.CommandGenerator()    # create the object for SNMP API

#**************************************
#    interface index
#**************************************
oid1 = "1.3.6.1.2.1.2.2.1.1"   	
n1 = len(oid1)
ifTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oid1, 0, ifTable)

#**************************************
#    interface description (ifDescr)
#**************************************
oid2 = "1.3.6.1.2.1.2.2.1.2"	# ifDescr
tmpTbl = {}
ifDescrTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oid2, 0, tmpTbl)
for x in tmpTbl:
   if x in ifTable:
      ifDescrTable[ifTable[x]] = tmpTbl[x]  # key: ifIndex   val: ifDescr
     
#**************************************
#    ARP interface index 
#**************************************
oid3 = "1.3.6.1.2.1.4.22.1.1"   # ifIndex
arpIfTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oid3, 0, arpIfTable)

#**************************************
#    ARP IP address
#**************************************
oid4 = "1.3.6.1.2.1.4.22.1.3"	# IP address
arpIPTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oid4, 1, arpIPTable)

#**************************************
#    ARP MAC address
#**************************************
oid5 = "1.3.6.1.2.1.4.22.1.2"	# MAC address
arpMACTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oid5, 2, arpMACTable)

#**********************************************
#   complete reading SNMP data
#   print the ARP table
#*********************************************
print('<div style="width:800px; margin:0 auto;">')
print('<h1>ARP TABLE</h1>')
print ('<table border=2>')
print ('<tr> <TH>MIB OID</TH><TH>Interface</TH><TH>IP Address</TH><TH>MAC Address</TH></tr>')
for i in arpIfTable:
   if arpIfTable[i] in ifDescrTable:
      ifName = ifDescrTable[ arpIfTable[i] ]
   else:
      ifName = "N/A(%d)" % arpIfTable[i]
   print ("<tr> <td>%20s</td> <td>%12s</td>  <td>%15s</td>  <td>%20s</td> </tr>" % (i, ifName, arpIPTable[i], arpMACTable[i]))


print ("</table>")
print('</div>')
print ("</body>")
print ("</html>")