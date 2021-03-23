#!/bin/bash
# /home/net484/student/net484s02/hw02
#
#Author :Sai Devaguptapu
#Date:1/20/2021
#Desctiption : Computing the round trip time (RTT) and standard deviation of RTT with various packet sizes
#
#Usage:hw02script.sh
#
check='100% packet loss' 
msg='error'
#prints the values of header file on the screen using the given format and start a new line
printf "IP_Address    Packet_Size       RTT             SD \n----------------------------------------------------------------------\n"
#defines loop to list Ip addresses of all the target machines
for ip in "140.192.40.4" "192.168.1.16" "100.1.1.17" "192.168.2.17" "192.168.20.104" "10.1.1.10" "10.1.1.20" "10.1.1.30"
        do
#defines loop to ping different packet sizes 
                for p_size in 64 128 256 512 1024 1280 1472 3000
                        do
# granting root previlages to use the flooding option and run the ping command to ping different packet sizes for each IP adress and send 100 ICMP messages for each run 
                                res=`supercmd ping -f -c 100 -s $p_size $ip`
# cheking if there has been any packet loss in the result or an error ,if there is any, then print fail to reach the target.
                                if [[ "$res" =~ ."$check". ]] || [[ "$res" =~ ."$msg". ]]; then
                                        printf "fail to reach the target \n"
                                        break
                                else
#If we can sucessfully ping the target machine then find for the rtt in a given string and print the preceeding word
                                        rtt=`echo $res | grep -oP '\w+(?= rtt)'`
#if we find any match for min/avg/max/mdev in the given string then print the succeeding word
                                        result=`echo $res | grep -oP '(?<=min/avg/max/mdev = )[^ ]*' | awk -F'[//]' '{print "\t" $2 ""}'`
# printing a formatted output showing the values of Ip address,Packet Size,RTT and SD
                                        printf "%-15s %-15s %-10s %-10s\n" "$ip" "$p_size" "$rtt" "$result"
                                fi
                        done
                        echo "----------------------------------------------------------------------"
        done
	