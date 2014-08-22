import requests
import re
from pymemcache.client import Client

# User defined variables
feedaddr = 'http://multiproxy.org/txt_all/proxy.txt'
feedID = 'multiproxy'
mkey = 'fetcher_multiproxyIP:feeddata'
killchain = 'unknown'

# No user modifications needed below.
client = Client(('localhost', 11211))
result = client.get(mkey)

if isinstance(result, str):
	splitlines = result.split('\n')
else:
	r = requests.get(feedaddr)
	client.set(mkey, r.content, expire=7200)
	splitlines = r.content.split('\n')

print('ipv4,feedID,killchain,description,port')

for x in splitlines:
	x = x.strip()
	if len(x) == 0: continue
	xlist = x.split(':')
	print("%s,%s,%s,%s,%s" % (xlist[0], feedID, killchain, 'Open proxy server',xlist[1]))
	
