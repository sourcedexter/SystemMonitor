import socket


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('www.google.com', 0))
    return s.getsockname()[0]
result = getNetworkIp()
print (result)
