import socket
import asyncio
from db import *
from collections import defaultdict


class Server:
    """Class of the server"""
    def __init__(self, ip: str, port: int):
        self.ip = str(ip)
        self.port = int(port)
        self.all_clients = []
        self.chat_history = []
        self.rooms = defaultdict(set)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.ip, self.port))
        self.server.setblocking(False)
        self.server.listen()

        self.event_loop = asyncio.get_event_loop()
        try:
            self.event_loop.run_until_complete(self.start())
        except KeyboardInterrupt:
            print('Exit')
            exit(0)

    async def accept_client(self) -> None:
        """Connects clients to the server"""
        while True:
            history = await self.get_chat_history_in_room(1)
            #print(history)
            history = await self.parse_chat_history(history)
            self.print_chat_history(history)
            client_socket, _ = await self.event_loop.sock_accept(self.server)
            if client_socket not in self.all_clients:
                self.all_clients.append(client_socket)
            self.event_loop.create_task(self.get_client_message(client_socket))

    async def send_message_to_everyone(self, client_socket: socket.socket, message: bytes) -> None:
        """Sends message from one client to others"""
        for client in self.all_clients:
            if client is not client_socket:
                await self.event_loop.sock_sendall(client, message)

    async def get_client_message(self, client_socket: socket.socket) -> None:
        """Gets client's message"""
        while True:
            message = await self.event_loop.sock_recv(client_socket, 1024)
            if not message:
                break
            await self.parse_client_message(message, client_socket)

    async def send_message_by_id(self, message: bytes, client_id: int) -> None:
        """Sends message from one client to another one, by the name of the second"""
        for client_i in range(len(self.all_clients)):
            if client_i == client_id:
                await self.event_loop.sock_sendall(self.all_clients[client_i], message)

    async def send_message_in_room(self, message: str, room_id: str) -> None:
        """Sends message from one client to others in the chosen room"""
        recipients = self.rooms.get(str(room_id))
        for recipient in recipients:
            await self.event_loop.sock_sendall(recipient, message.encode('utf-8'))

    async def add_to_room(self, room_id: str, client_socket: socket.socket) -> None:
        """Adds the given client to the room"""
        self.rooms[str(room_id)].add(client_socket)

    @staticmethod
    async def get_chat_history_in_room(room_id: int):
        """Returns chat history of all clients from the given room"""
        history = fetchall('messages', ['room_id', 'from_id', 'to_id', 'content'])
        result_history = []
        for message in history:
            if message[0] == room_id:
                result_history.append(message)
        return result_history

    @staticmethod
    async def parse_chat_history(chat_history: List[tuple]) -> Dict[str, str]:
        """Returns dictionary NAME:MESSAGE with all room's history"""
        history = dict()
        clients = fetchall('clients', ['id', 'name'])
        for tup in chat_history:
            history[tup[1]] = tup[3]
        for tup in clients:
            try:
                history[tup[1]] = history.pop(tup[0])
            except KeyError:
                pass
        return history

    @staticmethod
    def print_chat_history(chat_history: Dict[str, str]) -> None:
        """Writes history in the console"""
        for message in chat_history:
            print(f'{message} -> {chat_history[message]}')


    async def get_private_chat_history(self, first_client: socket.socket, second_client: socket.socket):
        """Returns chat history of 2 given clients"""

    async def get_main_chat_history(self):
        """Returns all history from the main chat"""

    async def parse_client_message(self, message: bytes, client_socket: socket.socket) -> None:
        """Parses client's input: some flags, commands, etc"""
        message = message.decode('utf-8')
        split_message = message.split(' ')

        if split_message[0] == '/create_room':
            await self.create_room(split_message[1], client_socket)
        elif split_message[0] == '/join':
            await self.add_to_room(split_message[1], client_socket)
        elif split_message[len(split_message) - 2] == '/to':
            await self.send_message_by_id((split_message[0] + '\n\r').encode('utf-8'),
                                          int(split_message[len(split_message) - 1]))
        elif split_message[len(split_message) - 2] == '/room':
            await self.send_message_in_room((split_message[0] + '\n\r'),
                                            split_message[len(split_message) - 1])
        else:
            await self.send_message_to_everyone(client_socket, message.encode('utf-8'))

    async def create_room(self, room_id: str, client_socket: socket.socket) -> None:
        """Creates the room by client's request"""
        self.rooms[room_id].add(client_socket)

    async def start(self) -> None:
        """Starts the server"""
        await self.event_loop.create_task(self.accept_client())


def main():
    server = Server(ip='127.0.0.1', port=8000)


if __name__ == '__main__':
    main()
