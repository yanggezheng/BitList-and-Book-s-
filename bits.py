# Part 1 goes here!
class DecodeError(Exception):
    pass


class ChunkError(Exception):
    pass


class BitList:
    def __init__(self, data):
        for ch in data:
            if ch not in ('0', '1'):
                raise ValueError(
                    'Format is invalid; does not consist of only 0 and 1')
        self.bits = data

    def __eq__(self, other):
        return self.bits == other.bits

    @staticmethod
    def from_ints(*args):
        bits = ''.join(str(bit) for bit in args)
        for char in bits:
            if char not in ('0', '1'):
                raise ValueError(
                    'Format is invalid; does not consist of only 0 and 1')
        return BitList(bits)

    def __str__(self):
        return self.bits

    def arithmetic_shift_left(self):
        self.bits = self.bits[1:] + '0'

    def arithmetic_shift_right(self):
        leftmost_bit = self.bits[0]
        self.bits = leftmost_bit + self.bits[:-1]

    def bitwise_and(self, other):
        if len(self.bits) != len(other.bits):
            raise ValueError(
                'a bitwise and can only be performed if both sequences of bits are of equal length')
        result = ''
        for i in range(len(self.bits)):
            if self.bits[i] == '1' and other.bits[i] == '1':
                result += '1'
            else:
                result += '0'
        return BitList(result)

    
    def chunk(self, chunk_length):
        if chunk_length <= 0:
            raise ChunkError('Chunk length should be greater than 0')
        if len(self.bits) % chunk_length != 0:
            raise ChunkError('Chunk length should divide the bit length evenly')
        chunks = [self.bits[i:i+chunk_length] for i in range(0, len(self.bits), chunk_length)]
        return [[int(bit) for bit in chunk] for chunk in chunks]

    def decode(self, encoding='utf-8'):
        if encoding not in ('us-ascii', 'utf-8'):
            raise ValueError('unsupported encoding')

        if encoding == 'us-ascii':
            return ''.join(chr(int(self.bits[i:i+7], 2)) for i in range(0, len(self.bits), 7))

        decoded = ''
        i = 0
        while i < len(self.bits):
            leading_byte = self.bits[i:i+8]
            leading_byte_int = int(leading_byte, 2)
            num_bytes = 1
            if leading_byte[0] != '0':
                if leading_byte[:3] == '110':
                    num_bytes = 2
                elif leading_byte[:4] == '1110':
                    num_bytes = 3
                elif leading_byte[:5] == '11110':
                    num_bytes = 4
                else:
                    raise DecodeError('invalid leading byte')
                if i + 8*num_bytes > len(self.bits):
                    raise DecodeError('incomplete sequence')
                for j in range(1, num_bytes):
                    continuation_byte = self.bits[i+8*j:i+8*j+8]
                    if continuation_byte[0:2] != '10':
                        raise DecodeError('invalid continuation byte')
                temp = [self.bits[i:i+8] for i in range (0, len(self.bits), 8)]
                f = bytes([int(ele,2) for ele in temp])
                decoded = f.decode('utf-8')
                i += 8 * num_bytes
            else:
                decoded += chr(leading_byte_int)
                i += 8
        return decoded

