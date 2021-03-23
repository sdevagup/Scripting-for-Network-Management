# /home/net484/student/net484s02/hw03/hw03script.py
#
#Author :Sai Devaguptapu
#Date:1/27/2021
#Desctiption :A script in Python to generate an intrusion report
#
#Usage:python hw03script.py <cr>
#
import re
import collections
def report():
    logfile=open('/var/log/secure.log')
    lines=logfile.readlines()
    ipcount={}
    for line in lines:
        match = re.search('(.*)(authentication failure)(.*)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', line)
        if match:
            ip=match.group(4)
            if ip not in ipcount:
                ipcount[ip]=1
            else:
                ipcount[ip]=ipcount[ip]+1
    print('{:>70}           {:<80}                 '.format('Intrusion IP Address','count'))
    filteredips=[]
    for ip,count in  ipcount.items():
        if count>20:
            filteredips.append((ip,count))
    ipcount = sorted(filteredips, key=lambda kv: kv[1],reverse=True)
    for ip in ipcount:
            print('{:>70}            {:<80}                      '.format(ip[0], ip[1]))



report()
