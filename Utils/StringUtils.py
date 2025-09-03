import random
import string


class StringUtils():
    @staticmethod
    def generate_string(length: int) -> str:
        valid_chars = string.ascii_letters + string.digits
        return ''.join(random.choices(valid_chars, k=length))