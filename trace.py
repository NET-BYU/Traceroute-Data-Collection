import sys
import scapy.all as scapy

target = 'google.com'
if len(sys.argv) == 2:
    target = sys.argv[1]

ans, unans = scapy.sr(scapy.IP(dst=target, ttl=(1,21),id=scapy.RandShort())/scapy.TCP(flags=0x2), timeout=.5)
for snd,rcv in ans:
    with open('/home/carter/VS Studio/Trace IP Address/output.txt', 'a') as f:
        toAdd = '\n'
        if snd.ttl < 10:
            toAdd += '0' + str(snd.ttl)
        else:
            toAdd += str(snd.ttl)
        toAdd += ' ' + str(rcv.src)
        f.write(toAdd)