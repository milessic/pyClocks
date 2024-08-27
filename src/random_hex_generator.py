from random import choices
from string import ascii_uppercase, digits
def generate_random_hex():
    return "#" + "".join(choices(digits + ascii_uppercase[:6], k=6))

if __name__ == "__main__":
    print("Random 10 hex colours")
    for _ in range(10):
        print(generate_random_hex())

