import sys

def shift_letter(ascii_code: int, shift: int) -> int:
    return ((ascii_code - ord('a') + shift) % 26) + ord('a')

def caesar_cipher(text: str, shift: int) -> str:
    text_list = list(text)
    for i in range(len(text_list)):
        code = ord(text_list[i])
        if code > 127:
            raise Exception("The script does not support your language yet.")
        elif 'a' <= text_list[i] <= 'z':
            text_list[i] = chr(shift_letter(code, shift))
    return ''.join(text_list)

def main():
    if len(sys.argv) != 4:
        raise Exception("Invalid number of arguments")

    action = sys.argv[1]
    text = sys.argv[2]
    shift = int(sys.argv[3])

    if action == "encode":
        print(caesar_cipher(text, shift))
    elif action == "decode":
        print(caesar_cipher(text, -shift))
    else:
        raise Exception("Please enter 'encode' or 'decode'.")

if __name__ == "__main__":
    main()
