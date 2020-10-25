import socket
import asyncio


class Server:
    """Class of the server"""
    def __init__(self, ip: str, port: int):
        self.ip = str(ip)
        self.port = int(port)
        self.all_clients = set()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.setblocking(False)
        self.server.listen()

        self.event_loop = asyncio.get_event_loop()
        self.event_loop.run_until_complete(self.start())

    async def accept_client(self) -> None:
        """Connects clients to the server"""
        while True:
            client_socket, _ = await self.event_loop.sock_accept(self.server)
            self.all_clients.add(client_socket)
            self.event_loop.create_task(self.send_message(client_socket))

    async def send_message(self, client_socket: socket.socket) -> None:
        """Sends message from one client to others"""
        while True:
            message = await self.event_loop.sock_recv(client_socket, 1024)
            if not message:
                break
            for client in self.all_clients:
                if client is not client_socket:
                    await self.event_loop.sock_sendall(client, message)

    async def start(self) -> None:
        """Starts the server"""
        await self.event_loop.create_task(self.accept_client())


def main():
    server = Server(ip='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
