#Copy Right:李嘉维1427407017
import select,socket,sys
class TCP_Client:
	def __init__(self):
		#accept the argument of host and port
		self.host = sys.argv[1]
		self.port = int(sys.argv[2])
		#set the initial argument of server socket
		self.bufferSize = 1024
		#build the socket
		self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#set the initial argument of select
		self.inputs = [sys.stdin,self.clientSocket]
		#Connect to the Server
		self.clientSocket.connect((self.host,self.port))
		self.clientSocket.setblocking(0)
		print '[System]Sucessfully connected to the server!'
	def run(self):
		while True:
			try:
				rlist,wlist,elist = select.select(self.inputs,[],[])
				for readable in rlist:
					if readable is self.clientSocket:
						data = readable.recv(self.bufferSize)
						print "[Server]"+data

					else:
						
						data = raw_input(">>")
						if data == 'exit':
							self.clientSocket.close()
							print '[System]Close'
							sys.exit(0)
						else:
							self.clientSocket.send(data)
			except KeyboardInterrupt:
				self.clientSocket.close()
				print '[System]Close'
				sys.exit(0)
def main():
	client = TCP_Client()
	client.run()
if __name__ == '__main__':
	main()