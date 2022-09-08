from engine import cryptoEngine

engine = cryptoEngine('opensesemiabra..')
text = b'HelloWorld!!....'
matrix = [
        ['H','o','l','.'],
        ['e','W','d','.'],
        ['l','o','!','.'],
        ['l','r','!','.']
    ]

def test_block_creation():
    assert matrix == engine.divide_into_blocks(text.encode())

def test_row_shifting():
    alpha = ['H','e','l','l']
    assert ['l','H','e','l'] == engine.shift_rows(alpha,3)

def test_revert_row_shift():
    #shifted array
    shifted = []
    shifted.append(matrix[0])
    for i in range(1,len(matrix)):
        shifted.append(engine.shift_rows(matrix[i],i))
    print(shifted)
    #unshift shifted rows
    unshifted=[]
    unshifted.append(shifted[0])
    for i in range(1,len(matrix)):
        unshifted.append(engine.shift_rows(shifted[i],4-i))
    print(unshifted)
    assert matrix==unshifted

def test_reconstruction():
    assert text==engine.reconstruct(engine.divide_into_blocks(text)[0])

def test_revert_xor():
    pass

def test_substitution():
    assert 99==engine.substitute(0)
    assert 202==engine.substitute(16)
    assert 161==engine.substitute(241)

def test_revert_substitution():
    input=16
    sub = engine.substitute(16)
    assert input==engine.unsubstitute(sub)

def test_multiplication():
    assert 21 == engine.multiply(0x02,0x87)
    assert 70 == engine.multiply(0x01,0x46)
    assert 178 == engine.multiply(0x03,0x6e)

engine.multiply(0x02,0x87)