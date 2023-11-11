import numpy as np

def get_input_file():
    return open('in.txt', 'r')


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
    output = np.array([])
    input = iter(input)
    for char in input:
        if char == '\n':
            continue
        if char == 'C':  # CQI value - skip next two chars (Q, I) and read next char
            next(input)
            next(input)
            char = f'CQI{next(input)}'
        bin_char = np.array(list(hexcqi_lut[char]))
        print(char, '->', bin_char)
        output = np.append(output, [bin_char.reshape(bin_char.size, -1)])

    return np.array([output]).flatten().astype(int)


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


def parse_binary_to_ascii(bin_vect):
    """
    parse binary vector into ascii characters
    """
    # bin_vect = bin_vect.reshape(-1, 8)
    chunks = [bin_vect[i:i + 8] for i in range(0, len(bin_vect), 8)]

    # Convert each chunk to decimal, and then to ASCII
    ascii_str = ''.join([chr(int(chunk, 2)) for chunk in chunks])

    return ascii_str


def decode_bin(bin_vect, inv_perm_matrix):
    """
    decode a binary vector using inverse permutation matrix
    """
    output = ''
    perm_matrix_size = inv_perm_matrix.shape[0]
    perm_matrix_length = perm_matrix_size ** 2
    cols_per_row = np.ceil(len(bin_vect) / perm_matrix_size).astype(int)
    print(bin_vect, len(bin_vect), cols_per_row, type(bin_vect))

    # pad bin_vect with zeros if necessary
    if len(bin_vect) % perm_matrix_length != 0:
        print('padding', len(bin_vect))
        bin_vect = np.append(bin_vect, np.zeros(perm_matrix_length - len(bin_vect) % perm_matrix_length))
        print('padded', len(bin_vect))

    # iterate over bin_vect in chunks of perm_matrix_size
    for i in range(0, len(bin_vect), perm_matrix_length):
        message = bin_vect[i:i + perm_matrix_length].reshape(perm_matrix_size, perm_matrix_size).astype(int)
        chunk = np.matmul(inv_perm_matrix, message).astype(int)
        output += ''.join(chunk.flatten().astype(str))
    return output


def iterate_lines(input_file):
    for line in input_file:
        inv_perm_matrix, hex_cqi = parse_line(line)
        bin_vect = parse_hex_cqi(hex_cqi)
        decoded_bin = decode_bin(bin_vect, inv_perm_matrix)
        parse_binary_to_ascii(decoded_bin)


if __name__ == '__main__':
    input_file = get_input_file()
    create_hexcqi_lut()
    # iterate_lines(input_file)
    inv_perm_matrix, hex_cqi = parse_line("0100000100101000:11d48ed9dCQIc6ab6c6147d845e586da03b9")
    bin_vect = parse_hex_cqi(hex_cqi)
    decoded_bin = decode_bin(bin_vect, inv_perm_matrix)
    print(decoded_bin)
    print(parse_binary_to_ascii(decoded_bin))
