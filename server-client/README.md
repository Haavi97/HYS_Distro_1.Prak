# User script


>Module that implements a simple server-client that can accept
several clients...

# Usage
CLI application that requires 3 parameters:
1. Server port
2. Client port
3. User name

There is no restriction for the name, but the port must not be from the reserved ones.

Example:
```bash
user.py 5000 6000 user1
```

## Usage example in different terminal windows

Terminal 1:
```bash
user.py 5000 6000 user1
```

Terminal 2:
```bash
user.py 6000 5000 user2
```

With the previous 2 code lines the two users can message themselves. You can \
add a third user but the can only send to one of the other users (servers):

Terminal 3 (this example connects to user 1 and listens in port 7000):
```bash
user.py 7000 5000 user3
```

# Plan
- [x] Server client user with multiple connections
- [ ] Connection to several ip addresses (client)
- [ ] Automatic connection to new ip addresses connecting to the user server (client)
- [ ] When a client connects to a server somehow send it's server port so the server \
can also connect to that user.
- [ ] Automatically add the addresses of new clients.
- [ ] Error handling
- [ ] Implement over the internet not only locally


# User 

``` python 
 class User() 
```

Documentation to User class.

This class handles ip address storing and retrieving them
from a txt file.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|     host | int |         (default value = 127.0.0.1)        Server ip address | 
|     port | int  |         (default value = 5000)        Server port | 
|     name | str |         User name | 


--------- 

## Methods 

 
| method    | Doc             |
|:-------|:----------------|
| start_server | Starts the server listening and accept any coming connection. | 
| accept_connection | Accepts incoming connections to the server. | 
| listen_data | Starts to received data from the given client. | 
| start_client | Starts client connection to the given server ip address and port. | 
| validate_msg | Validates an input message to avoid void strings. | 
 
 

### start_server

``` python 
    start_server() 
```


Starts the server listening and accept any coming connection.

### accept_connection

``` python 
    accept_connection() 
```


Accepts incoming connections to the server.

### listen_data

``` python 
    listen_data(conn, address) 
```


Starts to received data from the given client.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         conn | socket.socket |             connection object from server_socket.accept function | 
|         address | (int, int) |             address object from server_socket.accept function. Tuple containing (ip address, port) | 


### start_client

``` python 
    start_client(ip, host_port) 
```


Starts client connection to the given server ip address and port.

| Parameters    | Type             | Doc             |
|:-------|:-----------------|:----------------|
|         ip | str |             ip address of the server | 
|         host_port | int |             port number of the server | 


### validate_msg

``` python 
    validate_msg() 
```


Validates an input message to avoid void strings.