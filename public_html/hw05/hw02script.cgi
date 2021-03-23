#!/bin/sh
#
# file: hw02script.cgi
echo "content-type: text/plain"
echo
IPList="140.192.40.4 192.168.1.16 100.1.1.17 192.168.2.17 192.168.20.104 10.1.1.10 10.1.1.20 10.1.1.30"
PacketSize="64 128 256 512 1024 1280 1472 3000" 

printf "IP Address\t Packet Size\t      RTT\t    SD\n"
for ip in $IPList
do
	for ss in $PacketSize
	do
		# use the full path so the program can run by apache (web service)
		DATA=""    
		DATA=`/usr/local/bin/supercmd ping -f -c 100 -s $ss $ip | fgrep rtt | cut -d" " -f4`
		# echo $DATA
		if test "$DATA" = "" 
		then
			echo "Message: fail to reach the target host: $ip"
			break
		else
			RTT=`echo $DATA | cut -d"/" -f2`
			VAR=`echo $DATA | cut -d"/" -f4`
			printf "%-15s\t %11d\t %8.3f %12.3f\n" $ip $ss $RTT $VAR
		fi
	done
	echo "------------------------------------------------------"
done

