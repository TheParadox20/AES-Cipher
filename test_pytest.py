from AES import cryptoEngine

def test_decryption_engine():
    file = open('test_cases/hello.txt')
    text = file.read()
    assert 'text' == cryptoEngine.decrypt('asdfwr')