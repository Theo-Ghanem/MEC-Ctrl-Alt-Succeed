import numpy as np


def create_hexcqi_lut():
    """
    create a lookup table for hex cqi values
    """
    global hexcqi_lut
    hexcqi_lut = {}

    # add 0-9 values
    for i in range(0, 10):
        hexcqi_lut[str(i)] = f"{i:05b}"

    # add a-f values
    for char in 'abcdef':
        hexcqi_lut[char] = f"{ord(char) - 87:05b}"

    # add CQI value
    hexcqi_lut['CQI'] = f"{16:05b}"

    # add CQI values 0-9
    for i in range(0, 10):
        hexcqi_lut[f'CQI{i}'] = f"{16 + i + 1:05b}"

    # add CQI values a-f
    for char in 'abcdef':
        hexcqi_lut[f'CQI{char}'] = f"{16 + ord(char) - 87 + 1:05b}"


def get_input_file():
    return open('in.txt', 'r', encoding='utf-8')


def parse_line(input_line: str):
    """
    parse a line of input into convolution matrix and binary values
    """
    perm_matrix, hex_cqi = input_line.split(':')

    # convert string matrix to list of lists of square size
    matrix_size = int(len(perm_matrix) ** 0.5)
    perm_matrix = np.array(list(perm_matrix), dtype=int)
    perm_matrix = np.array([perm_matrix[i:i + matrix_size] for i in range(0, len(perm_matrix), matrix_size)], dtype=int)

    # invert permutation matrix
    inv_perm_matrix = np.linalg.inv(perm_matrix)

    return inv_perm_matrix, hex_cqi


def parse_hex_cqi(input: str):
    """
    parse hex cqi into binary value
    """
    print(f'Hex CQI Input:\n{input}') if verbose else None
    output = np.array([])
    input = iter(input)
    for char in input:
        if char == '\n':
            continue
        if char == 'C':  # CQI value - skip next two chars (Q, I) and read next char
            next(input)
            next(input)
            nxt = next(input)
            if nxt == 'C' or nxt == 'Q' or nxt == 'I': # manually add a repeated CQI value if there are two in a row
                bin_char = np.array(list(hexcqi_lut['CQI']))
                output = np.append(output, [bin_char.reshape(bin_char.size, -1)])
                next(input)
                next(input)

            char = f'CQI{nxt}' if nxt != 'C' and nxt != '\n' else 'CQI'
        bin_char = np.array(list(hexcqi_lut[char]))
        print(char, '->', bin_char) if verbose else None
        output = np.append(output, [bin_char.reshape(bin_char.size, -1)])

    return np.array([output]).flatten().astype(int)


def decode_bin(bin_vect, inv_perm_matrix):
    """
    decode a binary vector using inverse permutation matrix
    """
    output = ''
    perm_matrix_size = inv_perm_matrix.shape[0]
    perm_matrix_length = perm_matrix_size ** 2

    print(f'Inverse permutation matrix (n={perm_matrix_size}):\n{inv_perm_matrix}') if verbose else None

    # pad bin_vect with zeros if necessary
    if len(bin_vect) % perm_matrix_length != 0:
        print(f'Padding message from length {len(bin_vect)} to length ', flush=True, end='') if verbose else None
        bin_vect = np.append(bin_vect, np.zeros(perm_matrix_length - len(bin_vect) % perm_matrix_length))
        print(len(bin_vect)) if verbose else None

    print(f'Message:\n{bin_vect}') if verbose else None

    # iterate over bin_vect in chunks of perm_matrix_size
    for i in range(0, len(bin_vect), perm_matrix_length):
        message = bin_vect[i:i + perm_matrix_length].reshape(perm_matrix_size, perm_matrix_size).astype(int)
        chunk = inv_perm_matrix.dot(message).astype(int)
        output += ''.join(chunk.flatten().astype(str))
    print(f'Binary Output:\n{output}')
    return output


def parse_binary_to_ascii(bin_vect):
    """
    parse binary vector into ascii characters
    """
    chunks = [bin_vect[i:i + 8] for i in range(0, len(bin_vect), 8)]

    # Convert each chunk to decimal, and then to ASCII in utf-8 encoding
    ascii_output = ''.join([chr(int(chunk, 2)) for chunk in chunks])
    print(f'ASCII Output:\n{ascii_output}') if verbose else None
    return ascii_output

def iterate_lines(input_file):
    with open('out.txt', 'a') as f:
        for line in input_file:
            inv_perm_matrix, hex_cqi = parse_line(line)
            bin_vect = parse_hex_cqi(hex_cqi)
            decoded_bin = decode_bin(bin_vect, inv_perm_matrix)
            output = parse_binary_to_ascii(decoded_bin)
            # write output to file
            f.write(f'{output}\n')


def test_case():
    # Hello World! testcase
    inv_perm_matrix, hex_cqi = parse_line("0100000100101000:11d48ed9dCQIc6ab6c6147d845e586da03b9")
    bin_vect = parse_hex_cqi(hex_cqi)
    decoded_bin = decode_bin(bin_vect, inv_perm_matrix)
    parse_binary_to_ascii(decoded_bin)


if __name__ == '__main__':
    test = False
    verbose = False
    create_hexcqi_lut()

    if test:
        test_case()
    else:
        input_file = get_input_file()
        iterate_lines(input_file)
