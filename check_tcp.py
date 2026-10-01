import socket

for host in ["localhost", "127.0.0.1", "::1"]:
    for family, _, _, _, addr in socket.getaddrinfo(host, 5432, type=socket.SOCK_STREAM):
        try:
            s = socket.socket(family, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(addr)
            print(f"OK   {host} -> {addr}")
            s.close()
        except Exception as e:
            print(f"FAIL {host} -> {addr}: {type(e).__name__}: {e}")