import random
import string
from crypto_manager import crypto_manager

class HoneywordGenerator:
    """
    Generates honeywords that mimic the properties of the user's real password
    to make them indistinguishable to an attacker.
    """

    @staticmethod
    def generate(real_password: str, count: int = 19) -> list[str]:
        """
        Generates a list of fake passwords based on the real password's characteristics.
        """
        honeywords = []

        # Analyze the real password to mimic its characteristics
        length = len(real_password)

        # Determine the character set based on the real password
        chars = set()
        for char in real_password:
            # We add the character and its category to ensure the honeywords
            # feel "natural" relative to the real password
            chars.add(char)
            if char.isdigit():
                chars.update(string.digits)
            elif char.islower():
                chars.update(string.ascii_lowercase)
            elif char.isupper():
                chars.update(string.ascii_uppercase)
            else:
                chars.update(string.punctuation)

        # If password is too simple, ensure we have a reasonable pool of characters
        if not chars:
            chars = set(string.ascii_letters + string.digits)

        char_pool = "".join(chars)

        while len(honeywords) < count:
            # Generate a random word of the same length using the derived pool
            word = "".join(random.choices(char_pool, k=length))

            # Ensure the honeyword is NOT the real password
            if word != real_password:
                honeywords.append(word)

        return honeywords

# Singleton instance
honeyword_generator = HoneywordGenerator()
