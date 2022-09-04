class cryptoEngine:
    def __init__(self, key):
        self.key = key

    def encrypt(self,message):
        print('Starting ENCRYPTION')
        if isFile(message):
            file = open(message, 'r')
            message = file.read()
        print('Encrypting....\n',message)
            
    def decrypt(self,message):
        print('Starting DECRYPTION')
        if isFile(message):
            file = open(message, 'r')
            message = file.read()
        print('Decrypting....\n',message)
    
def isFile(path): #check if file exists
    try:
        file = open(path,'r')
    except:
        return False
    return True

def isValidKey(key):
    """
        Checks if key is 128, 192, or 256 bit
        returns 0 if none
    """
    if isFile(key):# if file is found
        file = open(key, 'r')
        key = file.read()

    if len(key)==16:
        return 1, key
    elif len(key)==24:
        return 2, key
    elif len(key)==32:
        return 3, key
    return 0, key


def main():
    choice = input('Welcome to the AES Cryptographic Engine. What will you be doing:\n\t1.) Encrypt text/file\n\t2.) Decrypt text/file\n')
    while 1:
        keyInput = input('Enter key/path to key file\n')
        key = isValidKey(keyInput)
        if key[0]>0:
            break
        print('Invalid key, please try again:\n')
    print(key)

    message = input(f"Enter text/path tofile to {'encrypt'if choice=='1' else 'decrypt'}\n")

    engine = cryptoEngine(key)
    if choice=='1':
        engine.encrypt(message)
    if choice=='2':
        engine.decrypt(message)

main()
