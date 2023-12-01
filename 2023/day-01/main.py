import string
import sys

english_digits = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}

def main(input_file):
    numbers = []
    for line in input_file:
        digits = []
        while line:
            for word, digit in english_digits.items():
                if line.startswith(word):
                    line = line[len(word):]
                    digits.append(digit)
                    break
            else:
                ch, line = line[0], line[1:]
                if ch in string.digits:
                    digits.append(ch)

        numbers.append(int(digits[0] + digits[-1]))
        
    print(sum(numbers))


if __name__ == "__main__":
    main(sys.stdin)
