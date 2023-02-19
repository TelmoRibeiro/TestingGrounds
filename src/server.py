import socket



########## GLOBAL ##########
IP_ADDRESS = "127.0.0.1"
PORT       = 12301
############################



print("creating socket...")
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((IP_ADDRESS, PORT))
    print("running server...")
    while True:
        s.listen(1)
        connection, address = s.accept()
        print("\n")
        print(f"connection from {address} established!")
        with connection:
            while True:
                request = connection.recv(2048).decode()
                if request == "request: public_key":
                    with open("public_key.pem", "r") as public_key_file:
                        public_key = public_key_file.read()
                        connection.send(f"{public_key}".encode())
                        print("done sending: public_key.pem")
                    break
                if request == "request: private_key":
                    with open("private_key.pem", "r") as private_key_file:
                        private_key = private_key_file.read()
                        connection.send(f"{private_key}".encode())
                        print("done sending: private_key.pem")
                    break
            print(f"connection from {address} closed!")