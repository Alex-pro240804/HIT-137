def process_string(input_str):
    numbers_str = ""
    letters_str = ""

    # Separate numbers and letters
    for char in input_str:
        if char.isdigit():
            numbers_str += char
        elif char.isalpha():
            letters_str += char

    # Extract even numbers and convert to ASCII values
    even_numbers = [int(numbers_str[i:i+1]) for i in range(len(numbers_str)) if int(numbers_str[i:i+1]) % 2 == 0]
    even_numbers_ascii = [ord(str(num)) for num in even_numbers]

    # Extract uppercase letters and convert to ASCII values
    uppercase_letters = [char for char in letters_str if char.isupper()]
    uppercase_ascii = [ord(char) for char in uppercase_letters]

    # Output the results
    print(f"Even numbers: {even_numbers}")
    print(f"Even numbers ASCII values: {even_numbers_ascii}")
    print(f"Uppercase letters: {uppercase_letters}")
    print(f"Uppercase letters ASCII values: {uppercase_ascii}")

# Example input string
input_str = "56awA198dsktr235207qVam145ss78fsg31O"

# Run the function
process_string(input_str)
