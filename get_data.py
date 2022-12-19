from os import system
from yaml import safe_load

with open("servers.yaml") as f:
    config = safe_load(f)

hosts = config["servers"]

# system('scp "%s" "%s:%s"' % (localfile, remotehost, remotefile) )
# scp -r netlab@iot.kitras.dev:/home/netlab/Traceroute-Data-Collection/Outputs .

for host in hosts:
    system('scp -r netlab@"%s:"/home/netlab/Traceroute-Data-Collection/Outputs ./Outputs/"%s"' % (host, host))