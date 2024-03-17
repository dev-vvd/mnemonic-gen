import binascii
import hashlib
import secrets

# 1. convert random bytes to hex.
# 2. calculate the SHA-256 hash of the random bytes.
# 3. bin(int(hex, 16))[2:].zfill(len(random_bytes) * 8) + bin(int(hashed_bytes, 16))[:len(random_bytes) * 8 // 32]
# 4. split binary result in groups of 11 bits.
# 5. convert every group of 11 bits to an int.
# 6. iterate bip39 wordlist with int value as index.

random_bytes = secrets.token_bytes(16)
print("random_bytes: "+str(random_bytes))
print("random_bytes len: "+str(len(random_bytes)))
print(int.from_bytes(random_bytes, 'big'))
random_hex = binascii.hexlify(random_bytes)
print("random_hex: "+str(random_hex))
hashed_bytes = hashlib.sha256(random_bytes).hexdigest()
print("SHA256 hashed_bytes: "+hashed_bytes)

print("random_hex_bin: " + str(bin(int(random_hex, 16))[2:].zfill(len(random_bytes) * 8)))
print("random_hex_bin len: " + str(len(bin(int(random_hex, 16))[2:].zfill(len(random_bytes) * 8))))
print("hashed_bytes_bin: " + str(bin(int(hashed_bytes, 16))[2:].zfill(256)))
print("checksum_bits: " + str(bin(int(hashed_bytes, 16))[2:].zfill(256)[:len(random_bytes) * 8 // 32]))
print("checksum_bits len: " + str(len(bin(int(hashed_bytes, 16))[2:][:len(random_bytes) * 8 // 32])))

bin_result = (
    bin(int(random_hex, 16))[2:].zfill(len(random_bytes) * 8)
    + bin(int(hashed_bytes, 16))[2:].zfill(256)[:len(random_bytes) * 8 // 32]
)

print("bin_result: "+str(bin_result))
print("bin_result len: "+str(len(bin_result)))

with open('english.txt') as file:
    word_list = [w.strip() for w in file.readlines()]

passphrase = []
for i in range(len(bin_result) // 11):
    # print(int(bin_result[i*11:(i+1)*11], 2))
    # print(bin_result[i*11:(i+1)*11])
    index = int(bin_result[i*11:(i+1)*11], 2)
    passphrase.append(word_list[index])

print(" ".join(passphrase))
print("passphrase count: "+str(len(passphrase)))

# random_bytes = b'o\xf9\\\xda]W\xb0\'\xc9h>\xaa\xba\x87D\xc3"E~\xfd\xc6j\x9a\xf9G\xfa\xdb\x06\xa7\xf8\xd8\xd0'
# mnemonic output: husband slab custom rival kitchen become certain amazing primary stage spell main cattle satoshi warfare snap online sketch wrong render heavy wise globe barely
# passphrase count: 24