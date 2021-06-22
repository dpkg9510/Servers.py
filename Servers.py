import subprocess
import csv
import os
import smtplib
from email.message import EmailMessage

# Ping the servers and define the results.
def ping(hostname):
    p = subprocess.Popen('ping ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    pingStatus = 'ok';
        
    for line in p.stdout:
        output = line.rstrip().decode('UTF-8')
 
        if (output.endswith('unreachable.')) :
            pingStatus = 'unreacheable'
            break
        elif (output.startswith('Ping request could not find host')) :
            pingStatus = 'host_not_found'
            break
        if (output.startswith('Request timed out.')) :
            pingStatus = 'timed_out'
            break
    
    return pingStatus

# Check if old output files are available and delete them. 
if os.path.exists('!ok.txt'):
    os.remove('!ok.txt')
if os.path.exists('./!timed_out.txt'):
    os.remove('./!timed_out.txt')  
if os.path.exists('./!unreachable.txt'):
    os.remove('./!unreachable.txt')
if os.path.exists('./!server-not-found.txt'):
    os.remove('./!server-not-found.txt')

# Write the results to the files.
def printPingResult(hostname):
    statusOfPing = ping(hostname)
    
    if (statusOfPing == 'host_not_found') :
        writeToFile('./!server-not-found.txt', hostname)
    elif (statusOfPing == 'unreacheable') :
        writeToFile('./!unreachable.txt', hostname)
    elif (statusOfPing == 'timed_out') :
        writeToFile('./!timed_out.txt', hostname)	   
    elif (statusOfPing == 'ok') :
        writeToFile('./!ok.txt', hostname)

def writeToFile(filename, data) :
    with open(filename, 'a') as output:
        output.write(data + '\n') 

# Get the information from the txt files, examples: 10.0.10.100, www.google.com. each as entry at every line in the txt file.
file = open('./servers.txt')

try:
    reader = csv.reader(file)
    
    for item in reader:
        printPingResult(item[0].strip())
finally:
    file.close()

# Count the outputs.
class finalStatus:
   def __init__(self, onlineCount, offlineCount):
        self.onlineCount = onlineCount
        self.offlineCount = offlineCount

file = open('./!ok.txt', 'r')

line_count = 0

for line in file:

    if line != "\n":

        line_count += 1
        onlineCount = line_count

file.close()

file = open('./!timed_out.txt', 'r')

line_count = 0

for line in file:

    if line != "\n":

        line_count += 1
        offlineCount = line_count

file.close()

# Send the outputs to email.
host = "SMTP server"
server = smtplib.SMTP(host)
msg = EmailMessage()
msg.set_content("Online Servers: " + str(onlineCount) + " \nOffline Servers: " + str(offlineCount) + " \nTotal Servers: " + str(onlineCount+offlineCount))
msg["Subject"] = "An Email Alert"
msg["From"] = "SENDER EMAIL"
msg["To"] = "RECEIVER EMAIL"

server.send_message(msg)
server.quit()
