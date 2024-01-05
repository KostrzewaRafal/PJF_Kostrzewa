import random
import string

class KeyGenerator:
    def generate_key(self, length, seed=None):
        if seed is not None:
            random.seed(seed)

        characters = string.ascii_letters + string.digits 
        random_string = ''.join(random.choice(characters) for _ in range(length))
        KEYstring = f'{random_string}='
        KEY = bytes(KEYstring,'UTF-8')
        print(KEY)

        return KEY