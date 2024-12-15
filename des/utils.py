#utils.py
def int_to_bin(number: int, block_size=8) -> str:
    binary = bin(number)[2:]
    return '0' * (block_size - len(binary)) + binary


def char_2_num(letter: str) -> int:
    return ord(letter) - ord('a')


def num_2_char(number: int) -> str:
    return chr(ord('a') + number)


def mod(a, b):
    return a % b


def left_circ_shift(binary: str, shift: int) -> str:
    shift = shift % len(binary)
    return binary[shift:] + binary[0: shift]

def pad_string(message: str, block_size=64) -> str:
    binary_message = ''.join(f"{ord(char):08b}" for char in message)  
    padding_needed = block_size - (len(binary_message) % block_size)
    padded_binary_message = binary_message + '0' * padding_needed 
    return padded_binary_message

def bin_to_text(binary_string: str) -> str:
    text = ''.join(chr(int(binary_string[i:i+8], 2)) for i in range(0, len(binary_string), 8))
    return text.strip()  