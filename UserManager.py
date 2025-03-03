import random

from User import User


class UserManager:
    USERS_FILE_PATH = "Users.txt"

    def __init__(self):
        self.users = self.load_users_from_file()

    def load_users_from_file(self):
        """Tải danh sách người dùng từ file"""
        users = []
        try:
            with open(self.USERS_FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split("|")
                    if len(data) >= 10:
                        users.append(User(*data[:9], int(data[9])))
        except FileNotFoundError:
            pass
        return users

    def save_users_to_file(self):
        """Lưu danh sách người dùng vào file"""
        with open(self.USERS_FILE_PATH, "w", encoding="utf-8") as file:
            for user in self.users:
                file.write(self.to_string(user) + "\n")

    def is_email_exist(self, email):
        return any(user.email == email for user in self.users)

    def is_username_exist(self, username):
        return any(user.username == username for user in self.users)

    def suggest_username(self, base_username):
        base = base_username.lower().replace(" ", "_")
        count = 1
        suggested = base
        while self.is_username_exist(suggested):
            suggested = f"{base}{count}"
            count += 1
        return suggested

    def suggest_password(self):
        chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        return ''.join(random.choice(chars) for _ in range(8))

    def register(self, ho_va_ten, ngay_sinh, gioi_tinh, CCCD, email, sdt, tai_khoan_ngan_hang, username, password):
        if self.is_email_exist(email):
            return "Email đã tồn tại!", None, None

        if self.is_username_exist(username):
            suggested_username = self.suggest_username(username)
            suggested_password = self.suggest_password()
            return "Username đã tồn tại!", suggested_username, suggested_password

        new_user = User(ho_va_ten, ngay_sinh, gioi_tinh, CCCD, email, sdt, tai_khoan_ngan_hang, username, password,balance= 100000)
        self.users.append(new_user)
        self.save_users_to_file()
        return "Đăng ký thành công!", None, None

    def to_string(self, user):
        return f"{user.ho_va_ten}|{user.ngay_sinh}|{user.gioi_tinh}|{user.CCCD}|{user.email}|{user.sdt}|" \
               f"{user.tai_khoan_ngan_hang}|{user.username}|{user.password}|{user.balance}"

    def login(self, username, password):
        """Kiểm tra đăng nhập"""
        for user in self.users:
            if user.username == username and user.password == password:
                return True, user
        return False, None