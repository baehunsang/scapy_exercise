from scapy.all import *

send(IP(dst="1.2.3.4")/TCP(dport=502, options=[("MSS", 0)]))

p = Ether()/IP(dst="www.secdev.org")/TCP()
print(p.summary())

print(p.dst)  # first layer that has an src field, here Ether
print(p[IP].src)  # explicitly access the src field of the IP layer

# sprintf() is a useful method to display fields
print(p.sprintf("%Ether.src% > %Ether.dst%\n%IP.src% > %IP.dst%"))
print(p.sprintf("%TCP.flags% %TCP.dport%"))

pkts=[p for p in IP(ttl=(1,5))/ICMP()]
print(pkts)

p = sr1(IP(dst="8.8.8.8")/UDP()/DNS(qd=DNSQR()))
print(p[DNS].an)