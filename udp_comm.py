"""
Simple library for communication with the ground robot raspberry pi over udp

Maintainer: Daan de Graaf
"""
import socket
import struct
import time
import sys

UDP_PORT = 12000

udp_ip = None

def open_socket(ip):
    global udp_ip
    udp_ip = ip
    sock = socket.socket(socket.AF_INET, # Internet
                         socket.SOCK_DGRAM) # UDP
    return sock

def send_cmd(sock, t, x, y, psi):
    sock.sendto(struct.pack("=Bddd", t, x, y, psi), (udp_ip, UDP_PORT))
