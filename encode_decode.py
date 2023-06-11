import socket
import pandas as pd

def caesar(data, key, mode):
    alphabet = 'abcdefghijklmnopqrstuvwyzàáãâéêóôõíúçABCDEFGHIJKLMNOPQRSTUVWYZÀÁÃÂÉÊÓÕÍÚÇ'
    new_data = ''
    for c in data:
        index = alphabet.find(c)
        if index == -1:
            new_data += c
        else:
            new_index = index + key if mode == 1 else index - key
            new_index = new_index % len(alphabet)
            new_data += alphabet[new_index:new_index+1]
    return new_data

def asciiEncode(message):
    values = []
    for char in message:
        values.append(ord(char))
    return values

def asciiDecode(message):
    values = []
    for char in message:
        values.append(chr(char))
    return ''.join(values)

def binaryEncode(array):
    values = []
    bit_values = []
    
    for i in array:
        values.append(f'{i:08b}'.format(8))
    
    values = list(''.join(values))

    for bit in values:
        bit_values.append(int(bit))

    return bit_values

def binaryDecode(array):
    #printar grafico aqui
    string_ints = [str(int) for int in array]
    string_ints = ''.join(string_ints)
    values = []
    # splits the string into an array containing substrings with the fixed length of (size of 1 byte)
    ascii_array =  [string_ints[i:i+8] for i in range(0, len(string_ints), 8)] 
    for i in ascii_array:
        values.append(int(i,2))
    return values

def Encode8B6T(message):
    message = binaryDecode(message)
    message = asciiDecode(message)
    encoded = ''
    table = pd.read_csv('8b6tTABLE.csv')
    table.fillna(' ', inplace = True)
    for i in range(len(message)):
        for j in range(len(table)):
            if(table['Char'].iloc[j] == message[i]):    
                encoded = encoded + flip(table['6T'].iloc[j])
    return encoded


def Decode8B6T(message):
    decoded = ''
    table = pd.read_csv('8b6tTABLE.csv')
    table.fillna(' ', inplace = True)
    i = 0
    k = 6
    for k in range(len(message)):
        for j in range(len(table)):
            if(table['6T'].iloc[j] == flip(message[0:6])):
                decoded = decoded + table['Char'].iloc[j]   
                message = message[6:]
    decoded = asciiEncode(decoded)
    decoded = binaryEncode(decoded)

    return decoded

def flip(data):
    flipped = ''
    counter = 0
    for i in range(len(data)):
        if data[i] == '+':
            flipped = flipped + '-'
            counter += 1
        elif data[i] == '-':
            flipped = flipped + '+'
            counter -= 1
        else:
            flipped = flipped + '0'
    if counter >= 1:
        return flipped
    if counter <= -1:
        return flipped
    else: return data

def encode(message):
    text_to_ceaser = caesar(message,5,1)
    ceaser_to_ascii = asciiEncode(text_to_ceaser)
    ascii_to_binary = binaryEncode(ceaser_to_ascii)
    binary_to_8B6T = Encode8B6T(ascii_to_binary)

    return binary_to_8B6T

def decode(message):
    EightB6T_to_binary = Decode8B6T(message)
    binary_to_ascii = binaryDecode(EightB6T_to_binary)
    ascii_to_ceaser = asciiDecode(binary_to_ascii)
    ceaser_to_text = caesar(ascii_to_ceaser,5,0)

    return ceaser_to_text

def get_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # doesn't even have to be reachable
            s.connect(('10.254.254.254', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP