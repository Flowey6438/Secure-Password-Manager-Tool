import json
import os
import base64
from cryptography.fernet import Fernet
import random
import string

DATA_FILE = "passwords.json"
KEY_FILE = "key.key"

def generate_key():
    key = Fernet.generate_key()
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists(KEY_FILE):
        generate_key()
    with open(KEY_FILE, "rb") as key_file:
        return key_file.read()

def encrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.encrypt(data.encode()).decode()

def decrypt_data(data, key):
    fernet = Fernet(key)
    return fernet.decrypt(data.encode()).decode()

def load_passwords(key):
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            encrypted_data = file.read()
            return json.loads(decrypt_data(encrypted_data, key))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_passwords(passwords, key):
    encrypted_data = encrypt_data(json.dumps(passwords), key)
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        file.write(encrypted_data)

def generate_random_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))

def add_password(passwords, key, account, username, password=None):
    if not password:
        password = generate_random_password()
    passwords[account] = {"username": username, "password": password}
    save_passwords(passwords, key)
    print(f"密码已添加：账号 - {account}, 用户名 - {username}")

def view_passwords(passwords):
    if passwords:
        print("\n存储的密码：")
        for account, details in passwords.items():
            print(f"账号：{account} | 用户名：{details['username']} | 密码：{details['password']}")
    else:
        print("没有存储的密码。")

if __name__ == "__main__":
    key = load_key()
    passwords = load_passwords(key)
    print("欢迎使用密码管理器！")

    while True:
        print("\n请选择一个操作：")
        print("1. 添加新密码")
        print("2. 查看存储的密码")
        print("3. 生成随机密码")
        print("4. 退出")

        choice = input("请输入选项（1/2/3/4）：")

        if choice == "1":
            account = input("请输入账号名称：")
            username = input("请输入用户名：")
            use_random = input("是否生成随机密码？（y/n）：").lower() == 'y'
            password = None if use_random else input("请输入密码：")
            add_password(passwords, key, account, username, password)
        elif choice == "2":
            view_passwords(passwords)
        elif choice == "3":
            length = int(input("请输入随机密码长度（默认12）：") or 12)
            print(f"生成的随机密码：{generate_random_password(length)}")
        elif choice == "4":
            print("感谢使用密码管理器，再见！")
            break
        else:
            print("无效选项，请重新选择。")
