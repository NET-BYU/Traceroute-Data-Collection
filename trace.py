import sys
import scapy.all as scapy


def traceRoute(target):

    ans, unans = scapy.sr(scapy.IP(dst=target, ttl=(1,21),id=scapy.RandShort())/scapy.TCP(flags=0x2), timeout=.5)
    output = []
    for snd,rcv in ans:
        output.append(rcv.src)
    return output
