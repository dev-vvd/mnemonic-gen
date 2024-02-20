from xmr import word_list

print(str("Monero word list: " + str(len(word_list))))
print(word_list)
xmr_mnemonic = input("Type a XMR 25-word seed: ")

seed_bin_lst = []
for i in xmr_mnemonic.split():
    print("index: " + str(word_list.index(i)))
    seed_bin_lst.append(bin(word_list.index(i))[2:].zfill(11))

seed_as_bin = "".join(seed_bin_lst)
print("seed_as_bin: "+seed_as_bin)
print("seed_as_bin(len): " + str(len(seed_as_bin)))

