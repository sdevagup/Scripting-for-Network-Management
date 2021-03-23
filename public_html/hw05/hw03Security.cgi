#!/usr/bin/python
import cgi
import pygeoip
print "Content-type:text/plain\n"
def hw03current():
    fd = open('/var/log/secure.log')  # default is open for read
    syslog = fd.readlines()

    countTable = {}  # initialization of a dictionary
    for line in syslog:
        data = line.split()
        items = len(data)
        if (items > 14):
            # print data[6], data[7], data[14]
            if ((data[6] == 'authentication') and (data[7] == 'failure;') and (data[14] == 'user=root')):
                [tmp, rhost] = data[13].split('=')
                if (rhost in countTable):
                    countTable[rhost] += 1
                else:
                    countTable[rhost] = 1  # create a new entry in the dictionary table

    print("%48s  %5s" % ("Intrusion IP Address", "Count"))
    print("-----------------------------------------------------------")
    # ****************************************
    #   sort by value in descending order
    # *****************************************
    for ip, count in sorted(countTable.items(), key=lambda x: (-x[1], x[0])):
        if count > 19:
            print("%48s  %5d" % (ip, count))


def hw03modified():
    fd = open('/var/log/secure.log')  # default is open for read
    syslog = fd.readlines()

    countTable = {}  # initialization of a dictionary
    for line in syslog:
        data = line.split()
        items = len(data)
        if (items > 14):
            # print data[6], data[7], data[14]
            if ((data[6] == 'authentication') and (data[7] == 'failure;') and (data[14] == 'user=root')):
                [tmp, rhost] = data[13].split('=')
                if (rhost in countTable):
                    countTable[rhost] += 1
                else:
                    countTable[rhost] = 1  # create a new entry in the dictionary table

    print("%20s  %5s %-15s  %-3s" % ("Intrusion IP Address", "Count", "City", "Country"))
    print("-------------------------------------------------------")
    # ****************************************
    #   sort by value in descending order
    # *****************************************
    gi = pygeoip.GeoIP('/usr/local/share/GeoIP/GeoLiteCity.dat')
    for ip, count in sorted(countTable.items(), key=lambda x: (-x[1], x[0])):
        if count > 20:
            x = gi.record_by_addr(ip)
            if x is None:
                print("%20s  %5d" % (ip, count))
            else:

                print("%20s  %5d %-15s %3s" % (ip, count, x['city'], x['country_code']))

query =cgi.FieldStorage()
option=query["option"].value
if option =='current':
    hw03current()
else:
    hw03modified()
