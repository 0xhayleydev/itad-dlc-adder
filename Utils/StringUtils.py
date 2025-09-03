import random
import string


class StringUtils(): # pylint: disable=too-few-public-methods

    @staticmethod
    def generate_string(length: int, valid_chars: str|None = None) -> str:
        if not valid_chars:
            valid_chars = string.ascii_letters + string.digits

        return ''.join(random.choices(valid_chars, k=length))
