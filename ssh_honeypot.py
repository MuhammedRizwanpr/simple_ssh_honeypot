import socket
from scapy.all import Ether,ARP,srp 
from datetime import datetime
import sys
import pandas as pd

host = "0.0.0.0"
port =  22
try:
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host,port))
    server.listen(1)
except PermissionError as e:
    print("USE SUDO")
    sys.exit()
except (OSError,TimeoutError) as e:
    print("IP addrees is worng/unreachble.....")
    sys.exit()

print("server start....")

client,addr = server.accept()

connect_time = datetime.now()
ip = addr[0]
port = addr[1]

server.close()

try :
    response = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip),timeout=1,verbose=0)[0]
except:
    print("ARP packet have some issuse..!")
    sys.exit()
sent_pkt,received_pkt = response[0]
attacker_mac = received_pkt.hwsrc

with open(f"/home/rizwan/Documents/scripts/honeypot/ssh_honeypot-{connect_time}.csv","w") as f:
    f.write("Tittle            :       Data        ")
    f.write(f"\nTime of attacker connect to the socket : {connect_time}")
    f.write(f"\nAttacker ip address : {ip}")
    f.write(f"\nAttacker ARP packet : {str(attacker_mac)}")

df = pd.read_csv(f"/home/rizwan/Documents/scripts/honeypot/ssh_honeypot-{connect_time}.csv")
print(df)