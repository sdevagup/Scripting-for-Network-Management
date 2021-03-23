#!/usr/bin/python

# Import modules for CGI handling
import cgi, cgitb

#  hw06 - configure an IP address on the interface serios0/0 of R4 (192.168.20.104)
#
#  syntax: python hw06script.py <host> <newip>
#
#  author:Sai Devaguptapu
#  date:02/17/2021
#
#************************************************************************
import telnetlib
print "Content-type:text/plain\n"

form   = cgi.FieldStorage()
router = form.getvalue('host')
#interface  = form.getvalue('interface')
newip = form.getvalue('newip')
mask = form.getvalue('netmask')

interface = "Serial0/0"   # must hard code the interface to avoid disaster
TIMEOUT = 3
password1 = "user"
password2 = "cisco"

# 1. create a telnet object
telnetObject=telnetlib.Telnet(router)
# 2. login/telnet to the router
telnetObject.read_until('Password:')
telnetObject.write(password1 +'\n')
# 3. enter into the privilege mode
telnetObject.write('enable\n')
telnetObject.write(password2 +'\n')
# 4. enter into the configuration mode
telnetObject.write('configure terminal\n')
# 5. enter into the interface configuration mode
telnetObject.write('interface '+interface +'\n')
# 6. set the new IP address
telnetObject.write('ip address '+ newip + ' '+mask +'\n')
# 7. exit
#    exit from the interface configruaiton mode
telnetObject.write('exit\n')
#    exit from the configuraiotn mode
telnetObject.write('exit\n')
#    exit from the privilege mode
telnetObject.write('exit\n')
print telnetObject.read_all()  # this line is required, but not sure why?
telnetObject.close()
print ('setting new ipaddress=%s on interface=%s on router=%s '%(newip,interface,router))
