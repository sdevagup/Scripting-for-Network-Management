# /home/net484/student/net484s02/hw04/hw04script.py
#
#Author :Sai Devaguptapu
#Date:02/02/2021
#Desctiption : Python script to analyze Multiple Linux syslog files
#
#Usage:python hw04script.py <cr>
from os import listdir
from os.path import isfile, join
from datetime import datetime
from datetime import date
#def to get person id from from the list of lines
def get_pid_from_line(line):
    n1 = line.index('[')
    n2 = line.index(']')
    pid = line[n1 + 1:n2]
    return pid
#def to get date from the list of lines
def get_date_from_line(line):
    n1 = 0
    n2 = line.index(' linux05')
    time = line[n1:n2]
    #formatting the date and time
    format = '%b %d %H:%M:%S'
    time = datetime.strptime(time, format)
    return time

#Defining a funtion
def analyze_login(file_name,total_times,user_counts):
    #open the syslog.txt file
    syslog_data = open(file_name)
    #reads all the lines from syslog_data
    lines = syslog_data.readlines()
    #using the open_times dictonary created above get the open times
    open_times={}
    for line in lines:
        try:
            if 'session opened' in line:
                #if we find session opened in the line then get the person id and open time
                pid =get_pid_from_line(line)
                open_time =get_date_from_line(line)
                open_times[pid]=open_time
                #else if the session closed is found then get the person id,close time and opentime from functions defined above
            elif 'session closed' in line:
                pid = get_pid_from_line(line)
                close_time =get_date_from_line(line)
                open_time =open_times[pid]
                # calucalting duration for open and close sessions
                duration = (close_time - open_time).total_seconds()
                n1 = line.index('for user')
                user_name =line[n1+9:-1 ]
                if user_name in total_times:
                    total_time_prv=total_times[user_name]
                else:
                    total_time_prv=0
                total_times[user_name]=total_time_prv + duration
                #get the previous count of the user
                if user_name in user_counts:
                    count= user_counts[user_name]
                #add one to the previous count
                else:
                    count=0
                count=count+1
                #store the updated count
                user_counts[user_name]=count
        except ValueError:
            pass
        except KeyError:
            pass
def print_report(total_times,user_counts):
    print('{:<15} {:<10} {:<15} {:<15}' .format('Account' ,'Count' ,'Total Time'  ,'Average'))
    for user_name in sorted(user_counts.keys()):
        print('{:<15} {:<10} {:<15} {:<15}' .format(user_name ,user_counts[user_name] ,total_times[user_name] ,total_times[user_name]/user_counts[user_name]) )






#analyze_login('secure.log.1')
def analyze_secure_log_files():
    path="/var/log/"
    user_counts={}
    total_times={}
    for file in listdir(path):
        filepath=join(path, file)
        if isfile(filepath) and file.startswith('secure.log'):
            analyze_login(filepath,total_times,user_counts)
    print_report(total_times,user_counts)
analyze_secure_log_files()




