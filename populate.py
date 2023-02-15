import random
import hashlib
import binascii
import string

entries = 20
message_length = 10  # words

with open("wordlist.txt") as f:
    wordlist = f.read().split()

def generate_random_string(length):
    """Generate a random string of specified length."""
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def hash_message(message):
    """Return a SHA-256 hash of the message."""
    message_bytes = message.encode('utf-8')
    hash_bytes = hashlib.sha256(message_bytes).digest()
    return binascii.hexlify(hash_bytes).decode('utf-8')

for i in range(entries):
    message = ' '.join(random.sample(wordlist, message_length))
    random_string = generate_random_string(10)
    hashed_message = hash_message(random_string + message)
    print(f'{hashed_message}:{message}')
