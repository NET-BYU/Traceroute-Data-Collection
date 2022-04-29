import sys
import scapy.all as scapy

target = 'google.com'
if len(sys.argv) == 2:
    target = sys.argv[1]

ans, unans = scapy.sr(scapy.IP(dst=target, ttl=(1,30),id=scapy.RandShort())/scapy.TCP(flags=0x2), timeout=3)
for snd,rcv in ans:
    print(snd.ttl, rcv.src, isinstance(rcv.payload, scapy.TCP))