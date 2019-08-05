# RpiRaven
* 1 . scan for raspberry pis over the internet with the technology of censys or shodan
* 2 . scan for on-LAN raspberry pis
* 3 . exploit them using default password
# Introduction
Rpi raven is a python tool that make you able to scan over the internet for Rpis and then try to connect to them with the default credential.
This tool is not intended to harm anyone or any raspberry, it's a simple tool that should make people realize that there are a lot of "ridiculous easy" vulnerable machines and that is not right, a lot of them could be used in some major attack like mirai.
# Installation
```bash
pip install shodan
pip install censys
pip install paramiko      or        apt-get install python-paramiko (should also work on debian)
```
# Usage
1. Gather host with shodan (api needed)                    
2. Gather host with censys.io (api needed)                 
3. scan for up host                                        
4. scan for vuln host

The tool is pretty simple, reduced to the minimu user interaction with the tool.
You will 4 options, the first two are intended to gather hosts from the web using shodan or censys.
The third one is to actually verify that the host are really up
The fourth one is to try to connect to them using default credentials

In order to make your tool work you have to get the censys.io and shodan api keys or the tool wont work
# Suggested querys
In order to gather hosts you will be asked to enter a query for shodan on censys.io
you could use your own query working with your account
The one and most easy that i suggest you are
```
raspbian-7
raspbian-8
```
if you have a plan with shodan or censys you could use search filters such as "port:22" or what you want, it's totally up.



legal disclaimer: Usage of hikxploit for attacking targets without prior mutual consent is illegal. It is the end user's responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this program

