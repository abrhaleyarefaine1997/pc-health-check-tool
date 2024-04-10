#!/usr/bin/env python

import psutil
import socket
import smtplib
import ssl

# Define the thresholds for each aspect of the system
CPU_THRESHOLD = 80  # percentage of CPU usage
DISK_THRESHOLD = 20  # percentage of disk space
MEMORY_THRESHOLD = 500  # megabytes of available memory
NETWORK_HOST = "www.google.com"  # host to ping for network connectivity

# Define the email details
SENDER_EMAIL = "sender@example.com"  # email address of the sender
RECEIVER_EMAIL = "receiver@example.com"  # email address of the receiver
PASSWORD = "password"  # password of the sender's email account
SMTP_SERVER = "smtp.example.com"  # SMTP server of the sender's email provider
PORT = 465  # port number for SSL connection

# Define a function to send an email alert
def send_email(subject, message):
    # Create a secure SSL context
    context = ssl.create_default_context()
    # Connect to the SMTP server and login
    with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=context) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        # Create an email message
        email = f"Subject: {subject}\n\n{message}"
        # Send the email
        server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, email)

# Check the CPU usage
cpu_usage = psutil.cpu_percent()
# If the CPU usage exceeds the threshold, send an email alert
if cpu_usage > CPU_THRESHOLD:
    subject = f"Warning: CPU usage is {cpu_usage}%"
    message = f"Your CPU usage is {cpu_usage}%, which is higher than the threshold of {CPU_THRESHOLD}%. Please check your system and take necessary actions."
    send_email(subject, message)

# Check the disk space
disk_usage = psutil.disk_usage("/")
disk_free = disk_usage.free / disk_usage.total * 100
# If the disk space is below the threshold, send an email alert
if disk_free < DISK_THRESHOLD:
    subject = f"Warning: Disk space is {disk_free:.2f}%"
    message = f"Your disk space is {disk_free:.2f}%, which is lower than the threshold of {DISK_THRESHOLD}%. Please check your system and free up some space."
    send_email(subject, message)

# Check the memory
memory_usage = psutil.virtual_memory()
memory_available = memory_usage.available / (1024 ** 2)
# If the memory is below the threshold, send an email alert
if memory_available < MEMORY_THRESHOLD:
    subject = f"Warning: Memory is {memory_available:.2f} MB"
    message = f"Your available memory is {memory_available:.2f} MB, which is lower than the threshold of {MEMORY_THRESHOLD} MB. Please check your system and close some applications."
    send_email(subject, message)

# Check the network connectivity
try:
    # Create a socket object
    sock = socket.socket()
    # Set a timeout for the connection attempt
    sock.settimeout(1)
    # Attempt to connect to the specified host and port
    response_time = sock.connect_ex((NETWORK_HOST, 80))

    # If the response time is zero, the network is fine
    if response_time == 0:
        print(f"Network is fine. Response time: {response_time} ms")
    # If the response time is not zero, the network is slow
    else:
        subject = f"Warning: Network is slow. Response time: {response_time} ms"
        message = f"Your network is slow. The response time from {NETWORK_HOST} is {response_time} ms, which is higher than the normal range. Please check your network connection and speed."
        send_email(subject, message)
except socket.error as e:
    # If there is an error, the network is down
    subject = f"Warning: Network is down. Error: {e}"
    message = f"Your network is down. There is an error when trying to ping {NETWORK_HOST}: {e}. Please check your network connection and status."
    send_email(subject, message)
