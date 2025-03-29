# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from AI import sha256, hash_file

def main():
    print("=== CHƯƠNG TRÌNH MÃ HÓA SHA-256 ===")
    
    while True:
        print("\nChọn chức năng:")
        print("1. Mã hóa chuỗi")
        print("2. Mã hóa nội dung file")
        print("3. Thoát")
        
        choice = input("Lựa chọn của bạn (1-3): ")
        
        if choice == "1":
            text = input("Nhập chuỗi cần mã hóa: ")
            hash_result = sha256(text)
            print(f"Kết quả SHA-256: {hash_result}")
            
        elif choice == "2":
            file_path = input("Nhập đường dẫn đến file: ")
            hash_result = hash_file(file_path)
            print(f"Kết quả SHA-256: {hash_result}")
            
        elif choice == "3":
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
            
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn 1, 2 hoặc 3.")

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
