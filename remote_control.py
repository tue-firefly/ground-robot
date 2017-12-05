"""
Script to receive commands from the base station (over UDP) and relay them to the arduino.
Also allows for Hardware-In-the-Loop simulation by returning the integrated velocities.

WARNING: This script does not currently work, it is very much a work in progress

Maintainer: Daan de Graaf
"""
import serial 
import socket
import struct

#initialize UDP
UDP_IP = "0.0.0.0"
UDP_PORT = 12000
sock = socket.socket(socket.AF_INET,
			socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
sec	= 1
usec	= 500000
timeval	= struct.pack('ll', sec, usec)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO,timeval)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1)

#Initialize USB interface with arduino
ser = serial.Serial('/dev/ttyACM0', 115200)
time.sleep(1)
while ser.inWaiting():
	print(ser.readline())
time.sleep(1)

tau = 0.1
tlast = time.time() - 2*tau
data = 0
inp = "a0d0b0e0c0f0n0t\r\n"
PORTX = 1205
PORTY = 1203
PORTPSI = 1204
PORTVX = 1206
PORTVY = 1207
PORTTIME = 1208
IP = '127.0.0.1'
tstart = time.time()

while True:
	try:
		data, addr = sock.recvfrom(24)
		(f_x, f_y, psi) = struct.unpack('=ddd', data)
		
		# Forward euler's method

		ser.write(struct.pack('=fff', (x, y, psi))
		ser.flush()



        ## Everything below this is old and obsolete


		IP 	= addr[0]
		message = str(data) + "\r\n"
		values = re.findall('\d+', message)
		values = list(map(int, values))
	except socket.error, msg:
		print('No message received')
	if time.time() - tlast > tau:
		fx = (float(values[0]) + float(values[7])/100) * (2 * values[1] - 1)
		fy = -(float(values[2]) + float(values[8])/100) * (2 * values[3] - 1)
		vx = vx + tau * (fx -5*vx)#what does the -5*vx mean? 
		vy = vy + tau * (fy -5*vy)#what does the -5*vy mean? 
		vpsi = math.pi/180 * (float(values[4]) + float(values[9])/100) * (2 * values[5] - 1)
		xmeas = xmeas + tau * vx
		ymeas = ymeas + tau * vy
		psimeas = psimeas + tau * vpsi
		tlast = time.time()
		vxout = 246.7 * (vx * math.cos(psimeas) + vy * math.sin(psimeas))
		vyout = 246.7 * (vx * (-math.sin(psimeas)) + vy * math.cos(psimeas))
		vpsiout = 180/3.1415 * vpsi
		if vxout < 0:
			xsign = 0
		else:
			xsign = 1
		if vyout < 0:
			ysign = 0
		else:
			ysign = 1
		if vpsiout < 0:
			psisign = 0
		else:
			psisign = 1
		inp = "a" + str(int(abs(vxout))) + "d" + str(int(xsign)) + "b" + str(int(abs(vyout))) + "e" + str(int(ysign)) + "c" + str(int(abs(vpsiout))) + "f" + str(int(psisign)) + "n" + str(int(1)) + "t\r\n"
		sock.sendto(str(round(xmeas*1000)), (IP, PORTX))
		sock.sendto(str(round(ymeas*1000)), (IP, PORTY))
		sock.sendto(str(round(psimeas*1000)), (IP, PORTPSI))
		sock.sendto(str(round(vx*1000)), (IP, PORTVX))
		sock.sendto(str(round(vy*1000)), (IP, PORTVY))
		sock.sendto(str(round((time.time()-tstart)*1000)), (IP, PORTTIME))
		ser.write(bytes(inp))
		ser.flush()
		print("fx: %.3f\nfy: %.3f\nvx: %.3f\nvy: %.3f\nvpsi: %.3f\nxmeas: %.3f\nymeas: %.3f\npsimeas: %.3f\n" % (fx, fy, vx,vy, vpsi, xmeas, ymeas, psimeas))

