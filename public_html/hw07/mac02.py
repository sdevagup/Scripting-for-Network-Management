#!/usr/bin/python
#******************************************88
#   get raw data for MAC address table
#****************************************************

from pysnmp.entity.rfc3413.oneliner import cmdgen
import sys
import snmpwalk

#**************************************************************
# main program
#*************************************************************
if (len(sys.argv) != 3):
   print "syntax: python %s <host> <valn>" % (sys.argv[0])
   sys.exit()

host = sys.argv[1]
vlan = sys.argv[2]    # this is a string
community = 'public' + '@' + vlan
cmdGen = cmdgen.CommandGenerator()

oid1 = '1.3.6.1.2.1.17.4.3.1.1'    # MAC address in the MAC forwarding table
oid2 = '1.3.6.1.2.1.17.4.3.1.2'    # Interface (ifIndex) in the MAC forwarding table

tbl1 = {}
snmpwalk.snmpwalk(host, community, oid1, 2, tbl1)
tbl2 = {}
snmpwalk.snmpwalk(host, community, oid2, 0, tbl2)
for x in tbl1:
   print 'MIB OID=%s    MAC Address=%s   IfIndex=%s' % (x, tbl1[x], tbl2[x])
