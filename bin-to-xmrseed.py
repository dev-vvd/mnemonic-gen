from xmr import word_list

print("binary to xmr mnemonic seed")
bin_data = input("Give a binary input: ")
seed = []
for i in range(len(bin_data) // 11):
    index = int(bin_data[i*11:(i+1)*11], 2)
    seed.append(word_list[index])

print(" ".join(seed))
print("count: "+str(len(bin_data) // 11) + " words")

