# -*- coding: utf-8 -*-

#IMPORT
import sys
import shodan
import censys
import re
import socket
from socket import error as socket_error
import os
import censys.ipv4
from censys.base import CensysException
import paramiko
#GLOBALS
path = os.path.abspath(os.path.dirname(sys.argv[0]))
user = "pi"
password = "raspberry"
def usage():
    print (""" ___       _  ___                     
| . \ ___ <_>| . \ ___  _ _  ___ ._ _ 
|   /| . \| ||   /<_> || | |/ ._>| ' |
|_\_\|  _/|_||_\_\<___||__/ \___.|_|_|
     |_|""")
    print ("""+------------------------------------------------------------+\n|                RpiRaven    author: m0ths3c                 |\n|------------------------------------------------------------|\n| Usage:                                                     |\n| 1. Gather host with shodan (api needed)                    |\n| 2. Gather host with censys.io (api needed)                 |\n| 3. scan for up host                                        |\n| 4. scan for vuln host                                      |\n+------------------------------------------------------------+""")
def shodan_research():
    apiShodan = open(path + "/apishodan.txt", "r").read()
    if apiShodan == "":
        print("[!]Shodan api not found")
        apiTyped = raw_input("[|]Please provide a new one:")
        with open(path + "/apishodan.txt", "wb") as api:
            api.write(apiTyped)
        api = shodan.Shodan(apiTyped)
    else:
        api = shodan.Shodan(apiShodan)
        try:
            print"[*]Please provide a valid query for the research"
            query = raw_input("[*]Suggested querys 'raspian-7 port:22'    :")
            results = api.search(query)
            with open(path + '/host.txt', "wb") as host:
                for service in results['matches']:
                    host.write(service['ip_str'] + ":" + str(service['port']))  # host.write(service['port']
                    host.write("\n")
        except KeyboardInterrupt:
            print("[*]See you space cowboy")
        except shodan.exception.APIError:
            print("[*]Please upgrade your plan or change api")
def censys_research():
    censysAPI = open(path + "/apicensys.txt", "r").read().splitlines()
    if censysAPI == []:
        print('[!]no censys api found, please insert a valid one')
        api_censys_uid = raw_input('[*]' + 'type here uid:')
        api_censys_scrt = raw_input('[*]' + 'type here secret:')
        with open(path + "/apicensys.txt", "wb") as api:
            api.write(api_censys_uid + "\n" + api_censys_scrt)
    else:
        uid = censysAPI[0]
        secret = censysAPI[1]
        query = raw_input("[-]Please provide a query:")
        try:
            for record in censys.ipv4.CensysIPv4(api_id=uid, api_secret=secret).search(query):
                ip = record['ip']
                port = record['protocols']
                port_raw = port[0]
                port = re.findall(r'\d+', port_raw)
                with open(path + '/host.txt',"a") as cen:
                    cen.write(ip +":" + str(port[0]))
                    cen.write("\n")
        except KeyboardInterrupt:
            pass
        except CensysException:
            pass


def up_scan():
    print"[+]Loading all host..."
    host = open(path+ "/host.txt", "r").read().splitlines()
    a = 0
    try:
        while a < len(host):
            global target_host
            global port
            pattern_1 = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
            pattern_2 = r'(\:).*'
            res = host[a]
            match1 = re.search(pattern_1, res)
            match2 = re.search(pattern_2, res)
            target_host = match1.group()
            port_raw = match2.group()
            port = port_raw[1:]
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.settimeout(5)
                client.connect((target_host, int(port)))
                client.send("GET /HTTP/1.1\r\nHost: google.com\r\n\r\n")
                response = client.recv(4096)
                x = True
            except socket_error:
                x = False
            except KeyboardInterrupt:
                print ("\n[---]exiting now[---]")
            if x == True:
                with open(path + '/upHost.txt', "a") as host_up:
                    host_up.write(target_host + ":" + port + "\n")
            elif x == False:
                pass

            a += 1
    except KeyboardInterrupt:
        print ("\n[---]exiting now[---]")
def vulnScan():
    from socket import error as socket_error
    i = 0
    host = open(path + "/upHost.txt").read().splitlines()
    ssh = paramiko.SSHClient()
    while i < len(host):
        pattern = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
        toParse = host[i]
        match = re.search(pattern, toParse)
        targetHost = match.group()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            sys.stdout.write("\r" + "[##]Checking " + targetHost+ "     ")
            sys.stdout.flush()
            ssh.connect(targetHost, username="pi", password="raspberry", timeout=5)
            with open(path + '/vuln_host.txt', 'a') as host_vuln:
                host_vuln.write(target_host)

        except paramiko.AuthenticationException:
            pass
        except paramiko.ssh_exception.NoValidConnectionsError:
            pass
        except socket_error:
            pass
        except paramiko.ssh_exception.SSHException:
            pass
        except:
            pass
        i += 1


def response():
    global usage
    usage_str = raw_input('\n[#]Select an option:')
    if str(usage_str) == "1":
        shodan_research()
        response()
    elif str(usage_str) == "2":
        censys_research()
        response()
    elif str(usage_str) =="3":
        up_scan()
    elif str(usage_str) =="4":
        vulnScan()
def main():
    try:
        usage()
        response()
    except KeyboardInterrupt:
        print("[*]See you space cowboy")
main()