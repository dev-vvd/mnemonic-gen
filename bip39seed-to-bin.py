with open('english.txt') as file:
    word_list = [w.strip() for w in file.readlines()]
print(word_list)
print("list length: " + str(len(word_list)) + " words")

mnemonic = input("Type a BIP39 mnemonic for binary value: ")

seed_bin_lst = []
for i in mnemonic.split():
    # print(word_list.index(i))
    seed_bin_lst.append(bin(word_list.index(i))[2:].zfill(11))

seed_as_bin = "".join(seed_bin_lst)
print("seed_as_bin: "+seed_as_bin)
print("len: "+str(len(seed_as_bin)))
