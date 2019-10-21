import binascii
import random
import lfsr

# Takes a text and converts it to binary using ASCII encoding
def ASCII2bin(msg):
    M_i = []
    Mlen = len(msg)
    for i in range(0,Mlen):
        ascii_no = ord(msg[i])
        ascii_bin = bin(ascii_no)
        char_len = len(ascii_bin)
        if(char_len<9):
            for j in range(0,9-char_len):
                M_i.append(0)
        for j in range(2,char_len):
            M_i.append(int(ascii_bin[j]))
    return M_i

# Retransformation to see the decrypted message
def bin2ASCII(msg):
    res = list()
    for i in range(len(msg)//7):
        bins = msg[:7]
        str_bin = ''.join(str(x) for x in bins)
        res.append(chr(int(str_bin,2)))
        msg = msg[7:]
    return "".join(res)
