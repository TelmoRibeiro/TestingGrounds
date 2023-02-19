from Crypto.PublicKey import RSA



print("generating keys...")
key = RSA.generate(2048) 

with open("private_key.pem", "wb") as private_key_file:
    private_key_file.write(key.export_key("PEM"))
print("done generating: private_key.pem")

with open("public_key.pem", "wb") as public_key_file:
    public_key_file.write(key.public_key().export_key("PEM"))
print("done generating: public_key.pem")