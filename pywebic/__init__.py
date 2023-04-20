import asyncio
import mimetypes
import os
import re
import io
import socket
from contextlib import redirect_stdout


class WebServer:
    def __init__(self, loop, host = '', port = 8000) -> None:
        self.host = host
        self.port = port
        self.loop = loop
        self.PY_BLOCK_REGEX = r'(<\?py\s+(.+?)\s*\?>)'

    async def serve_file(self, client_socket, filename):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nFile Not Found'
            await self.loop.sock_sendall(client_socket, response.encode('utf-8'))
        else:
            content_type, _ = mimetypes.guess_type(filename)
            headers = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n'
            await self.loop.sock_sendall(client_socket, headers.encode('utf-8') + content)

    async def handle_request(self, client_socket):
        request_data = (await self.loop.sock_recv(client_socket, 1024)).decode('utf-8')
        method, path, version = request_data.split('\r\n')[0].split(' ')

        if method != 'GET':
            response = 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/html\r\n\r\nMethod Not Allowed'
            await self.loop.sock_sendall(client_socket, response.encode('utf-8'))
            client_socket.close()
            return

        if path[1:] == "":
            filename = os.path.join(os.getcwd(), "index.html")
        else:
            filename = os.path.join(os.getcwd(), path[1:])
        if os.path.isfile(filename):
            if filename.endswith('.html'):
                with open(filename, 'r') as f:
                    html = f.read()
                
                def replace_py_blocks(match):
                    block = match.group(2)
                    # print("got a py block:", block)
                    f = io.StringIO()
                    with redirect_stdout(f):
                        # exec(block, {'echo': self.echo}, {'buffer': buffer})
                        exec(block)
                        result = f.getvalue()
                    return result

                new_html = re.sub(self.PY_BLOCK_REGEX, replace_py_blocks, html, flags=re.DOTALL)

                content = new_html.encode('utf-8')
            else:
                with open(filename, 'rb') as f:
                    content = f.read()

            content_type, _ = mimetypes.guess_type(filename)
            headers = f'HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n'
            await self.loop.sock_sendall(client_socket, headers.encode('utf-8') + content)
        else:
            response = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\nFile Not Found'
            await self.loop.sock_sendall(client_socket, response.encode('utf-8'))

        client_socket.close()

    async def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(1)

            print(f'Serving PyWebic HTTP on port {self.port} ...')

            server_socket.setblocking(False)
            while True:
                client_socket, address = await self.loop.sock_accept(server_socket)
                print(f'Got a request from {address[0]}')
                asyncio.create_task(self.handle_request(client_socket))

