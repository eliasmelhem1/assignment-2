import socket
import threading

# Predefined bank accounts (for simplicity)
accounts = {
    "1001": {"password": "pass1", "balance": 5000},
    "1002": {"password": "pass2", "balance": 3000},
    "1003": {"password": "pass3", "balance": 7000},
}

# Client handling function
def handle_client(client_socket, client_address):
    try:
        # Authentication
        client_socket.send(b"Enter account number: ")
        account_number = client_socket.recv(1024).decode().strip()
        client_socket.send(b"Enter password: ")
        password = client_socket.recv(1024).decode().strip()

        if account_number in accounts and accounts[account_number]["password"] == password:
            client_socket.send(b"Authentication successful\n")
            while True:
                # Menu
                client_socket.send(b"\n1. Check Balance\n2. Deposit Money\n3. Withdraw Money\n4. Exit\nChoose an option: ")
                option = client_socket.recv(1024).decode().strip()
                
                if option == '1':
                    # Check Balance
                    balance = accounts[account_number]["balance"]
                    client_socket.send(f"Your balance is: {balance}\n".encode())
                elif option == '2':
                    # Deposit Money
                    client_socket.send(b"Enter amount to deposit: ")
                    amount = float(client_socket.recv(1024).decode().strip())
                    accounts[account_number]["balance"] += amount
                    client_socket.send(b"Deposit successful\n")
                elif option == '3':
                    # Withdraw Money
                    client_socket.send(b"Enter amount to withdraw: ")
                    amount = float(client_socket.recv(1024).decode().strip())
                    if amount <= accounts[account_number]["balance"]:
                        accounts[account_number]["balance"] -= amount
                        client_socket.send(b"Withdrawal successful\n")
                    else:
                        client_socket.send(b"Insufficient balance\n")
                elif option == '4':
                    # Exit
                    final_balance = accounts[account_number]["balance"]
                    client_socket.send(f"Your final balance is: {final_balance}\n".encode())
                    break
                else:
                    client_socket.send(b"Invalid option\n")
        else:
            client_socket.send(b"Authentication failed\n")
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 9999))
    server.listen(5)
    print("Server started and listening on port 9999")

    while True:
        client_socket, client_address = server.accept()
        print(f"Accepted connection from {client_address}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()