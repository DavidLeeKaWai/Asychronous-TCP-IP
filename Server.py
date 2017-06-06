#Copy Right:李嘉维1427407017
import socket,sys,select
from time import ctime 
class TCP_Server:
	def __init__(self):
		#accept the argument of ip and port from cmd 
		self.host = sys.argv[1]
		self.port = int(sys.argv[2])
		#set the initial argument of server socket
		self.bufferSize = 1024
		self.maxClient = 5		
		#set the dictionary of connected socket
		self.connections =  {}
		#build socket
		self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serverSocket.bind((self.host,self.port))
		self.serverSocket.listen(self.maxClient)
		self.serverSocket.setblocking(0)
		#set the initial argument of select
		self.inputs = [sys.stdin,self.serverSocket]
		print "[System]Server start!"
	def run(self):
		while True:
			try:
				rlist,wlist,elist = select.select(self.inputs, [], [])
				for readable in rlist:
					if readable == self.serverSocket:
						connection,ip = readable.accept()
						connection.setblocking(0)
						print "[System]Accept connection from:"+format(ip)
						self.connections[connection] = ip
						self.inputs.append(connection)
						# print connection.recv(self.bufferSize)
					else:
						if readable == sys.stdin:
							data = raw_input(">>")
							if data == 'exit':
								print '[System]Server closed'
								sys.exit(0)
							for client in self.connections.keys():
								client.send(data)
						else:
							data = readable.recv(self.bufferSize)
							if not data:
								print '[System]'+format(self.connections[readable])+'closed'
								self.inputs.remove(readable)
								del self.connections[readable]

								readable.close()							
							else:
								if data == 'exit':
									self.inputs.remove(readable)
									print '[System]'+format(self.connections[readable])+'closed'
									del self.connections[readable]
									readable.close()
									# connections.remove(readable)
								else:
									print format(self.connections[readable])+data
			except KeyboardInterrupt:
				print '[System]Server closed'
				sys.exit(0)
def main():
	server = TCP_Server()
	server.run()
if __name__ == '__main__':
	main()