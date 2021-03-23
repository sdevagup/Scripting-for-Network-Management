#!/usr/bin/python
import cgi, cgitb

# ****************************************************
#     getMACTable.py
#
#     Description: get the MAC table from remote host
#     Date: 02/23/2021
#     Author: Sai Devaguptapu

#     local Python module: snmpwalk
# ***************************************************

from pysnmp.entity.rfc3413.oneliner import cmdgen
import snmpwalk
import sys

print("Content-type:text/html\n")
print("<html>")
print("<head>")
print("<title>MAC Table</title>")
print("</head>")
print("<body>")

form = cgi.FieldStorage()
host = form.getvalue('host')
vlan = form.getvalue('vlan')

# *********************************************************
#  main program
# *********************************************************
community = 'public' + '@' + vlan

cmdGen = cmdgen.CommandGenerator()  # create the object for SNMP API

oid1 = '1.3.6.1.2.1.17.4.3.1.1'    # MAC address in the MAC forwarding table
oid2 = '1.3.6.1.2.1.17.4.3.1.2'    # Interface (ifIndex) in the MAC forwarding table

tbl1 = {}
snmpwalk.snmpwalk(host, community, oid1, 2, tbl1)
tbl2 = {}
snmpwalk.snmpwalk(host, community, oid2, 0, tbl2)

# **********************************************
#   complete reading SNMP data
#   print the ARP table
# *********************************************
print('<div style="width:800px; margin:0 auto;">')
print('<h1>MAC ADDRESS TABLE</h1>')
print('<table border=2>')
print('<tr> <TH>MIB OID</TH><TH>Interface</TH><TH>MAC Address</TH></tr>')
for x in tbl1:
   print ('<tr> <td>%20s</td> <td>FastEthernet0/%s</td> <td>%20s</td> </tr>' % (x, tbl2[x], tbl1[x]))
print("</table>")
print('</div>')
print("</body>")
print("</html>")