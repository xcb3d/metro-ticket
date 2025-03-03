class User:
    def __init__(self, ho_va_ten , ngay_sinh,gioi_tinh, CCCD, email, sdt, tai_khoan_ngan_hang, username, password, balance):

        self.ho_va_ten = ho_va_ten
        self.ngay_sinh = ngay_sinh
        self.gioi_tinh = gioi_tinh

        self.CCCD = CCCD
        self.email = email
        self.sdt = sdt

        self.tai_khoan_ngan_hang = tai_khoan_ngan_hang
        self.username = username
        self.password = password

        self.balance = balance
