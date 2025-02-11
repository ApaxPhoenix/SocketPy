# SocketPy

SocketPy is a Python library designed to simplify network programming by providing an easy-to-use interface for handling socket connections. Whether you're building a chat application, a network monitoring tool, or any other networked system, SocketPy streamlines the process with its intuitive API and robust features.

## Installation

To install SocketPy, use pip:

```bash
pip install socketpy
```

SocketPy has no complex dependencies, ensuring a smooth setup process.

## Features

SocketPy offers a variety of features to make network programming more efficient:

- **Multi-Protocol Support**: Work with TCP, UDP, and ICMP protocols effortlessly.
- **Simplified Connections**: Easily set up and manage server and client connections.
- **JSON Handling**: Automatically encode and decode JSON data for seamless communication.
- **Connection Management**: Track and manage active connections with ease.

## Getting Started

Below are examples demonstrating how to use SocketPy for common network programming tasks.

### Creating a Server

Here’s how to set up a basic server that listens for incoming connections and handles communication:

```python
from socketpy import SocketPy

# Start the server
with SocketPy.server(host="127.0.0.1", port=8080) as server:
    while True:
        try:
            # Accept a new connection
            connection, address = server.socket.accept()
            print(f"New connection from {address[0]}:{address[1]}")
            
            # Add the new connection to the list
            server.connections.append({
                "address": f"{address[0]}:{address[1]}",
                "connection": connection,
                "status": "connected"
            })
            
            # Handle communication with the client
            with connection:
                while True:
                    data = server.receive(connection=connection)
                    if data:
                        print(f"Received: {data}")
                        server.send({"response": "Message received"}, connection=connection)
                        
        except KeyboardInterrupt:
            print("Shutting down the server...")
            break
```

### Creating a Client

Connecting to a server is straightforward with SocketPy:

```python
from socketpy import SocketPy

# Connect to the server
with SocketPy.client(host="127.0.0.1", port=8080) as client:
    client.send({"message": "Hello, server!"})
    response = client.receive()
    print(f"Server response: {response}")
```

### Sending and Receiving Messages

Sending and receiving messages is simple and intuitive:

```python
# Send a message to the server
client.send({"status": "Everything is running smoothly."})

# Receive a response from the server
response = client.receive()
print(response)
```

### Managing Connections

SocketPy makes it easy to manage active connections:

```python
# Disconnect a client by IP address
server.detach(ip="127.0.0.1")
```

## License

SocketPy is released under the MIT License. For more details, please refer to the [LICENSE](LICENSE) file. You are free to use, modify, and distribute this software as you see fit.