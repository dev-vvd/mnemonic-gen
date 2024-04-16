import binascii
import hmac
import hashlib
import secrets
import unicodedata
import base58

# 1. convert random bytes to hex.
# 2. calculate the SHA-256 hash of the random bytes. (CHECKSUM)
# 3. bin(int(hex, 16))[2:].zfill(len(random_bytes) * 8) + bin(int(hashed_bytes, 16))[:len(random_bytes) * 8 // 32] (CHECKSUM)
# 4. split binary result in groups of 11 bits.
# 5. convert every group of 11 bits to an int.
# 6. iterate bip39 wordlist with int value as index.


def generate_mnemonic(entropy: bytes) -> str:
    print("entropy: " + str(entropy))
    entropy_hex = binascii.hexlify(entropy)
    print("entropy_hex: " + str(entropy_hex))
    hashed_entropy = hashlib.sha256(entropy).hexdigest()
    print("hashed_entropy: " + hashed_entropy)

    print("entropy_hex_bin: " + str(bin(int(entropy_hex, 16))[2:].zfill(len(entropy) * 8)))
    print("entropy_hex_bin len: " + str(len(bin(int(entropy_hex, 16))[2:].zfill(len(entropy) * 8))))
    print("hashed_entropy_bin: " + str(bin(int(hashed_entropy, 16))[2:].zfill(256)))
    print("checksum_bits: " + str(bin(int(hashed_entropy, 16))[2:].zfill(256)[:len(entropy) * 8 // 32]))
    print("checksum_bits len: " + str(len(bin(int(hashed_entropy, 16))[2:][:len(entropy) * 8 // 32])))

    bin_result = (
            bin(int(entropy_hex, 16))[2:].zfill(len(entropy) * 8)
            + bin(int(hashed_entropy, 16))[2:].zfill(256)[:len(entropy) * 8 // 32]
    )

    print("bin_result: " + str(bin_result))
    print("bin_result len: " + str(len(bin_result)))

    with open('english.txt') as file:
        word_list = [w.strip() for w in file.readlines()]

    passphrase = []
    for i in range(len(bin_result) // 11):
        # print(int(bin_result[i*11:(i+1)*11], 2))
        # print(bin_result[i*11:(i+1)*11])
        index = int(bin_result[i * 11:(i + 1) * 11], 2)
        passphrase.append(word_list[index])

    mnemonic = " ".join(passphrase)

    return mnemonic


def mnemonic_to_seed(mnemonic: str, passphrase: str = "") -> bytes:
    mnemonic = unicodedata.normalize("NFKD", mnemonic)
    passphrase = unicodedata.normalize("NFKD", passphrase)
    passphrase = "mnemonic" + passphrase
    mnemonic_bytes = mnemonic.encode('utf-8')
    passphrase_bytes = passphrase.encode('utf-8')
    seed = hashlib.pbkdf2_hmac('sha512', mnemonic_bytes, passphrase_bytes, 2048)
    return seed


# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#master-key-generation
# https://github.com/bitcoin/bips/blob/master/bip-0032.mediawiki#serialization-format
def seed_to_master_key(seed: bytes, testnet: bool = 'False') -> bytes:

    I = hmac.new(b'Bitcoin seed', seed, hashlib.sha512).digest()
    master_secret_key = I[:32]
    master_chain_code = I[32:]

    version_bytes = {
        'mainnet_public': binascii.unhexlify('0488b21e'),
        'mainnet_private': binascii.unhexlify('0488ade4'),
        'testnet_public': binascii.unhexlify('043587cf'),
        'testnet_private': binascii.unhexlify('04358394'),
    }
    xprv = version_bytes['mainnet_private']
    # print(xprv)
    if testnet:
        xprv = version_bytes['testnet_private']

    # depth(1byte), fingerprint(4bytes), child_num(4bytes)
    xprv += b'\x00' * 9
    # print(xprv)
    # chain code
    xprv += master_chain_code
    # print(xprv)
    # public key or private key data (serP(K) for public keys, 0x00 || ser256(k) for private keys)
    xprv += b'\x00' + master_secret_key
    # print(xprv)
    # double hash with SHA-256 for checksum bits
    hashed_xprv = hashlib.sha256(xprv).digest()
    hashed_xprv = hashlib.sha256(hashed_xprv).digest()

    checksum_bits = hashed_xprv[:4]
    # print(checksum_bits)
    xprv += checksum_bits

    return base58.b58encode(xprv)


def main():
    # random_bytes = secrets.token_bytes(32)
    random_bytes = b'o\xf9\\\xda]W\xb0\'\xc9h>\xaa\xba\x87D\xc3"E~\xfd\xc6j\x9a\xf9G\xfa\xdb\x06\xa7\xf8\xd8\xd0'
    mnemonic = generate_mnemonic(random_bytes)
    print(mnemonic)
    print("passphrase count: " + str(len(mnemonic.split())))
    seed = mnemonic_to_seed(mnemonic, "")
    print("seed: " + binascii.hexlify(seed).decode('utf-8'))
    print("master_key: " + seed_to_master_key(seed, False).decode('utf-8'))


if __name__ == "__main__":
    main()

# random_bytes = b'o\xf9\\\xda]W\xb0\'\xc9h>\xaa\xba\x87D\xc3"E~\xfd\xc6j\x9a\xf9G\xfa\xdb\x06\xa7\xf8\xd8\xd0'
# mnemonic output: husband slab custom rival kitchen become certain amazing primary stage spell main cattle satoshi warfare snap online sketch wrong render heavy wise globe barely
# passphrase count: 24