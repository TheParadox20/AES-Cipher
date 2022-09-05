from engine import cryptoEngine


debugging = 1

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
    choice = '1' if debugging else input('Welcome to the AES Cryptographic Engine. What will you be doing:\n\t1.) Encrypt text/file\n\t2.) Decrypt text/file\n')
    while 1:
        keyInput = 'k.txt' if debugging else input('Enter key/path to key file\n')
        key = isValidKey(keyInput)
        if key[0]>0:
            break
        print('Invalid key, please try again:\n')
    print(key)

    message = 'test_cases/hello.txt' if debugging else input(f"Enter text/path tofile to {'encrypt'if choice=='1' else 'decrypt'}\n")

    engine = cryptoEngine(key)
    if choice=='1':
        cipher = engine.encrypt(message)
    if choice=='2':
        text = engine.decrypt(message)

main()
