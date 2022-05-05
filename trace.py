import os
import scapy.all as scapy


def traceRoute(target):

    ans, unans = scapy.sr(scapy.IP(dst=target, ttl=(1,21),id=scapy.RandShort())/scapy.TCP(flags=0x2), timeout=.5)
    output = []
    for snd,rcv in ans:
        output.append(rcv.src)
    return output


def GetTTL(ip):
  result = os.popen("ping -c 1 "+ip).read()
  n = result.find("ttl=")
  if n >= 0:
    ttl = result[n+4:]
    n = ttl.find(" ")
    if n > 0:
      return int(ttl[:n])
  return -1
