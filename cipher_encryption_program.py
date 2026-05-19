# ============================================================================
# ENCRYPTION AND DECRYPTION PROGRAM - Multiple Cipher Techniques
# ============================================================================

# CAESAR CIPHER: Shifts each letter by a fixed number
def caesar_encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            if char.isupper():
                char_position = ord(char) - ord('A')
                new_position = (char_position + shift) % 26
                encrypted_text += chr(ord('A') + new_position)
            else:
                char_position = ord(char) - ord('a')
                new_position = (char_position + shift) % 26
                encrypted_text += chr(ord('a') + new_position)
        else:
            encrypted_text += char
    return encrypted_text


def caesar_decrypt(text, shift):
    # Decrypt by reversing the shift value
    return caesar_encrypt(text, -shift)


# VIGENERE CIPHER: Uses a keyword to determine varying shifts for each letter
def vigenere_encrypt(text, keyword):
    encrypted_text = ""
    keyword_index = 0
    for char in text:
        if char.isalpha():
            key_char = keyword[keyword_index % len(keyword)].upper()
            shift = ord(key_char) - ord('A')
            if char.isupper():
                char_position = ord(char) - ord('A')
                new_position = (char_position + shift) % 26
                encrypted_text += chr(ord('A') + new_position)
            else:
                char_position = ord(char) - ord('a')
                new_position = (char_position + shift) % 26
                encrypted_text += chr(ord('a') + new_position)
            keyword_index += 1
        else:
            encrypted_text += char
    return encrypted_text


def vigenere_decrypt(text, keyword):
    # Decrypt by subtracting the keyword shifts instead of adding
    decrypted_text = ""
    keyword_index = 0
    for char in text:
        if char.isalpha():
            key_char = keyword[keyword_index % len(keyword)].upper()
            shift = ord(key_char) - ord('A')
            if char.isupper():
                char_position = ord(char) - ord('A')
                new_position = (char_position - shift) % 26
                decrypted_text += chr(ord('A') + new_position)
            else:
                char_position = ord(char) - ord('a')
                new_position = (char_position - shift) % 26
                decrypted_text += chr(ord('a') + new_position)
            keyword_index += 1
        else:
            decrypted_text += char
    return decrypted_text


# ROW TRANSPOSITION CIPHER
def row_transposition_encrypt(text, key):
    key_length = len(key)
    sorted_indices = sorted(range(key_length), key=lambda i: key[i])
    num_rows = (len(text) + key_length - 1) // key_length
    padded_text = text + ' ' * (num_rows * key_length - len(text))
    grid = [list(padded_text[row_index * key_length:(row_index + 1) * key_length]) for row_index in range(num_rows)]
    encrypted_text = ""
    for col_index in sorted_indices:
        for row_index in range(num_rows):
            encrypted_text += grid[row_index][col_index]
    return encrypted_text


def row_transposition_decrypt(text, key):
    # Rebuild the original text by reversing the column reordering
    key_length = len(key)
    sorted_indices = sorted(range(key_length), key=lambda i: key[i])
    num_rows = len(text) // key_length
    grid = [['' for _ in range(key_length)] for _ in range(num_rows)]
    text_index = 0
    for col_index in sorted_indices:
        for row_index in range(num_rows):
            grid[row_index][col_index] = text[text_index]
            text_index += 1
    decrypted_text = ""
    for row_index in range(num_rows):
        for col_index in range(key_length):
            decrypted_text += grid[row_index][col_index]
    return decrypted_text.rstrip()


# RAILFENCE CIPHER: Writes text in a zigzag pattern and reads line by line
def railfence_encrypt(text, num_rails):
    if num_rails == 1:
        return text
    rails = [[] for _ in range(num_rails)]
    rail_index = 0
    direction = 1
    for char in text:
        rails[rail_index].append(char)
        rail_index += direction
        if rail_index == num_rails - 1:
            direction = -1
        elif rail_index == 0:
            direction = 1
    return ''.join(''.join(rail) for rail in rails)


def railfence_decrypt(text, num_rails):
    # Map positions in zigzag pattern, fill with encrypted text, then read in zigzag order
    if num_rails == 1:
        return text
    rails = [[] for _ in range(num_rails)]
    rail_index = 0
    direction = 1
    for _ in range(len(text)):
        rails[rail_index].append(None)
        rail_index += direction
        if rail_index == num_rails - 1:
            direction = -1
        elif rail_index == 0:
            direction = 1
    text_index = 0
    for rail_idx in range(num_rails):
        for pos_idx in range(len(rails[rail_idx])):
            rails[rail_idx][pos_idx] = text[text_index]
            text_index += 1
    decrypted_text = ""
    rail_index = 0
    direction = 1
    rail_char_indices = [0] * num_rails
    for _ in range(len(text)):
        decrypted_text += rails[rail_index][rail_char_indices[rail_index]]
        rail_char_indices[rail_index] += 1
        rail_index += direction
        if rail_index == num_rails - 1:
            direction = -1
        elif rail_index == 0:
            direction = 1
    return decrypted_text


# ============================================================================
# HYBRID CIPHERS: Combine two ciphers in sequence
# ============================================================================

# Vigenere + Caesar
def vigenereAndCaesarEncrypt(text, keyword, shift):
    return caesar_encrypt(vigenere_encrypt(text, keyword), shift)


def vigenereAndCaesarDecrypt(text, keyword, shift):
    # Reverse order: decrypt Caesar first, then Vigenere
    return vigenere_decrypt(caesar_decrypt(text, shift), keyword)


# Vigenere + Railfence
def VigenereAndRailfenceEncrypt(text, keyword, num_rails):
    return railfence_encrypt(vigenere_encrypt(text, keyword), num_rails)


def vigenereAndRailfenceDecrypt(text, keyword, num_rails):
    # Reverse order: decrypt Railfence first, then Vigenere
    return vigenere_decrypt(railfence_decrypt(text, num_rails), keyword)


# Vigenere + Row Transposition
def vigenereAndRowTranspositionEncrypt(text, keyword, key):
    return row_transposition_encrypt(vigenere_encrypt(text, keyword), key)


def vigenereAndRowTranspositionDecrypt(text, keyword, key):
    # Reverse order: decrypt Row Transposition first, then Vigenere
    return vigenere_decrypt(row_transposition_decrypt(text, key), keyword)


# Caesar + Railfence
def ceasarAndRailfenceEncrypt(text, shift, num_rails):
    return railfence_encrypt(caesar_encrypt(text, shift), num_rails)


def caesarAndRailfenceDecrypt(text, shift, num_rails):
    # Reverse order: decrypt Railfence first, then Caesar
    return caesar_decrypt(railfence_decrypt(text, num_rails), shift)


# Caesar + Row Transposition
def ceasarAndRowTranspositionEncrypt(text, shift, key):
    return row_transposition_encrypt(caesar_encrypt(text, shift), key)


def caesarAndRowTranspositionDecrypt(text, shift, key):
    # Reverse order: decrypt Row Transposition first, then Caesar
    return caesar_decrypt(row_transposition_decrypt(text, key), shift)


# Row Transposition + Railfence
def rowTranspositionAndRailfenceEncrypt(text, key, num_rails):
    return railfence_encrypt(row_transposition_encrypt(text, key), num_rails)


def rowTranspositionAndRailfenceDecrypt(text, key, num_rails):
    # Reverse order: decrypt Railfence first, then Row Transposition
    return row_transposition_decrypt(railfence_decrypt(text, num_rails), key)


# ============================================================================
# USER INTERFACE MENUS
# ============================================================================

def display_main_menu():
    # Display main menu with cipher options
    print("\n" + "=" * 70)
    print("ENCRYPTION AND DECRYPTION PROGRAM")
    print("=" * 70)
    print("\nChoose a Cipher Type:")
    print("1. Caesar Cipher")
    print("2. Vigenere Cipher")
    print("3. Row Transposition Cipher")
    print("4. Railfence Cipher")
    print("5. Hybrid Ciphers")
    print("6. Exit")
    print("-" * 70)


def caesar_cipher_menu():
    # Handle Caesar cipher encryption/decryption
    print("\n" + "-" * 70)
    print("CAESAR CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    try:
        shift = int(input("Enter the shift value (1-25): ").strip())
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    if choice == "1":
        result = caesar_encrypt(text, shift)
        print(f"\nOriginal Text:  {text}")
        print(f"Shift Value:    {shift}")
        print(f"Encrypted Text: {result}")
    elif choice == "2":
        result = caesar_decrypt(text, shift)
        print(f"\nEncrypted Text: {text}")
        print(f"Shift Value:    {shift}")
        print(f"Decrypted Text: {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def vigenere_cipher_menu():
    # Handle Vigenere cipher encryption/decryption
    print("\n" + "-" * 70)
    print("VIGENERE CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    keyword = input("Enter the keyword: ").strip()
    if choice == "1":
        result = vigenere_encrypt(text, keyword)
        print(f"\nOriginal Text:  {text}")
        print(f"Keyword:        {keyword}")
        print(f"Encrypted Text: {result}")
    elif choice == "2":
        result = vigenere_decrypt(text, keyword)
        print(f"\nEncrypted Text: {text}")
        print(f"Keyword:        {keyword}")
        print(f"Decrypted Text: {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def row_transposition_cipher_menu():
    # Handle Row Transposition cipher encryption/decryption
    print("\n" + "-" * 70)
    print("ROW TRANSPOSITION CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    key = input("Enter the key (e.g., 3142): ").strip()
    if choice == "1":
        result = row_transposition_encrypt(text, key)
        print(f"\nOriginal Text:  {text}")
        print(f"Key:            {key}")
        print(f"Encrypted Text: {result}")
    elif choice == "2":
        result = row_transposition_decrypt(text, key)
        print(f"\nEncrypted Text: {text}")
        print(f"Key:            {key}")
        print(f"Decrypted Text: {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def railfence_cipher_menu():
    # Handle Railfence cipher encryption/decryption
    print("\n" + "-" * 70)
    print("RAILFENCE CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    try:
        num_rails = int(input("Enter the number of rails (2 or more): ").strip())
        if num_rails < 2:
            print("Number of rails must be at least 2!")
            return
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    if choice == "1":
        result = railfence_encrypt(text, num_rails)
        print(f"\nOriginal Text:   {text}")
        print(f"Number of Rails: {num_rails}")
        print(f"Encrypted Text:  {result}")
    elif choice == "2":
        result = railfence_decrypt(text, num_rails)
        print(f"\nEncrypted Text:  {text}")
        print(f"Number of Rails: {num_rails}")
        print(f"Decrypted Text:  {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def vigenereAndCaesarMenu():
    # Handle Vigenere + Caesar hybrid encryption/decryption
    print("\n" + "-" * 70)
    print("VIGENERE + CAESAR CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    keyword = input("Enter the Vigenere keyword: ").strip()
    try:
        shift = int(input("Enter the Caesar shift value: ").strip())
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    if choice == "1":
        result = vigenereAndCaesarEncrypt(text, keyword, shift)
        print(f"\nOriginal Text:     {text}")
        print(f"Vigenere Keyword:  {keyword}")
        print(f"Caesar Shift:      {shift}")
        print(f"Encrypted Text:    {result}")
    elif choice == "2":
        result = vigenereAndCaesarDecrypt(text, keyword, shift)
        print(f"\nEncrypted Text:    {text}")
        print(f"Vigenere Keyword:  {keyword}")
        print(f"Caesar Shift:      {shift}")
        print(f"Decrypted Text:    {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def vigenereAndRailfenceMenu():
    # Handle Vigenere + Railfence hybrid encryption/decryption
    print("\n" + "-" * 70)
    print("VIGENERE + RAILFENCE CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    keyword = input("Enter the Vigenere keyword: ").strip()
    try:
        num_rails = int(input("Enter the number of rails (2 or more): ").strip())
        if num_rails < 2:
            print("Number of rails must be at least 2!")
            return
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    if choice == "1":
        result = VigenereAndRailfenceEncrypt(text, keyword, num_rails)
        print(f"\nOriginal Text:     {text}")
        print(f"Vigenere Keyword:  {keyword}")
        print(f"Number of Rails:   {num_rails}")
        print(f"Encrypted Text:    {result}")
    elif choice == "2":
        result = vigenereAndRailfenceDecrypt(text, keyword, num_rails)
        print(f"\nEncrypted Text:    {text}")
        print(f"Vigenere Keyword:  {keyword}")
        print(f"Number of Rails:   {num_rails}")
        print(f"Decrypted Text:    {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def vigenereAndRowTranspositionMenu():
    # Handle Vigenere + Row Transposition hybrid encryption/decryption
    print("\n" + "-" * 70)
    print("VIGENERE + ROW TRANSPOSITION CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    keyword = input("Enter the Vigenere keyword: ").strip()
    key = input("Enter the Row Transposition key (e.g., 3142): ").strip()
    if choice == "1":
        result = vigenereAndRowTranspositionEncrypt(text, keyword, key)
        print(f"\nOriginal Text:     {text}")
        print(f"Vigenere Keyword:  {keyword}")
        print(f"Row Transpos Key:  {key}")
        print(f"Encrypted Text:    {result}")
    elif choice == "2":
        result = vigenereAndRowTranspositionDecrypt(text, keyword, key)
        print(f"\nEncrypted Text:    {text}")
        print(f"Vigenere Keyword:  {keyword}")
        print(f"Row Transpos Key:  {key}")
        print(f"Decrypted Text:    {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def caesarAndRailfenceMenu():
    # Handle Caesar + Railfence hybrid encryption/decryption
    print("\n" + "-" * 70)
    print("CAESAR + RAILFENCE CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    try:
        shift = int(input("Enter the Caesar shift value: ").strip())
        num_rails = int(input("Enter the number of rails (2 or more): ").strip())
        if num_rails < 2:
            print("Number of rails must be at least 2!")
            return
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    if choice == "1":
        result = ceasarAndRailfenceEncrypt(text, shift, num_rails)
        print(f"\nOriginal Text:     {text}")
        print(f"Caesar Shift:      {shift}")
        print(f"Number of Rails:   {num_rails}")
        print(f"Encrypted Text:    {result}")
    elif choice == "2":
        result = caesarAndRailfenceDecrypt(text, shift, num_rails)
        print(f"\nEncrypted Text:    {text}")
        print(f"Caesar Shift:      {shift}")
        print(f"Number of Rails:   {num_rails}")
        print(f"Decrypted Text:    {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def caesarAndRowTranspositionMenu():
    # Handle Caesar + Row Transposition hybrid encryption/decryption
    print("\n" + "-" * 70)
    print("CAESAR + ROW TRANSPOSITION CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    try:
        shift = int(input("Enter the Caesar shift value: ").strip())
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    key = input("Enter the Row Transposition key (e.g., 3142): ").strip()
    if choice == "1":
        result = ceasarAndRowTranspositionEncrypt(text, shift, key)
        print(f"\nOriginal Text:     {text}")
        print(f"Caesar Shift:      {shift}")
        print(f"Row Transpos Key:  {key}")
        print(f"Encrypted Text:    {result}")
    elif choice == "2":
        result = caesarAndRowTranspositionDecrypt(text, shift, key)
        print(f"\nEncrypted Text:    {text}")
        print(f"Caesar Shift:      {shift}")
        print(f"Row Transpos Key:  {key}")
        print(f"Decrypted Text:    {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def rowTranspositionAndRailfenceMenu():
    # Handle Row Transposition + Railfence hybrid encryption/decryption
    print("\n" + "-" * 70)
    print("ROW TRANSPOSITION + RAILFENCE CIPHER")
    print("-" * 70)
    print("1. Encrypt")
    print("2. Decrypt")
    choice = input("Choose operation (1 or 2): ").strip()
    text = input("Enter the text: ").strip()
    key = input("Enter the Row Transposition key (e.g., 3142): ").strip()
    try:
        num_rails = int(input("Enter the number of rails (2 or more): ").strip())
        if num_rails < 2:
            print("Number of rails must be at least 2!")
            return
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    if choice == "1":
        result = rowTranspositionAndRailfenceEncrypt(text, key, num_rails)
        print(f"\nOriginal Text:     {text}")
        print(f"Row Transpos Key:  {key}")
        print(f"Number of Rails:   {num_rails}")
        print(f"Encrypted Text:    {result}")
    elif choice == "2":
        result = rowTranspositionAndRailfenceDecrypt(text, key, num_rails)
        print(f"\nEncrypted Text:    {text}")
        print(f"Row Transpos Key:  {key}")
        print(f"Number of Rails:   {num_rails}")
        print(f"Decrypted Text:    {result}")
    else:
        print("Invalid choice! Please select 1 or 2.")


def hybrid_ciphers_menu():
    # Display hybrid cipher options and route to selected cipher
    print("\n" + "=" * 70)
    print("HYBRID CIPHERS - Combine Multiple Cipher Techniques")
    print("=" * 70)
    print("\nChoose a Hybrid Cipher Combination:")
    print("1. Vigenere + Caesar")
    print("2. Vigenere + Railfence")
    print("3. Vigenere + Row Transposition")
    print("4. Caesar + Railfence")
    print("5. Caesar + Row Transposition")
    print("6. Row Transposition + Railfence")
    print("7. Back to Main Menu")
    print("-" * 70)
    choice = input("Enter your choice (1-7): ").strip()
    if choice == "1":
        vigenereAndCaesarMenu()
    elif choice == "2":
        vigenereAndRailfenceMenu()
    elif choice == "3":
        vigenereAndRowTranspositionMenu()
    elif choice == "4":
        caesarAndRailfenceMenu()
    elif choice == "5":
        caesarAndRowTranspositionMenu()
    elif choice == "6":
        rowTranspositionAndRailfenceMenu()
    elif choice == "7":
        return
    else:
        print("Invalid choice! Please select 1-7.")


# Main program execution
if __name__ == "__main__":
    while True:
        display_main_menu()
        choice = input("Enter your choice (1-6): ").strip()
        if choice == "1":
            caesar_cipher_menu()
        elif choice == "2":
            vigenere_cipher_menu()
        elif choice == "3":
            row_transposition_cipher_menu()
        elif choice == "4":
            railfence_cipher_menu()
        elif choice == "5":
            hybrid_ciphers_menu()
        elif choice == "6":
            print("\n" + "=" * 70)
            print("Thank you for using the Encryption Program!")
            print("=" * 70)
            break
        else:
            print("Invalid choice! Please select 1-6.")
        continue_choice = input("\nDo you want to continue? (yes/no): ").strip().lower()
        if continue_choice != "yes" and continue_choice != "y":
            print("\n" + "=" * 70)
            print("Thank you for using the Encryption Program!")
            print("=" * 70)
            break
