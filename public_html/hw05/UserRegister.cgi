#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb 

print "Content-type:text/html\n"
print "<html>"
print "<head>"
print "<title>Registration Confirmation</title>"
print "</head>"
print "<body>"
print "<H1>User Registration Confirmation</H1>"

#**************************************************
# Get data from fields, use cgi.FieldStorage to create the form object
#**************************************************
# Create instance of FieldStorage 
form   = cgi.FieldStorage() 
userID = form.getvalue('user')
password   = form.getvalue('password')
usertype = form.getvalue('utype')
course  = form.getvalue('course')
print "<h2>%s registred</h2>" % (userID)

buffer = "%s;%s;%s;%s\n" % (userID,password,usertype,course)
userfile = "/home/net484/student/net484s02/public_html/hw05/user.data"
fd = open(userfile, "a")   # attach the data to the file
fd.write(buffer)

print "</body>"
print "</html>"

