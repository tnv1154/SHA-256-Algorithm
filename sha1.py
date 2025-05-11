# Các hằng số ban đầu cho SHA-1
H0 = [
    0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0
]

def rotate_left(value, shift):
    """Xoay xâu nhị phân value, shift bit sang trái"""
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def ch(e, f, g):
    """Hàm ch = (e and f) xor ((not e) and g)"""
    return (e & f) ^ (~e & g)

def parity(a, b, c):
    """Hàm tính parity = a xor b xor c """
    return a ^ b ^ c

def maj(a, b, c):
    """Hàm đa số maj = (a and b) xor (a and c) xor (b and c)"""
    return (a & b) ^ (a & c) ^ (b & c)

def step_1(text):
    """Bước 1: chuyển xâu sang nhị phân -> thêm 1 bit 1 -> thêm bit 0 -> thêm 64 bit đại diện độ dài"""
    # Chuyển xâu sang chuỗi byte
    text = text.encode('utf-8')

    # Nối 10000000 vào chuỗi
    padded_text = bytearray(text)
    padded_text.append(0x80)  # 0x80 = 10000000 trong nhị phân

    # Nối 0 cho đến khi là bội số của 512, nhưng trừ 64 bit
    while (len(padded_text) * 8) % 512 != 448:
        padded_text.append(0x00)

    # Thêm 64 bit big-endian đại diện độ dài đầu vào ở dạng nhị phân của text
    original_length = len(text) * 8
    for i in range(8):
        padded_text.append((original_length >> (56 - i * 8)) & 0xFF)

    return padded_text

def step_2(padded_text):
    """Tạo lịch trình tin nhắn và thực hiện SHA-1"""
    # Sao chép dữ liệu từ bước 1 vào mảng mới, trong đó mỗi mục là 32 bit => mỗi khối là 64 byte => 512 bit
    blocks = []
    for i in range(0, len(padded_text), 64):
        blocks.append(padded_text[i:i + 64])

    # Khởi tạo giá trị băm
    h0, h1, h2, h3, h4 = H0

    for block in blocks:
        w = [0] * 80

        # Sao chép khối vào 16 từ (512 bit) đầu tiên
        for i in range(16):
            w[i] = int.from_bytes(block[i * 4: (i + 1) * 4], byteorder='big')

        # Mở rộng lịch tin nhắn cho SHA-1
        for i in range(16, 80):
            w[i] = rotate_left(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)

        # Khởi tạo biến
        a, b, c, d, e = h0, h1, h2, h3, h4

        # Vòng lặp nén chính
        for i in range(80):
            if 0 <= i <= 19:
                f = ch(b, c, d)
                k = 0x5A827999
            elif 20 <= i <= 39:
                f = parity(b, c, d)
                k = 0x6ED9EBA1
            elif 40 <= i <= 59:
                f = maj(b, c, d)
                k = 0x8F1BBCDC
            else:  # 60 <= i <= 79
                f = parity(b, c, d)
                k = 0xCA62C1D6

            temp = (rotate_left(a, 5) + f + e + k + w[i]) & 0xFFFFFFFF
            e = d
            d = c
            c = rotate_left(b, 30)
            b = a
            a = temp

        # Thêm giá trị vào hash hiện tại
        h0 = (h0 + a) & 0xFFFFFFFF
        h1 = (h1 + b) & 0xFFFFFFFF
        h2 = (h2 + c) & 0xFFFFFFFF
        h3 = (h3 + d) & 0xFFFFFFFF
        h4 = (h4 + e) & 0xFFFFFFFF

    # Nối các giá trị hash => kết quả cuối
    digest = ""
    for h in [h0, h1, h2, h3, h4]:
        digest += format(h, '08x')

    return digest

def sha1(text):
    padded_text = step_1(text)
    digest = step_2(padded_text)
    return digest

if __name__ == '__main__':
    text = input("Nhập xâu cần mã hóa: ")
    digest = sha1(text)
    print(f"SHA-1: {digest}")