import socket
import sys

def download_file(filename, server_ip, server_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((server_ip, server_port))
        request = f'GET {filename}\n'
        sock.sendall(request.encode())
        response_header = ''
        while True:
            chunk = sock.recv(1).decode()
            response_header += chunk
            if '\n\n' in response_header:
                break

        # Check for a valid response
        header_lines = response_header.split('\n')
        if header_lines[0] != '200 OK':
            print(f"Error from server: {header_lines[0]}")
            return

        body_length = int(header_lines[2].split(': ')[1])
        received_bytes = 0
        body_chunks = []
        while received_bytes < body_length:
            chunk = sock.recv(min(body_length - received_bytes, 4096))
            if not chunk:
                raise RuntimeError("Socket connection broken")
            body_chunks.append(chunk)
            received_bytes += len(chunk)

        file_content = b''.join(body_chunks)
        with open(filename, 'wb') as file:
            file.write(file_content)

        print(f"File {filename} downloaded and saved successfully.")

    finally:
        sock.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 CSDownloader.py <filename> <server_ip> <server_port>")
        sys.exit(1)

    filename = sys.argv[1]
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])

    download_file(filename, server_ip, server_port)
