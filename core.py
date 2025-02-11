from typing import List, Dict, Optional, Union
import socket
import json

class SocketPyCore:
    """
    A socket manager for TCP, UDP, and ICMP protocols.
    Provides functionality to manage server and client connections.

    Attributes:
        host (str): The host address.
        port (int): The port number.
        protocol (str): The communication protocol (TCP, UDP, or ICMP).
        connections (List[Dict[str, Union[str, Optional[socket.socket]]]]): A list of active connections.
        socket (Optional[socket.socket]): The main socket object.
    """

    MAX_PACKET_SIZE: int = 65535  # Maximum UDP packet size
    BUFFER_SIZE: int = 4096  # Default buffer size for receiving data

    def __init__(self, host: str, port: int, protocol: str = "TCP") -> None:
        self.host: str = host
        self.port: int = port
        self.protocol: str = protocol.upper()
        self.connections: List[Dict[str, Union[str, Optional[socket.socket]]]] = []
        self.socket: Optional[socket.socket] = None

        try:
            if self.protocol == "TCP":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            elif self.protocol == "UDP":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            elif self.protocol == "ICMP":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            else:
                raise ValueError(f"Unsupported protocol: {protocol}")

            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        except socket.error as error:
            raise Exception(f"Failed to initialize socket: {error}")

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context and clean up the socket."""
        if self.socket:
            self.socket.close()

    def send(self, data: Dict, ip: Optional[str] = None, connection: Optional[socket.socket] = None) -> None:
        """
        Sends data to a connected socket.
        - Server can send data to a specific client using their IP address.
        - Client sends data to the connected server.

        Args:
            data (Dict): The dictionary to send as JSON.
            ip (Optional[str]): Target IP address for server-side sending (optional).
            connection (Optional[socket.socket]): The socket object for server-targeted sending.

        Raises:
            Exception: If the socket or connection fails.
        """
        if not self.socket:
            raise Exception("Socket is not initialized.")

        try:
            data = json.dumps(data).encode("utf-8")
            if self.protocol == "TCP":
                if connection:
                    connection.send(data)  # Send to a specific client
                elif ip:
                    # Find connection by IP
                    target = next(
                        (conn["connection"] for conn in self.connections if conn["address"] == ip), None
                    )
                    if target:
                        target.send(data)
                    else:
                        raise Exception(f"No active connection found for IP: {ip}")
                else:
                    self.socket.send(data)  # For clients
            elif self.protocol == "UDP":
                if ip is None:
                    raise ValueError("IP address is required for UDP communication.")
                self.socket.sendto(data, (ip, self.port))  # UDP sending
            print("Data sent successfully.")
        except socket.error as error:
            raise Exception(f"Failed to send data: {error}")

    def receive(self, ip: Optional[Union[str, List[str]]] = None, connection: Optional[socket.socket] = None) -> Optional[Dict]:
        """
        Receives data from a socket. Filters incoming data by IP address if specified.

        Args:
            ip (Optional[Union[str, List[str]]]): A string or list of allowed IP addresses to receive data from.
            connection (Optional[socket.socket]): The connection to receive data from (for TCP servers).

        Returns:
            Optional[Dict]: The received data as a dictionary, or None if no data was received.

        Raises:
            Exception: If the socket or connection fails.
        """
        if not self.socket:
            raise Exception("Socket is not initialized.")

        try:
            if self.protocol == "TCP":
                if connection:
                    data = connection.recv(self.BUFFER_SIZE)
                    if data:
                        address = connection.getpeername()[0]
                        if ip and address not in ip:
                            return None
                        print(f"Data received from {address}.")
                        return json.loads(data.decode("utf-8"))
            elif self.protocol == "UDP":
                data, address = self.socket.recvfrom(self.MAX_PACKET_SIZE)
                if ip and address[0] not in ip:
                    return None
                print(f"Data received from {address[0]}.")
                return json.loads(data.decode("utf-8"))
        except socket.error as error:
            raise Exception(f"Failed to receive data: {error}")
        except json.JSONDecodeError:
            raise Exception("Received data is not valid JSON.")

    def detach(self, ip: str) -> None:
        """
        Disconnects a client from the server based on its IP address.

        Args:
            ip (str): The IP address of the client to disconnect.

        Raises:
            Exception: If the IP address is not found in the active connections.
        """
        try:
            # Find the connection by IP and close the socket
            connection = next(
                (conn["connection"] for conn in self.connections if conn["address"] == ip), None
            )
            if connection:
                connection.close()
                # Mark the connection as disconnected
                for conn in self.connections:
                    if conn["address"] == ip:
                        conn["status"] = "disconnected"
                print(f"Disconnected client with IP: {ip}")
            else:
                raise Exception(f"No active connection found for IP: {ip}")
        except socket.error as error:
            raise Exception(f"Failed to disconnect client: {error}")
