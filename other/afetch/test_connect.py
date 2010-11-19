import socket
import sys

host = "localhost"
port = 5002

#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.connect((host, port))

s = socket.create_connection((host, port))
s.send('{"cmd": "twitter_user_list_info", "data": {"token" : "user", "users": [42053149, 43722655, 78727134, 19311402, 104667446, 8453452, 16831087, 33747184, 14277276, 19532593, 90683732, 82002786]}}\n\r\n')

buf = ""
while 1:
    data = s.recv(1000)
    if not data:
        break
    buf += data

sys.stdout.write(buf)
s.close()



