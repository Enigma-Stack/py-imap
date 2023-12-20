import base64

def encode_to_64(sample_string: str):
    sample_string_bytes = sample_string.encode("ascii") 
    
    base64_bytes = base64.b64encode(sample_string_bytes) 
    base64_string = base64_bytes.decode("ascii") 

    return base64_string

def decode_from_64(sample_string: str):
    base64_string = sample_string
    base64_bytes = base64_string.encode("ascii") 
    
    sample_string_bytes = base64.b64decode(base64_bytes) 
    sample_string = sample_string_bytes.decode("ascii") 
    return sample_string

def encrypt(message,key):
    print(len(key))
    res = ''
    for i in range(len(message)):
        if ord(message[i])<48:
            if ord(key[i])>=97:
                res += chr((ord(message[i]) + ord(key[i]) - 140)%5 + 43)
            else:
                res += chr((ord(message[i]) + ord(key[i]) - 91)%5 + 43)
        elif 48<=ord(message[i])<=57:
            if ord(key[i])>=97:
                res += chr((ord(message[i]) + ord(key[i]) - 145)%10 + 48)
            else:
                res += chr((ord(message[i]) + ord(key[i]) - 96)%10 + 48)
        elif 60<=ord(message[i])<=63:
            if ord(key[i])>=97:
                res += chr((ord(message[i]) + ord(key[i]) - 157)%4 + 60)
            else:
                res += chr((ord(message[i]) + ord(key[i]) - 108)%4 + 60)
        elif 65<=ord(message[i])<=90:
            if ord(key[i])>=97:
                res += chr((ord(message[i]) + ord(key[i]) - 162)%26 + 65)
            else:
                res += chr((ord(message[i]) + ord(key[i]) - 113)%26 + 65)
        else:
            if ord(key[i])>=97:
                res += chr((ord(message[i]) + ord(key[i]) - 194)%26 + 97)
            else:
                res += chr((ord(message[i]) + ord(key[i]) - 145)%26 + 97)
    return res

def decrypt(message,key):
    res64 = ''
    for i in range(len(message)):
        if ord(message[i])<48:
            if ord(key[i])>=97:
                res64 += chr((ord(message[i]) - ord(key[i]) + 54)%5 + 43)
            else:
                res64 += chr((ord(message[i]) - ord(key[i]) + 5)%5 + 43)
        elif 48<=ord(message[i])<=57:
            if ord(key[i])>=97:
                res64 += chr((ord(message[i]) - ord(key[i]) + 49)%10 + 48)
            else:
                res64 += chr((ord(message[i]) - ord(key[i]))%10 + 48)
        elif 60<=ord(message[i])<=63:
            if ord(key[i])>=97:
                res64 += chr((ord(message[i]) - ord(key[i]) + 37)%4 + 60)
            else:
                res64 += chr((ord(message[i]) - ord(key[i]) - 12)%4 + 60)
        elif 65<=ord(message[i])<=90:
            if ord(key[i])>=97:
                res64 += chr((ord(message[i]) - ord(key[i]) + 32)%26 + 65)
            else:
                res64 += chr((ord(message[i]) - ord(key[i]) - 17)%26 + 65)
        else:
            if ord(key[i])>=97:
                res64 += chr((ord(message[i]) - ord(key[i]) + 26)%26 + 97)
            else:
                res64 += chr((ord(message[i]) - ord(key[i]) - 49)%26 + 97)
    return res64


# Test input 1 -> 'Good evening, fellow team members. Kindly test!! to see if this works pr0p3rlY and (&43[][]s[=-])
# input_message = input('Enter your message to encrypt: ')
# start = time.time()
# enc,key = encrypt(input_message)
# print(f'Encrypted message is {enc}')
# print(f'Key is {key}')
# message_64 = decrypt(enc,key)
# message = decrypt_from_64(message_64)
# end = time.time()
# print(f'Original message: {message}')
# print(f'Time taken {end-start}')

def main(inp):
    message_to_encrypt = inp
    # start = time.time()
    enc,key = encrypt(message_to_encrypt)
    # print(f'Encrypted message is {enc}')
    # print(f'Key is {key}')
    message_64 = decrypt(enc,key)
    message = decode_from_64(message_64)
    return message
    # end = time.time()
    # print(f'Original message: {message}')
    # print(f'Time taken {end-start}')

# main()