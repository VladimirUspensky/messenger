import socket
import asyncio


class Client:
    """Class of the client"""
    def __init__(self, server_ip: str, server_port: int):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((str(server_ip), int(server_port)))
        self.client.setblocking(False)
        self.event_loop = asyncio.get_event_loop()
        self.event_loop.run_until_complete(self.start_client())

    async def send_message(self) -> None:
        """Sends messages to other clients"""
        while True:
            message = await self.event_loop.run_in_executor(None, input, '-')
            await self.event_loop.sock_sendall(self.client, message.encode('utf-8'))

    async def get_message(self) -> None:
        """Gets messages from other clients"""
        while True:
            message = await self.event_loop.sock_recv(self.client, 1024)
            if not message:
                break
            print(message.decode('utf-8'))

    async def start_client(self) -> None:
        """Starts interaction between the current client and the server"""
        await asyncio.gather(self.event_loop.create_task(self.get_message()),
                             self.event_loop.create_task(self.send_message()))


def main():
    client = Client(server_ip='127.0.0.1', server_port=8000)
    client.start_client()


if __name__ == '__main__':
    main()
