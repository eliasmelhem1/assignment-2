import socket

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 9999))

    while True:
        response = client.recv(4096)
        if not response:
            break
        print(response.decode(), end="")

        # Sending user input to server
        user_input = input()
        client.send(user_input.encode())
        if user_input == '4':  # Exit option
            break

    client.close()

if __name__ == "__main__":
    start_client()
    