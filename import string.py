import string
import secrets

def get_user_input():
    # Get and validate password length
    while True:
        try:
            length = int(input("Enter password length: "))
            if length <= 0:
                print("❌ Length must be greater than 0.")
            else:
                break
        except ValueError:
            print("❌ Please enter a valid number.")

    # Character set selection
    include_letters = input("Include letters? (y/n): ").strip().lower() == 'y'
    include_numbers = input("Include numbers? (y/n): ").strip().lower() == 'y'
    include_symbols = input("Include symbols? (y/n): ").strip().lower() == 'y'

    # Ensure at least one character type is selected
    if not (include_letters or include_numbers or include_symbols):
        print("⚠ You must include at least one character type. Try again.\n")
        return get_user_input()

    return length, include_letters, include_numbers, include_symbols


def generate_password(length, use_letters, use_numbers, use_symbols):
    char_pool = ""
    if use_letters:
        char_pool += string.ascii_letters  # a-z + A-Z
    if use_numbers:
        char_pool += string.digits         # 0-9
    if use_symbols:
        char_pool += string.punctuation    # !"#$%&'()*+,-./...

    if not char_pool:
        raise ValueError("No characters available to generate password.")

    # Securely generate password
    password = ''.join(secrets.choice(char_pool) for _ in range(length))
    return password


if __name__ == "__main__":
    length, letters, numbers, symbols = get_user_input()
    password = generate_password(length, letters, numbers, symbols)
    print("\n✅ Generated Password:", password)
