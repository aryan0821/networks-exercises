from socket import *
print('starting')
clientSocket = socket(AF_INET, SOCK_STREAM)
serverName = 'date.cs.umass.edu'
address = (serverName, 18765)
clientSocket.connect(address)
sentence = ('GET 12345_redsox.jpg\n'.encode())

grading_sock = socket(AF_INET, SOCK_STREAM)
grading_sock.connect((serverName, 20001))
grading_sock.send(b'IAM 12345\n')
grade_res = grading_sock.recv(512)
print(grade_res)

clientSocket.send(sentence)
something = clientSocket.recv(1024)
print(something)