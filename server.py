import sys
import socket
import asyncio


class Server:
    """Class of the server"""
    def __init__(self, ip: str, port: int):
        self.ip = str(ip)
        self.port = int(port)
        self.all_clients = []
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
            if client_socket not in self.all_clients:
                self.all_clients.append(client_socket)
            self.event_loop.create_task(self.get_client_message(client_socket))

    async def send_message_to_everyone(self, client_socket: socket.socket, message: bytes) -> None:
        """Sends message from one client to others"""
        while True:
            for client in self.all_clients:
                if client is not client_socket:
                    await self.event_loop.sock_sendall(client, message)
            break

    async def get_client_message(self, client_socket: socket.socket) -> None:
        """Gets client's message"""
        while True:
            message = await self.event_loop.sock_recv(client_socket, 1024)
            if not message:
                break
            split_message = message.decode('utf-8').split(' ')
            if split_message[len(split_message) - 2] == '-to':
                await self.send_message_by_id((split_message[0] + '\n\r').encode('utf-8'),
                                              int(split_message[len(split_message) - 1]))
            else:
                await self.send_message_to_everyone(client_socket, message)

    async def send_message_by_id(self, message: bytes, client_id: int) -> None:
        """Sends message from one client to another one, by the name of the second"""
        while True:
            for client_i in range(len(self.all_clients)):
                if client_i == client_id:
                    await self.event_loop.sock_sendall(self.all_clients[client_i], message)
            break

    async def start(self) -> None:
        """Starts the server"""
        await self.event_loop.create_task(self.accept_client())


def main():
    server = Server(ip='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
