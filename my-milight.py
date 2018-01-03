import socket
import sys
import time
import binascii
import argparse
 
HOST = ''   # Symbolic name meaning all available interfaces
PORT = 5987 # Arbitrary non-privileged port
BRIDGE ='192.168.88.25' # Change here for your local milight hub address

parser = argparse.ArgumentParser(description='A simple easy-to-integrate with ha-bridge - and therefore Google home & Amazon eco - milight v6 bridge controller python script')
parser.add_argument('-c','--cmd', help='ON,OFF,BRI,SAT,COLOR,WHITE', required=True)
parser.add_argument('-b','--brightness', help='Value of brightess percent', required=False)
parser.add_argument('-s','--saturation', help='Value of saturation percent', required=False)
parser.add_argument('-o','--color', help='Value of color', required=False)
parser.add_argument('-z','--zone', help='Value of zone (1,2,3,4, 0 means all, 5 means bridge)', required=True)

args = vars(parser.parse_args())

if args['cmd'] == 'ON':
    if args['zone'] == '5':
        cmd = bytearray([0x31, 0x00, 0x00, 0x00, 0x03, 0x03, 0x00, 0x00, 0x00])
    else:
        cmd = bytearray([0x31, 0x00, 0x00, 0x08, 0x04, 0x01, 0x00, 0x00, 0x00])
    
if args['cmd'] == 'OFF':
    if args['zone'] == '5':
        cmd = bytearray([0x31, 0x00, 0x00, 0x00, 0x03, 0x04, 0x00, 0x00, 0x00])
    else:
        cmd = bytearray([0x31, 0x00, 0x00, 0x08, 0x04, 0x02, 0x00, 0x00, 0x00])
    
if args['cmd'] == 'BRI':
    if args['zone'] == '5':
        mybri = bytes(bytearray([int(args['brightness'])]))
        cmd = bytearray([0x31, 0x00, 0x00, 0x00, 0x02])
        cmd =cmd+mybri+bytearray([0x00, 0x00, 0x00])
    else:
        mybri = bytes(bytearray([int(args['brightness'])]))
        cmd = bytearray([0x31, 0x00, 0x00, 0x08, 0x03])
        cmd =cmd+mybri+bytearray([0x00, 0x00, 0x00])

if args['cmd'] == 'SAT':
    if args['zone'] == '5':
        mysat = bytes(bytearray([int(args['saturation'])]))
        cmd = bytearray([0x31, 0x00, 0x00, 0x00, 0x02])
        cmd =cmd+mysat+bytearray([0x00, 0x00, 0x00])
    else:
        mysat = bytes(bytearray([int(args['saturation'])]))
        cmd = bytearray([0x31, 0x00, 0x00, 0x08, 0x02])
        cmd =cmd+mysat+bytearray([0x00, 0x00, 0x00])
            
if args['cmd'] == 'COLOR':
    if args['zone'] == '5':
        mycol = bytes(bytearray([int(args['color'])]))
        cmd = bytearray([0x31, 0x00, 0x00, 0x00, 0x01])
        cmd =cmd+mycol+mycol+mycol+mycol
    else:
        mycol = bytes(bytearray([int(args['color'])]))
        cmd = bytearray([0x31, 0x00, 0x00, 0x08, 0x01])
        cmd =cmd+mycol+mycol+mycol+mycol

if args['cmd'] == 'WHITE':
    if args['zone'] == '5':
        cmd = bytearray([0x31, 0x00, 0x00, 0x00, 0x03, 0x05, 0x00, 0x00, 0x00])
    else:
        cmd = bytearray([0x31, 0x00, 0x00, 0x08, 0x05, 0x64, 0x00, 0x00, 0x00])

if args['zone'] == '5':
        myzone = bytes(bytearray([int('1')]))
else:
        myzone = bytes(bytearray([int(args['zone'])]))

# Datagram (udp) socket
try :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg :
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
 
 
# Bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error , msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()
     
print 'Socket bind complete'
 
firstmsg = bytearray([0x20,0x00, 0x00, 0x00, 0x16, 0x02, 0x62, 0x3A, 0xD5, 0xED, 0xA3, 0x01, 0xAE, 0x08, 0x2D, 0x46, 0x61, 0x41, 0xA7, 0xF6, 0xDC, 0xAF, 0xD3, 0xE6, 0x00, 0x00, 0x1E])
s.sendto(firstmsg, (BRIDGE, PORT))

#time.sleep(1)

#now keep talking with the client
q=1
while q:
    # receive data from client (data, addr)
    d = s.recvfrom(1024)
    data = d[0]
    addr = d[1]
     
    if not data: 
        break
     
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + binascii.hexlify(bytearray(data))

    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - Bridgesession1 ' + binascii.hexlify(bytearray(data[19]))
    print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - Bridgesession2 ' + binascii.hexlify(bytearray(data[20]))
    
    #80 00 00 00 11 {WifiBridgeSessionID1} {WifiBridgeSessionID2} 00 {SequenceNumber} 00 {COMMAND} {ZONE NUMBER} 00 {Checksum}
    
    secmsg = bytearray([0x80, 0x00, 0x00, 0x00, 0x11])
    secmsg+=data[19]
    secmsg+=data[20]
    secmsg+=bytearray([0x00, 0x01, 0x00])
    secmsg=secmsg+cmd+myzone
    secmsg+=bytearray([0x00])
    tochksum=cmd+myzone+bytearray([0x00])
    chksum=0
    for b in tochksum:
        chksum += b
    chksum = chksum & 0xff
    secmsg+=bytes(bytearray([chksum]))
    print 'Secmsg - ' + binascii.hexlify(bytearray(secmsg))
    q=0
    
s.sendto(secmsg, (BRIDGE, PORT))
s.close()
