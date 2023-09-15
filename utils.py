""" Utils.py module is there to store the helper functions """

## Imports

## Functions

# Conversion of a list of integers between 0 and 5 from and to Base64

def baseX_to_baseY(num_str, base_x, base_y):
    """Convert a number from base-x to base-y using string manipulation."""

    chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ+/"
    char_to_int = {char: i for i, char in enumerate(chars)}

    num_base10 = 0
    for digit in num_str:
        num_base10 = num_base10 * base_x + char_to_int[digit]

    if num_base10 == 0:
        return "0"

    num_baseY = ""
    while num_base10 > 0:
        num_base10, remainder = divmod(num_base10, base_y)
        num_baseY = chars[remainder] + num_baseY

    return num_baseY

def list_to_base64(lst):
    """Convert a list of integers [0, 5] to a base-64 string."""

    # Add a sentinel value '6' to preserve leading zeros
    lst_with_sentinel = [6] + lst
    num_base7 = ''.join(map(str, lst_with_sentinel))
    return baseX_to_baseY(num_base7, 7, 64)

def base64_to_list(base64_str):
    """Convert a base-64 string to a list of integers [0, 5]."""

    num_base7 = baseX_to_baseY(base64_str, 64, 7)
    # Remove the sentinel value '6' to get the original list
    return [int(digit) for digit in num_base7[1:]]
