from contextlib import contextmanager
import socket
import warnings
from .core import SocketPyCore

class SocketPy:
    @classmethod
    @contextmanager
    def server(cls, host: str, port: int, protocol: str = "TCP") -> SocketPyCore:
        """
        Context manager for running a server.

        Args:
            host (str): Host address.
            port (int): Port number.
            protocol (str): Communication protocol (default is TCP).

        Yields:
            SocketPyCore: An instance of the socket manager.

        Raises:
            Exception: If the server fails to start.
        """
        obj: SocketPyCore = SocketPyCore(host, port, protocol)
        try:
            obj.socket.bind((host, port))
            if obj.protocol == "TCP":
                obj.socket.listen(5)
            print(f"Started server at {host}:{port}. Press Ctrl+C to stop it.")
            yield obj
        except socket.error as error:
            warnings.warn(f"Server initialization failed: {error}", RuntimeWarning)
            raise Exception(f"Critical server failure: {error}")
        finally:
            obj.__exit__(None, None, None)

    @classmethod
    @contextmanager
    def client(cls, host: str, port: int, protocol: str = "TCP") -> SocketPyCore:
        """
        Context manager for running a client.

        Args:
            host (str): Host address.
            port (int): Port number.
            protocol (str): Communication protocol (default is TCP).

        Yields:
            SocketPyCore: An instance of the socket manager.

        Raises:
            Exception: If the client fails to connect.
        """
        obj: SocketPyCore = SocketPyCore(host, port, protocol)
        try:
            obj.socket.connect((host, port))
            print(f"Connected to server at {host}:{port}.")
            yield obj
        except ConnectionRefusedError:
            warnings.warn(f"Connection refused to {host}:{port}", RuntimeWarning)
        except socket.gaierror:
            warnings.warn(f"Address resolution failed for {host}", RuntimeWarning)
        except socket.error as error:
            raise Exception(f"Client connection failed: {error}")
        finally:
            if obj.socket:
                obj.socket.close()
