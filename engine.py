""" helpful
"hello world".encode('ascii') -> array of ascii decimal(s)
chr(<ascii decimal>) -> character
hex(int) -> hex string
''.join(map(bin,bytearray('\\','utf8'))) -> binary
int('10101000101',2) -> binary to decimal
int('f',16) -> hex to decimal
^ -> bitwise XOR operator
bin(n).replace("0b", "") -> binary from int
"""
class cryptoEngine:
    Sbox = [ #reading array item returns decimal representation
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76], 
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0], 
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15], 
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75], 
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84], 
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf], 
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8], 
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2], 
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73], 
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb], 
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79], 
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08], 
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a], 
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e], 
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf], 
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
    ]

    mix_matrix=[
        [0x2,0x3,0x1,0x1],
        [0x1,0x2,0x3,0x1],
        [0x1,0x1,0x2,0x3],
        [0x3,0x1,0x1,0x2]
    ]
    blockOrder=[0,4,8,12,1,5,9,13,2,6,10,14,3,7,11,15]
    roundConstants=['01','02','04','08','10','20','40','80','1B','36'] #at least for 128 bit


    def __init__(self, key):
        self.key = key[1]
        self.encryption_level = key[0] #128 192 or 256 bit


    def divide_into_blocks(self,message):
        """
            divides text into 128bits (16 chars)
            in a 4x4 matrix
            if message is less than 16chars, append '\0'
        """
        if type(message)==list:
            blocks=[[],[],[],[]]
            cursor=0
            for j in range(0,4):
                for k in range(0,4):
                    blocks[j].append(message[self.blockOrder[cursor]])
                    cursor+=1
            return blocks
        
        #Make message divisible by 16
        if(len(message)%16!=0):
            for i in range(0,(16-len(message)%16)):
                message+=b'\0'
        if(len(message)<16):
            for i in range(0,(16-len(message))):
                message+=b'\0'
        #create blocks
        blocks=[]
        for i in range(0,len(message),16):
            sub_message = message[i:i+16]
            cursor=0
            block=[[],[],[],[]]
            for j in range(0,4):
                for k in range(0,4):
                    block[j].append(sub_message[self.blockOrder[cursor]])
                    cursor+=1
            blocks.append(block)
        return blocks
        
    #def order_block(self,x):

    def key_expansion(self):
        precursor_key=self.divide_into_blocks(self.key.encode('ascii'))[0]
        expandedKey = [precursor_key]
        for i in range(0,10):# Create 10 keys i == round number
            new_block = []
            #rotate column
            word=[]
            for j in range (1,4):
                word.append(precursor_key[j][3])
            word.append(precursor_key[0][3])
            #substitution
            for k in range(0,len(word)):
                word[k]=self.substitute(word[k])
            #XOR round constant
            word[0]=self.XOR(word[0],int(self.roundConstants[i],16))
            for l in range(1,4):
                word[l] = self.XOR(word[l],00)
            #XOR corresponding keys
            for m in range(0,len(word)):
                word[m] = self.XOR(word[m],precursor_key[m][0])
            #remaining words in key
            new_block+=word
            for n in range(1,4):#3 words remaining
                for o in range(0,len(word)):
                    word[o] = self.XOR(word[o],precursor_key[o][n])
                new_block+=word

            new_block=self.divide_into_blocks(new_block)
            expandedKey.append(new_block)
            precursor_key=new_block
        return expandedKey

    def XOR(self,a,b):
        """
        Input(a,b):
            Scenario 1: a=list and b = list; one dimensional array
            Scenario 2: a=list and b = int
            Scenario 3: a=int and b = int
        """
        if (type(a)==type(b)==list): #scenario 1
            omega=[]
            if (len(a)!=len(b)):
                return
            if type(a[0])==list: # scenario 1.2 => Multidimensional array
                for i in range(0,len(a)):
                    temp=[]
                    for j in range(0,len(a[i])):
                        temp.append(a[i][j]^b[i][j])
                    omega.append(temp)
                return omega
            
            for i in range(0,len(a)):
                omega.append(a[i]^b[i])
            return omega
        if (type(a)!=type(b)): #scenario 2
            omega = []
            for i in range(0,len(a)):
                omega.append(a[i]^b)
            return omega
        return a^b #scenario 3
    
    def add_round_key(self,a,b):
        return self.XOR(a,b)
    
    def substitute(self,input):#input is a decimal output decimal
        #convert to hex string
        input = hex(input)[2:]
        if len(input)==1:
            input='0'+input
        row = int(input[0],16)
        col = int(input[1],16)
        return self.Sbox[row][col]
    
    def unsubstitute(self,input): #given a decimal find location of row and column in sbox and convert to decimal
        for i in range(0,len(self.Sbox)):
            if input in self.Sbox[i]:
                row=i
                break
        col = self.Sbox[row].index(input)
        #Create hex string from row and column
        row=hex(row)[2:]
        col=hex(col)[2:]
        output = row+col
        return int(output,16)


    def shift_rows(self,array,padding=1): #takes one dimensional array
        return array[padding:]+array[:padding]
    
    def mix_columns(self,matrix): # Takes 4x4 matrix and returns 4x4 matrix
        return matrix
    
    def reconstruct(self,matrix): #Takes 4x4 matrix returns 16 bytes
        block=b''
        #Flatten array
        flat=[]
        for i in range(0,len(matrix)):
            for j in range(0,len(matrix[i])):
                flat.append(matrix[j][i])
        #Convert decimal to hex then to bytes
        for i in flat:
            hexd=hex(i)[2:]
            if len(hexd)==1:
                hexd='0'+hexd
            block+=bytes.fromhex(hexd)
        return block
    
    def encrypt(self,message):
        if self.encryption_level!=1:
            print('Only 128 bit keys supported currently')
            return
        cipher = b''
        print('Starting ENCRYPTION')
        if isFile(message):
            file = open(message, 'rb')
            message = file.read()
        else:
            message=message.encode() #creates byte array
        message_blocks = self.divide_into_blocks(message)
        
        keys = self.key_expansion()
        
        for i in range(0,len(message_blocks)): # For each block
            block = message_blocks[i]
            for j in range(0,11): # Take each block through AES flow 10 times
                # Add round key
                block = self.XOR(block,keys[j])
                # Substitute
                for x in range(0,len(block)):
                    for y in range(0,len(block[x])):
                        block[x][y]=self.substitute(block[x][y])
                #Shift rows
                for k in range(1,len(block)):
                    block[k]=self.shift_rows(block[k],k)
                #Shift columns
                if i!=10: # Final round skip shifting columns
                    block=self.mix_columns(block)
            cipher+=self.reconstruct(block)
        return cipher
            
    def decrypt(self,cipher):
        text=b''
        print('Starting DECRYPTION')
        if isFile(cipher):
            file = open(cipher, 'rb')
            cipher = file.read()
        else:
            cipher=cipher.encode()
        
        message_blocks = self.divide_into_blocks(cipher)
        keys = self.key_expansion()

        for i in range(0,len(message_blocks)): # For each block
            block = message_blocks[i]
            for j in range(0,11): # Take each block through AES flow 10 times
                #Shift columns
                if i!=0: # First round skip shifting columns
                    block=self.mix_columns(block)
                
                #Invert Shift rows
                for k in range(1,len(block)):
                    block[k]=self.shift_rows(block[k],4-k)
                
                # Un Substitute
                for x in range(0,len(block)):
                    for y in range(0,len(block[x])):
                        block[x][y]=self.unsubstitute(block[x][y])

                # Add round key
                block = self.XOR(block,keys[10-j])
            text+=self.reconstruct(block)
        
        return text

def isFile(path): #check if file exists
        try:
            file = open(path,'r')
        except:
            return False
        return True    