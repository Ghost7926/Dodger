#!/bin/python3
import os
import subprocess
import sys


print(r"""

  _____            _                 
 |  __ \          | |                
 | |  | | ___   __| | __ _  ___ _ __ 
 | |  | |/ _ \ / _` |/ _` |/ _ \ '__|
 | |__| | (_) | (_| | (_| |  __/ |   
 |_____/ \___/ \__,_|\__, |\___|_|   
                      __/ |          
                     |___/           

""")
print("Version 1.2")
print("Created by Ryan 'Ghost' Voit")
print("\nThis program will change the hostname and the MAC address of your Kali Linux machine.")
print("Your terminal promt will not change unless you close and reopen it.")
print("This program is meant for educational purposes only!\n")


# Check if the user running the program is root
def check_if_root():
    if os.geteuid() != 0:
        print("This script must be run with as root.")
        sys.exit(1)

# check if the interface exists
def interface_exists(interface):
    try:
        subprocess.run(['ip', 'link', 'show', interface], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# change the hostname
def change_hostname(new_hostname):
    try:
        current_hostname = subprocess.check_output(['hostname']).decode().strip()

        # Set the new hostname using the 'hostnamectl' command
        subprocess.run(['hostnamectl', 'set-hostname', new_hostname], check=True)

        # Update the /etc/hosts file to reflect the new hostname
        with open("/etc/hosts", "r") as hosts_file:
            hosts = hosts_file.read()
            hosts = hosts.replace(current_hostname, new_hostname)

        with open("/etc/hosts", "w") as hosts_file:
            hosts_file.write(hosts)

        subprocess.run(['systemctl', 'restart', 'networking'], check=True)

        print("Hostname has been changed to", new_hostname)
    except Exception as e:
        print("An error occurred:", str(e))

def alter_mac(interface):
    try:
        # Use 'macchanger -r' to change the MAC address of the specified interface
        subprocess.run(['macchanger', '-r', interface], check=True)

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    
    check_if_root()

    new_hostname = input("Enter the new hostname: ")

    while True:
        interface = input("Enter the interface you want to change: ")

        if interface_exists(interface):
            break
        else:
            print("The specified interface does not exist. Please try again.")

    # Call the function to change the hostname and restart services
    change_hostname(new_hostname)
    alter_mac(interface)
