import random

with open('english.txt') as file:
    word_list = [w.strip() for w in file.readlines()]
print(word_list)
print("list length: " + str(len(word_list)) + " words")

rand_words = []
for i in range(12):
    index = random.randint(0, len(word_list) - 1)
    rand_words.append(word_list[index])
print(" ".join(rand_words))

mnemonic = input("Type a BIP39 mnemonic for binary value: ")

seed_bin_lst = []
for i in mnemonic.split():
    # print(word_list.index(i))
    seed_bin_lst.append(bin(word_list.index(i))[2:].zfill(11))

seed_as_bin = "".join(seed_bin_lst)
seed_as_int = int(seed_as_bin, 2)
print("seed_as_bin: "+seed_as_bin)
print("len: "+str(len(seed_as_bin)))
print("seed_as_int: "+str(seed_as_int))
print("len: "+str(len(str(seed_as_int))))
seed_as_hex = hex(seed_as_int)[2:]
print("seed_as_hex: "+seed_as_hex)
print("len: "+str(len(seed_as_hex)))
print("hex_to_int: "+str(int(seed_as_hex, 16)))
print("int_as_bin: "+bin(int(seed_as_hex, 16))[2:])
print("len: "+str(len(bin(int(seed_as_hex, 16))[2:])))
