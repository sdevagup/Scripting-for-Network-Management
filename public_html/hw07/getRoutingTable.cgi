#!/usr/bin/python
import cgi, cgitb
#****************************************************
#     getRoutingTable.py 
#	usage: python getRoutingTable.py <host> <vlan>
#
#     Description: get the IP Routing table from remote host/router
#     Date: 2/10/2020
#     Author: Anthony Chung (after a script by James Yu)
#***************************************************

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import snmpwalk

print ("Content-type:text/html\n")
print ("<html>")
print ("<head>")
print ("<title>IPRouting Table</title>")
print ("</head>")
print ("<body>")

form   = cgi.FieldStorage()
host= form.getvalue('host')

RouteTypeList = ('unknown', 'other', 'valid', 'direct', 'indirect', 'undefined')   # use tupple
RouteProtoList =('unknow', 'other', 'local', 'netmgmt', 'icmp', 'egp', 'ggp', 'hello', 'rip', 'is-is', 'es-is', 'igrp', 'bbn', 'ospf', 'bgp', 'undefined') 

#*********************************************************
#  main program
#*********************************************************
community = 'public' 

#**************************************
#    interface index
#**************************************
oidx = "1.3.6.1.2.1.2.2.1.1"   	
ifTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oidx, 0, ifTable)

#**************************************
#    interface description (ifDescr)
#**************************************
oidy = "1.3.6.1.2.1.2.2.1.2"	# ifDescr
tmpTbl = {}
ifDescrTable = {}
snmpResult = snmpwalk.snmpwalk(host, community, oidy, 0, tmpTbl)
for x in tmpTbl:
   if x in ifTable:
      ifDescrTable[ifTable[x]] = tmpTbl[x]  # key: ifIndex   val: ifDescr
     
#**************************************
#    ipRouteDest 
#**************************************
oid1 = "1.3.6.1.2.1.4.21.1.1"
ipRouteDest = {}
snmpwalk.snmpwalk(host, community, oid1, 1, ipRouteDest)

#**************************************
#    ipRouteIf 
#**************************************
oid2 = "1.3.6.1.2.1.4.21.1.2"
tmpTbl = {}
ipRouteIfTbl = {}
snmpwalk.snmpwalk(host, community, oid2, 0, tmpTbl)
for x in tmpTbl:
   y = tmpTbl[x]

   if y == 0:
      ipRouteTbl[x] = 'default'		
   elif y in ifDescrTable:
      ipRouteIfTbl[x] = ifDescrTable[y]
   else:
      print ("Progrma Assert: unknown routeIfIndex=", y)

#**************************************
#    ipRouteNextHop 
#**************************************
oid7 = "1.3.6.1.2.1.4.21.1.7"
ipRouteNextHop = {}
snmpwalk.snmpwalk(host, community, oid7, 1, ipRouteNextHop)

#**************************************
#    ipRouteType 
#**************************************
oid8 = "1.3.6.1.2.1.4.21.1.8"
ipRouteType = {}
snmpwalk.snmpwalk(host, community, oid8, 0, ipRouteType)

oid9 = "1.3.6.1.2.1.4.21.1.9"
ipRouteProto = {}
snmpwalk.snmpwalk(host, community, oid9, 0, ipRouteProto)

oid11 = "1.3.6.1.2.1.4.21.1.11"
ipRouteMask = {}
snmpwalk.snmpwalk(host, community, oid11, 1, ipRouteMask)

#**********************************************
#   complete reading SNMP data
#   print the routing table
#*********************************************
print('<div style="width:800px; margin:0 auto;">')
print('<h1>IPRouting TABLE</h1>')
print ('<table border=2>')

print ("<tr> <TH>%16s</TH>  <TH>%16s</TH>  <TH>%16s</TH>  <TH>%16s</TH>  <TH>%12s</TH> <TH>%16s</TH>  <TH>%18s</TH></tr>\n" % ('MIB OID', 'Route Destination', 'NextHop(Gateway)', 'Interface', 'Route Type', 'Route Protocol', 'Network Mask'))
for i in ipRouteDest:
   rtype  = RouteTypeList[ ipRouteType[i] ]
   rproto = RouteProtoList[ ipRouteProto[i] ]
   print ("<tr> <td>%16s</td> <td>%16s</td>  <td>%16s</td> <td>%16s</td> <td>%9s(%d)</td> <td>%12s(%2d)</td> <td>%18s</td></tr>" % (i, ipRouteDest[i], ipRouteNextHop[i], ipRouteIfTbl[i], rtype, ipRouteType[i], rproto, ipRouteProto[i], ipRouteMask[i]))


print ("</table>")
print('</div>')
print ("</body>")
print ("</html>")