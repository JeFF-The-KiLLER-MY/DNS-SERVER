#!/usr/bin/env python3
from socketserver import UDPServer, BaseRequestHandler
from dnslib import DNSRecord, RR, QTYPE, A
import time

# -----------------------------
# Configuration
# -----------------------------
HOST = "0.0.0.0"   # listen on all interfaces
PORT = 5353       # high port so we don't need sudo
RESPONSE_IP = "127.0.0.1"  # IP to return for every query

# -----------------------------
# Logo Banner
# -----------------------------
LOGO = r"""
    _____            ________  ________        ________  __                        __    __  __  __        __        ________  _______  
   |     \          |        \|        \      |        \|  \                      |  \  /  \|  \|  \      |  \      |        \|       \ 
    \$$$$$  ______  | $$$$$$$$| $$$$$$$$       \$$$$$$$$| $$____    ______        | $$ /  $$ \$$| $$      | $$      | $$$$$$$$| $$$$$$$\
      | $$ /      \ | $$__    | $$__             | $$   | $$    \  /      \       | $$/  $$ |  \| $$      | $$      | $$__    | $$__| $$
 __   | $$|  $$$$$$\| $$  \   | $$  \            | $$   | $$$$$$$\|  $$$$$$\      | $$  $$  | $$| $$      | $$      | $$  \   | $$    $$
|  \  | $$| $$    $$| $$$$$   | $$$$$            | $$   | $$  | $$| $$    $$      | $$$$$\  | $$| $$      | $$      | $$$$$   | $$$$$$$\
| $$__| $$| $$$$$$$$| $$      | $$               | $$   | $$  | $$| $$$$$$$$      | $$ \$$\ | $$| $$_____ | $$_____ | $$_____ | $$  | $$
 \$$    $$ \$$     \| $$      | $$               | $$   | $$  | $$ \$$     \      | $$  \$$\| $$| $$     \| $$     \| $$     \| $$  | $$
  \$$$$$$   \$$$$$$$ \$$       \$$                \$$    \$$   \$$  \$$$$$$$       \$$   \$$ \$$ \$$$$$$$$ \$$$$$$$$ \$$$$$$$$ \$$   \$$
"""

class DNSHandler(BaseRequestHandler):
    def handle(self):
        data, sock = self.request
        request = DNSRecord.parse(data)
        print(f"[{time.strftime('%H:%M:%S')}] Query for {request.q.qname}")
        reply = request.reply()
        reply.add_answer(RR(
            rname=request.q.qname,
            rtype=QTYPE.A,
            rclass=1,
            ttl=60,
            rdata=A(RESPONSE_IP)
        ))
        sock.sendto(reply.pack(), self.client_address)

if __name__ == "__main__":
    print(LOGO)
    print(f"Starting DNS server on {HOST}:{PORT}, answering with {RESPONSE_IP}")
    with UDPServer((HOST, PORT), DNSHandler) as server:
        server.serve_forever()


