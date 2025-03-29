from param.ipython import message

# Các hằng số ban đầu (Các số nguyên tố 8 byte đầu tiên)
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]

# Giá trị băm ban đầu (Các số nguyên tố 4 byte đầu tiên)
H0 = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

def rotate_right(value, shift):
    """Xoay xâu nhị phân value, shift bit sang phải"""
    # value >> shift : dịch phải shift vị trí
    # value << shift : dịch trái 32 - shift vị trí
    #  & 0xFFFFFFFF: AND với giá trị 0xFFFFFFFF(32 bit 1) => đảm bảo xâu luôn có 32 bit, bit thừa bị loại bỏ
    return ( (value >> shift) | (value << (32 - shift)) ) & 0xFFFFFFFF

def ch(e, f, g):
    """Hàm ch = (e and f) xor ((not e) and g)"""
    return (e & f) ^ (~e & g)

def maj(a, b, c):
    """Hàm đa số maj = (a and b) xor (a and c) xor (b and c)"""
    #Tại mỗi vị trí bit, nếu ít nhất hai trong ba chuỗi(a,b,c) có bit là 1,thì kết quả tại vị trí đó trong hàm maj cũng sẽ là 1
    return (a & b) ^ (a &  c) ^ ( b & c)

def gamma0(x):
    """s0 = (w[i-15] rightrotate 7) xor (w[i-15] rightrotate 18) xor (w[i-15] rightshift 3)"""
    return rotate_right(x, 7) ^ rotate_right(x, 18) ^ (x >> 3)

def gamma1(x):
    """s1 = (w[i- 2] rightrotate 17) xor (w[i- 2] rightrotate 19) xor (w[i- 2] rightshift 10)"""
    return rotate_right(x, 17) ^ rotate_right(x, 19) ^ (x >> 10)

def sigma0(x):
    """S0 = (a rightrotate 2) xor (a rightrotate 13) xor (a rightrotate 22)"""
    return rotate_right(x, 2) ^ rotate_right(x, 13) ^ rotate_right(x, 22)

def sigma1(x):
    """S1 = (e rightrotate 6) xor (e rightrotate 11) xor (e rightrotate 25)"""
    return rotate_right(x, 6) ^ rotate_right(x, 11) ^ rotate_right(x, 25)

def step_1(text):
    """Bước 1: chuyển xâu sang nhị phân -> thêm 1 bit 1 -> thêm bit 0 -> thêm 64 bit đại diện độ dài"""
    #Chuyển xâu sang chuỗi byte
    text = text.encode('utf-8')

    #Nối 10000000 vào chuỗi
    padded_text = bytearray(text)
    padded_text.append(0x80) #0x80 = 10000000 trong nhị phân

    #Nối 0 cho đến khi là bội số của 512, nhưng trừ 64 bit
    while ( len(padded_text) * 8) % 512 != 448:
        padded_text.append(0x00)

    #Thêm 64 bit big-endian đại diện độ dài đầu vào ở dạng nhị phân của text
    original_length = len(text) * 8
    for i in range(8):
        padded_text.append( (original_length >> (56 - i * 8)) & 0xFF )

    return padded_text

def step_2(padded_text):
    """Tạo lịch trình tin nhắn"""
    #Sao chép dữ liệu từ bước 1 vào mảng mới, trong đó mỗi mục là 32 bit => mỗi phần từ là 64 bit => 512 bit
    blocks = []
    for i in range(0, len(padded_text), 64):
        blocks.append(padded_text[i:i + 64])

    #Khởi tạo giá trị băm
    h0, h1, h2, h3, h4, h5, h6, h7 = H0

    for block in blocks:
        w = [0] * 64

        #Sao chép khối vào 16 từ (512 bit : dữ liệu + độ dài) đầu tiên
        for i in range(16):
            w[i] = int.from_bytes(block[i * 4: (i + 1) * 4], byteorder='big')

        #Mở rộng lịch tin nhắn
        for i in range(16, 64):
            """s0 = (w[i-15] rightrotate 7) xor (w[i-15] rightrotate 18) xor (w[i-15] rightshift 3)
                s1 = (w[i- 2] rightrotate 17) xor (w[i- 2] rightrotate 19) xor (w[i- 2] rightshift 10)
                w[i] = w[i-16] + s0 + w[i-7] + s1"""
            w[i] = ( w[i-16] + gamma0(i-15) + w[i-7] + gamma1(i-2) ) & 0xFFFFFFFF

        #Khởi tạo biến
        a, b, c, d, e, f, g, h = h0, h1, h2, h3, h4, h5, h6, h7
        #Vòng lặp nén chính
        for i in range(64):
            temp1 = (h + sigma1(e) + ch(e, f, g) + K[i] + w[i]) & 0xFFFFFFFF
            temp2 = (sigma0(e) + maj(a, b, c)) & 0xFFFFFFFF

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xFFFFFFFF
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xFFFFFFFF

        #Thêm giá trị vào hash hiện tại
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF
        h5 = (h5 + f) & 0xFFFFFFFF
        h6 = (h6 + g) & 0xFFFFFFFF
        h7 = (h7 + h) & 0xFFFFFFFF

    #Nối các giá trị hash => kết quả cuối
    digest = ""
    for h in [h0, h1, h2, h3, h4, h5, h6, h7]:
        digest += format(h, '08x')

    return digest

if __name__ == '__main__':
    text = input("Nhập xâu cần mã hóa")
    padded_text = step_1(text)
    digest = step_2(padded_text)
    print(digest)

