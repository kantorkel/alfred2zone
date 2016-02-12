#!/usr/bin/env python3

import json
import sys
import re
from ipaddress import *
from time import time

ValidHostnameRegex = "^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$"
prefix = IPv6Network('2a03:2267::/64')

data = json.load(sys.stdin)["nodes"].values()

print("""$TTL 600  ; 10 minutes
@     IN SOA  srv01.hamburg.freifunk.net. hostmaster.hamburg.freifunk.net. (
          %i ; serial
          600        ; refresh (10min)
          30         ; retry (30s)
          3600       ; expire (1 hour)
          60         ; minimum (1 minute)
          )
          NS srv01.hamburg.freifunk.net.
          NS named.exosphere.de.
          NS ns.ohrensessel.net.
      """ % time())

HostnameRegex = re.compile(ValidHostnameRegex)

for e in data:
  node = e["nodeinfo"]
  try:
    hostname = node['hostname']
    if HostnameRegex.match(hostname) == None:
      continue

    address = None

    for a in node['network']['addresses']:
      a = IPv6Address(a)
      if a in prefix:
        address = a
        break

    if address:
      print("%s\tAAAA\t%s" % (hostname, address))
  except:
    pass
