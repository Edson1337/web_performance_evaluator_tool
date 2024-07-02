import socket

def check_port(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((host, port))
            print(f"The {port} port is in use.")
            return True
        except ConnectionRefusedError:
            print(f"The {port} port is not in use or the application is not accepting connections.")
            return False
        except socket.error as e:
            print(f"Error checking port: {e}")
            return False