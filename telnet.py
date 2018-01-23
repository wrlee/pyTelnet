import socket
import threading


class net:
	"""Sort of a lightweight telnet server."""

	def __init__(self):
		# super(net, self).__init__()
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.host = 'localhost' #socket.gethostname()
		# print('timeout:',socket.getdefaulttimeout())

	def telnet(self,port=4002,connectionCount=2):
		#https://pymotw.com/2/threading/
		self.socket.bind((self.host,port))
		self.socket.listen(connectionCount)
		threads = []
#		try:
		while True:
			print('Waiting for connection...')
			try:
				connection,addr = self.socket.accept()
			except KeyboardInterrupt:
				print('interrupt accept()')
				break
			print('Received connection from  %s:%d' % (addr[0],addr[1]))
			# self.startDialog(connection,addr)
			thread = threading.Thread(target=self.startDialog, args=(connection,addr))
			threads.append(thread)
			thread.start()
			print(threads)
#		except KeyboardInterrupt:

		print('after telnet accept loop', threads)
		def empty_thread(thread):
			print(thread.name,thread.is_alive())
			del thread
		for i,thread in enumerate(threads):
			print(i,thread.name, thread.is_alive())
			threads.remove(thread)
			del thread
		print('end:', threads)

	def dialog(self,connection,addr):
		msg = '\r\nThank you for connecting from %s:%d\r\n\r\n' % (addr[0],addr[1])
		msg = msg.encode('ascii')
		connection.send(msg)
		while True:
			try:
				msg = yield connection.recv(2048)
				print('d:',msg)
				if len(msg):
					try:
						msg = (msg+'\r\n').encode('ascii')
					except (AttributeError,TypeError):
						msg = msg+'\r\n'.encode('ascii')
					connection.send(msg)
				yield
			except KeyboardInterrupt:
				print('dialog() break')
				break
		yield

	def startDialog(self,connection,addr):
		dialog_gen = self.dialog(connection,addr)
		for msg in dialog_gen:
			try:
				print('sd:',msg)
				if msg == b'\xff\xf4\xff\xfd\x06':
					break
				while len(msg) and msg[0] == 255:
					if msg[1] >= 250:
						msg = msg[3:]
					else:
						msg = msg[2:]
				msg = msg.strip()
				if len(msg):
	#				try:
						msg = '%d: %s' % (addr[1],msg.decode().strip())
	#				except UnicodeEncodeError as e:
	#					print(e)
	#					msg = '%d: %s' % (addr[1],msg)
				dialog_gen.send(msg)
				# print(str(msg))
				# connection.send(msg)
			except KeyboardInterrupt:
				print('break from dialog loop')
				break
		connection.close()
		print('Close connection to  %s:%d' % (addr[0],addr[1]))

	def connect(host,port=80):
		connection = socket.connect((host,port))
		request = connection.recv()
		print('<< ',request)


if __name__ != '__main__':
	def co(val):
		'https://stackoverflow.com/a/35470049/765032'
		print('start co()')
		while True:
			# print('before first yield',val)
			# print('before second yield',val)
			val = yield val
			# print('after second yield',val)
			yield
	gen = co(1)
	for i in gen:
		print('iteration',i)
		gen.send(i+1)
		if i > 5: break
	# gen.send(v)
	# for i in gen:
		# print('loop',i)
else:
	n = net()
	n.telnet(23)
