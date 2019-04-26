#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree
from netaddr import *
import os
import sys
import re


bad_nets = [IPNetwork('127.0.0.0/24'), IPNetwork('10.0.0.0/8'),
	    IPNetwork('192.168.0.0/16'), IPNetwork('172.16.0.0/12')
]
bad_ips = ('0.0.0.0', '255.255.255.255')


def is_true_net(net, ip=1):
    try:
        if net in bad_ips:
            return 0
        nets = list(bad_nets)
        nets.append(IPNetwork(net))
        if len(cidr_merge(nets)) == 4:
            return 0
        return 1
    except:
        return 0


def get_xml(url):
    r = requests.get(url)
    return xml.etree.ElementTree.fromstring(r.text)


def to_net(xml):
    ips = []
    for content in xml:
        for node in content:
            if node.tag == "ip":
                if node.text:
                    ips += node.text.split(',')
    return ips


def merge_net(ips):
    ip_list = []
    for ip in ips:
        if is_true_net(ip):
            ip_list.append(IPNetwork(ip))
    return cidr_merge(ip_list)


def main():
    path = re.sub('parser.py$', '', sys.argv[0])
    os.chdir(path)
    xml = get_xml('http://api.antizapret.info/all.php?type=xml')
    nets = to_net(xml)
    nets = merge_net(nets)
    file = open('black_nets.list', 'w')
    for net in nets:
        file.write(str(net) + '\n')
    file.close()
    os.system("git add .")
    os.system("git commit -m \"`date`\"")
    os.system("git push")


if __name__ == "__main__":
    main()
