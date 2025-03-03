class Train:
    def __init__(self, ma_tau, tuyen_tau, lo_trinh, lich_trinh, ghe_trong):
        self.ma_tau = ma_tau          # Mã tàu
        self.tuyen_tau = tuyen_tau    # Tuyến tàu
        self.lo_trinh = lo_trinh      # Lộ trình
        self.lich_trinh = lich_trinh  # Ngày giờ khởi hành
        self.ghe_trong = ghe_trong    # Số ghế trống