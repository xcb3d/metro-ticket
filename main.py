import sys
from datetime import datetime

from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog, QTableWidgetItem, QLineEdit, QDateEdit, QLabel, QComboBox
from PyQt6.QtCore import QDate, QDateTime
from PyQt6.QtGui import QColor

from User import User
from UserManager import UserManager
from TrainManager import TrainManager
from TicketManager import TicketManager
from giaodien import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.manager = UserManager()
        self.train_manager = TrainManager()
        self.ticket_manager = TicketManager()
        
        # Khởi tạo danh sách ghế đã chọn và danh sách nút ghế
        self.selected_seats = []
        self.seat_buttons = []
        
        # Sửa lỗi tên nút ghế g12 (đang là pushButton_17)
        if hasattr(self.ui, "pushButton_17"):
            self.ui.pushButton_g12 = self.ui.pushButton_17
            self.ui.pushButton_g12.setObjectName("pushButton_g12")
        
        # Thiết lập trang đăng nhập là trang mặc định khi khởi động
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # Thiết lập focus vào trường mật khẩu khi chuyển đến trang đăng nhập
        self.ui.stackedWidget.currentChanged.connect(self.handle_page_change)

        # Thiết lập các giá trị cho comboBox tài khoản ngân hàng
        self.ui.comboBox_cs_tknh.addItems(["BIDV", "Vietcombank", "Agribank", "Techcombank", "VPBank", "MBBank"])
        
        # Thiết lập các giá trị cho comboBox phương thức thanh toán
        self.ui.comboBox_nt_pttt.addItems(["Thẻ tín dụng", "Thẻ ghi nợ", "Ví điện tử", "Chuyển khoản ngân hàng"])
        
        # Thiết lập chế độ ẩn mật khẩu
        self.ui.lineEdit_dkt_mkht.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.lineEdit_dmk_mkm.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.lineEdit_dmk_mktt.setEchoMode(QLineEdit.EchoMode.Password)
        self.ui.lineEdit_dp_pw.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Thay thế QLineEdit bằng QDateEdit cho ngày sinh trong trang chỉnh sửa thông tin
        # Lưu lại vị trí của QLineEdit
        grid_layout = self.ui.lineEdit_cs_ngay_sinh.parent().layout()
        position = grid_layout.indexOf(self.ui.lineEdit_cs_ngay_sinh)
        row, column, rowSpan, columnSpan = grid_layout.getItemPosition(position)
        
        # Xóa QLineEdit cũ
        self.ui.lineEdit_cs_ngay_sinh.setParent(None)
        
        # Tạo QDateEdit mới
        self.ui.dateEdit_cs_ngay_sinh = QDateEdit(parent=self.ui.gridLayoutWidget_9)
        self.ui.dateEdit_cs_ngay_sinh.setObjectName("dateEdit_cs_ngay_sinh")
        self.ui.dateEdit_cs_ngay_sinh.setDisplayFormat("yy/MM/dd")
        self.ui.dateEdit_cs_ngay_sinh.setCalendarPopup(True)  # Cho phép hiển thị lịch khi nhấp vào
        
        # Thêm QDateEdit vào vị trí cũ của QLineEdit
        grid_layout.addWidget(self.ui.dateEdit_cs_ngay_sinh, row, column, rowSpan, columnSpan)
        
        # Thay thế QLineEdit bằng QDateEdit cho ngày sinh trong trang đăng ký
        # Lưu lại vị trí của QLineEdit
        grid_layout_dk = self.ui.lineEdit_dk_ngay_sinh.parent().layout()
        position_dk = grid_layout_dk.indexOf(self.ui.lineEdit_dk_ngay_sinh)
        row_dk, column_dk, rowSpan_dk, columnSpan_dk = grid_layout_dk.getItemPosition(position_dk)
        
        # Xóa QLineEdit cũ
        self.ui.lineEdit_dk_ngay_sinh.setParent(None)
        
        # Tạo QDateEdit mới
        self.ui.dateEdit_dk_ngay_sinh = QDateEdit(parent=self.ui.gridLayoutWidget)
        self.ui.dateEdit_dk_ngay_sinh.setObjectName("dateEdit_dk_ngay_sinh")
        self.ui.dateEdit_dk_ngay_sinh.setDisplayFormat("yy/MM/dd")
        self.ui.dateEdit_dk_ngay_sinh.setCalendarPopup(True)  # Cho phép hiển thị lịch khi nhấp vào
        
        # Thêm QDateEdit vào vị trí cũ của QLineEdit
        grid_layout_dk.addWidget(self.ui.dateEdit_dk_ngay_sinh, row_dk, column_dk, rowSpan_dk, columnSpan_dk)

        # Thiết lập các giá trị cho comboBox trong trang tra cứu
        # Thêm các tuyến tàu vào comboBox
        self.ui.comboBox.addItem("Tất cả")
        self.ui.comboBox.addItems(self.train_manager.get_routes())
        
        # Thêm các ga vào comboBox ga xuất phát và ga đến
        self.ui.comboBox_tc_di.addItem("Tất cả")
        self.ui.comboBox_tc_den.addItem("Tất cả")
        self.ui.comboBox_tc_di.addItems(self.train_manager.stations)
        self.ui.comboBox_tc_den.addItems(self.train_manager.stations)
        
        # Thiết lập định dạng ngày giờ cho dateTimeEdit
        self.ui.dateTimeEdit.setDisplayFormat("yyyy-MM-dd HH:mm")
        self.ui.dateTimeEdit.setCalendarPopup(True)
        
        # Thiết lập ngày giờ hiện tại cho dateTimeEdit
        current_datetime = datetime.now()
        qt_datetime = QDateTime(
            current_datetime.year,
            current_datetime.month,
            current_datetime.day,
            current_datetime.hour,
            current_datetime.minute
        )
        self.ui.dateTimeEdit.setDateTime(qt_datetime)
        
        # Thiết lập các giá trị cho comboBox trong trang mua vé
        self.ui.comboBox_mv_tuyen_tau.clear()
        self.ui.comboBox_mv_tuyen_tau.addItem("Tất cả")
        self.ui.comboBox_mv_tuyen_tau.addItems(self.train_manager.get_routes())
        
        # Thiết lập định dạng ngày cho dateEdit_mv_ngay_di
        self.ui.dateEdit_mv_ngay_di.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateEdit_mv_ngay_di.setCalendarPopup(True)
        self.ui.dateEdit_mv_ngay_di.setDate(QDate(current_datetime.year, current_datetime.month, current_datetime.day))
        
        # Thiết lập các nút ghế
        self.setup_seat_buttons()
        
        # Kết nối nút trong đăng kí
        self.ui.pushButton_dk_dang_nhap.clicked.connect(self.go_to_login_page)
        self.ui.pushButton_dk_dang_ki.clicked.connect(self.register_user)

        # Kết nối nút trong đăng nhập
        self.ui.pushButton_dp_dp.clicked.connect(self.handle_login)
        self.ui.pushButton_dn_dk.clicked.connect(self.go_to_registration_page)

        # Kết nối nút trong Màn hình chính
        self.ui.pushButton_mhc_tc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton__mhc_mv.clicked.connect(self.go_to_buy_ticket_page)
        self.ui.pushButton_mhc_lsgd.clicked.connect(self.go_to_transaction_history_page)
        self.ui.pushButton_mhc_tk.clicked.connect(self.go_to_account_page)

        # Kết nối nút trong tra cứu
        self.ui.pushButton_tc_mhc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_tc_mv.clicked.connect(self.go_to_buy_ticket_page)
        self.ui.pushButton_tc_lsgd.clicked.connect(self.go_to_transaction_history_page)
        self.ui.pushButton_tc_tk.clicked.connect(self.go_to_account_page)
        self.ui.pushButton_tc_tc_2.clicked.connect(self.search_trains)

    #Kết nối nút trong mua vé
        self.ui.pushButton_ms_mhc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_mv_tc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_mv_lsgd.clicked.connect(self.go_to_transaction_history_page)
        self.ui.pushButton_mv_tk.clicked.connect(self.go_to_account_page)
        self.ui.pushButton_mv_mv_2.clicked.connect(self.buy_ticket)
        self.ui.pushButton_mv_mv_3.clicked.connect(self.reset_seat_selection)
        
        # Kết nối sự kiện thay đổi tuyến tàu
        self.ui.comboBox_mv_tuyen_tau.currentIndexChanged.connect(self.load_trains_for_route)
        
        # Kết nối sự kiện thay đổi chuyến tàu
        self.ui.comboBox_mv_chuyen.currentIndexChanged.connect(self.load_train_details)

        # Kết nối nút trong Lịch sử giao dịch
        self.ui.pushButton_lsgd_mhc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_lsgd_tc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_lsgd_mv.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.pushButton_lsgd_tk.clicked.connect(self.go_to_account_page)

        # Kết nối nút trong Thông tin tài khoản
        self.ui.pushButton_tk_mhc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.pushButton_tk_tc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.pushButton_tk_mv.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.pushButton_tk_lsgd.clicked.connect(self.go_to_transaction_history_page)
        self.ui.pushButton_tk_cstt.clicked.connect(self.go_to_edit_page)
        self.ui.pushButton_tk_nt.clicked.connect(self.go_to_deposit_page)
        self.ui.pushButton_tk_dmk.clicked.connect(self.go_to_change_password_page)
        self.ui.pushButton_tk_dang_xuat.clicked.connect(self.handle_logout)

        # kết nối nút chình sửa thông tin
        self.ui.pushButton_cs_back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))
        self.ui.pushButton_cs_luu.clicked.connect(self.save_user_info)

        # kết nối nút nạp tiền
        self.ui.pushButton_nt_back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))
        self.ui.pushButton_nt_xac_nhan.clicked.connect(self.deposit_money)

        # kết nối nút đổi mật khẩu
        self.ui.pushButton_dmk_back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))
        self.ui.pushButton_dmk_dmk.clicked.connect(self.change_password)

        # Cấu hình các widget lịch sử giao dịch
        self.ui.dateTimeEdit_lsgd_bd.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateTimeEdit_lsgd_bd.setCalendarPopup(True)
        self.ui.dateTimeEdit_lsgd_bd.setDateTime(QDateTime.currentDateTime().addDays(-30))  # Mặc định 30 ngày trước
        
        self.ui.dateTimeEdit_lsgd_kt.setDisplayFormat("dd/MM/yyyy")
        self.ui.dateTimeEdit_lsgd_kt.setCalendarPopup(True)
        self.ui.dateTimeEdit_lsgd_kt.setDateTime(QDateTime.currentDateTime())  # Mặc định ngày hiện tại
        
        # Thêm tùy chọn "Tất cả" vào comboBox trạng thái thanh toán
        self.ui.comboBox_lsgd_tttt.insertItem(0, "Tất cả")
        
        # Kết nối sự kiện thay đổi ngày để kiểm tra tính hợp lệ
        self.ui.dateTimeEdit_lsgd_bd.dateTimeChanged.connect(self.validate_transaction_date_range)
        self.ui.dateTimeEdit_lsgd_kt.dateTimeChanged.connect(self.validate_transaction_date_range)
        
        # Kết nối nút tìm kiếm
        self.ui.pushButton_lsgd_tim_kiem.clicked.connect(self.search_transactions)
        
        # Kết nối nút làm mới
        self.ui.pushButton_lsgd_tai.clicked.connect(self.load_transaction_history)

        # Kết nối sự kiện nhấn Enter trong các trường đăng nhập
        self.ui.lineEdit_dp_un.returnPressed.connect(lambda: self.ui.lineEdit_dp_pw.setFocus())
        self.ui.lineEdit_dp_pw.returnPressed.connect(self.handle_login)

        # Tạo comboBox cho mã tàu trong trang mua vé
        self.ui.comboBox_mv_ma_tau = QComboBox(parent=self.ui.page_muave)
        self.ui.comboBox_mv_ma_tau.setObjectName("comboBox_mv_ma_tau")
        
        # Đặt vị trí và kích thước cho comboBox mã tàu
        # Đặt ở trên comboBox tuyến tàu
        tuyen_tau_pos = self.ui.comboBox_mv_tuyen_tau.geometry()
        self.ui.comboBox_mv_ma_tau.setGeometry(
            tuyen_tau_pos.x(), 
            tuyen_tau_pos.y() - 40,  # Đặt phía trên comboBox tuyến tàu
            tuyen_tau_pos.width(), 
            tuyen_tau_pos.height()
        )
        
        # Thêm nhãn cho comboBox mã tàu
        self.ui.label_mv_ma_tau = QLabel(parent=self.ui.page_muave)
        self.ui.label_mv_ma_tau.setObjectName("label_mv_ma_tau")
        self.ui.label_mv_ma_tau.setText("Mã tàu:")
        self.ui.label_mv_ma_tau.setGeometry(
            self.ui.label_28.x(),  # Cùng tọa độ x với nhãn tuyến tàu
            self.ui.comboBox_mv_ma_tau.y(),  # Cùng tọa độ y với comboBox mã tàu
            self.ui.label_28.width(),
            self.ui.label_28.height()
        )
        
        # Thêm các mã tàu vào comboBox
        self.ui.comboBox_mv_ma_tau.addItem("Tất cả")
        self.ui.comboBox_mv_ma_tau.addItems(self.train_manager.get_train_code_prefixes())
        
        # Lấy vị trí của comboBox chuyến tàu
        chuyen_tau_pos = self.ui.comboBox_mv_chuyen.geometry()
        
        # Đảm bảo dateEdit hiển thị và đặt ở vị trí đúng
        self.ui.dateEdit_mv_ngay_di.setVisible(True)
        
        # Lấy gridLayout chứa các thành phần
        grid_layout = self.ui.gridLayoutWidget_5.layout()
        
        # Xóa các thành phần khỏi gridLayout
        grid_layout.removeWidget(self.ui.comboBox_mv_chuyen)
        grid_layout.removeWidget(self.ui.dateEdit_mv_ngay_di)
        grid_layout.removeWidget(self.ui.label_35)
        grid_layout.removeWidget(self.ui.label_29)
        
        # Thêm lại các thành phần vào gridLayout với vị trí mới
        # Thêm comboBox_mv_chuyen vào vị trí của dateEdit_mv_ngay_di (dòng 3)
        grid_layout.addWidget(self.ui.comboBox_mv_chuyen, 3, 2, 1, 1)
        # Thêm dateEdit_mv_ngay_di vào vị trí của comboBox_mv_chuyen (dòng 5)
        grid_layout.addWidget(self.ui.dateEdit_mv_ngay_di, 5, 2, 1, 1)
        # Thêm label_35 (Chọn chuyến tàu) vào vị trí của label_29 (dòng 3)
        grid_layout.addWidget(self.ui.label_35, 3, 0, 1, 1)
        # Thêm label_29 (Ngày đi) vào vị trí của label_35 (dòng 5)
        grid_layout.addWidget(self.ui.label_29, 5, 0, 1, 1)
        
        # Đổi tên label thành "Ngày đi:"
        self.ui.label_29.setText("Ngày đi:")
        
        # Ẩn comboBox thời gian nếu nó tồn tại
        if hasattr(self.ui, 'comboBox_mv_thoi_gian'):
            self.ui.comboBox_mv_thoi_gian.setVisible(False)
            # Xóa comboBox thời gian khỏi UI
            self.ui.comboBox_mv_thoi_gian.deleteLater()
            delattr(self.ui, 'comboBox_mv_thoi_gian')
        
        # Cập nhật giá vé
        self.update_ticket_price()
        
        # Tải danh sách chuyến tàu cho ngày đã chọn
        self.load_trains_for_route()
        
        # Kết nối sự kiện thay đổi mã tàu
        self.ui.comboBox_mv_ma_tau.currentIndexChanged.connect(self.load_trains_for_route)
        
        # Kết nối sự kiện thay đổi ngày đi
        self.ui.dateEdit_mv_ngay_di.dateChanged.connect(self.load_trains_for_route)

    def register_user(self):
        ho_va_ten = self.ui.lineEdit_dk_ho_va_ten.text()
        ngay_sinh = self.ui.dateEdit_dk_ngay_sinh.date().toString("yyyy-MM-dd")
        gioi_tinh = "Nam" if self.ui.radioButton_dk_nam.isChecked() else "Nữ"
        CCCD = self.ui.lineEdit_dk_cccd.text()
        email = self.ui.lineEdit_dk_email.text()
        sdt = self.ui.lineEdit_dk_sdt.text()
        tai_khoan_ngan_hang = self.ui.comboBox_dk_tknn.currentText()
        username = self.ui.lineEdit_dk_un.text()
        password = self.ui.lineEdit_dk_pw.text()

        # Kiểm tra các trường bắt buộc
        if not all([ho_va_ten, ngay_sinh, CCCD, email, sdt, tai_khoan_ngan_hang, username, password]):
            QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Gọi phương thức register với các tham số riêng lẻ
        result, suggested_username, suggested_password = self.manager.register(
            ho_va_ten,
            ngay_sinh,
            gioi_tinh,
            CCCD,
            email,
            sdt,
            tai_khoan_ngan_hang,
            username,
            password
        )

        if result == "Email đã tồn tại!":
            QMessageBox.warning(
                self,
                "Lỗi đăng ký",
                "Email đã tồn tại! Vui lòng sử dụng email khác.",
                QMessageBox.StandardButton.Ok
            )
            self.ui.lineEdit_dk_email.setFocus()

        elif "Username đã tồn tại" in result:
            reply = QMessageBox.question(
                self, "Đề xuất",
                f"Dùng username: {suggested_username} và password: {suggested_password}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                new_result, _, _ = self.manager.register(
                    ho_va_ten,
                    ngay_sinh,
                    gioi_tinh,
                    CCCD,
                    email,
                    sdt,
                    tai_khoan_ngan_hang,
                    suggested_username,  # Sử dụng username đề xuất
                    suggested_password  # Sử dụng password đề xuất
                )

                if new_result == "Đăng ký thành công!":
                    # Cập nhật UI và clear form
                    self.ui.lineEdit_dk_un.setText(suggested_username)
                    self.ui.lineEdit_dk_pw.setText(suggested_password)
                QMessageBox.information(self, "Thành công", "Đăng ký thành công với đề xuất!")
                self.clear_fields()
            else:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn username khác.")
        else:
            QMessageBox.information(self, "Kết quả", result)
            self.clear_fields()

    def clear_fields(self):
        """Xóa nội dung các ô nhập liệu sau khi đăng ký thành công"""
        self.ui.lineEdit_dk_ho_va_ten.clear()
        self.ui.dateEdit_dk_ngay_sinh.setDate(QDate.currentDate())
        self.ui.radioButton_dk_nam.setChecked(False)
        self.ui.radioButton_dk_nu.setChecked(False)
        self.ui.lineEdit_dk_cccd.clear()
        self.ui.lineEdit_dk_email.clear()
        self.ui.lineEdit_dk_sdt.clear()
        self.ui.lineEdit_dk_un.clear()
        self.ui.lineEdit_dk_pw.clear()

    def handle_login(self):
        """Xử lý sự kiện đăng nhập"""
        username = self.ui.lineEdit_dp_un.text()
        password = self.ui.lineEdit_dp_pw.text()

        is_valid, user = self.manager.login(username, password)

        if is_valid:
            # Lưu thông tin người dùng hiện tại
            self.current_user = user
            
            # Hiển thị thông tin người dùng lên giao diện
            self.display_user_info()
            
            # Chuyển đến màn hình chính
            self.ui.stackedWidget.setCurrentIndex(2)
        else:
            QMessageBox.warning(
                self,
                "Lỗi đăng nhập",
                "Sai tên đăng nhập hoặc mật khẩu!",
                QMessageBox.StandardButton.Ok
            )
            # Chỉ xóa trường mật khẩu, giữ lại tên đăng nhập
            self.ui.lineEdit_dp_pw.clear()
            self.ui.lineEdit_dp_pw.setFocus()

    def display_user_info(self):
        """Hiển thị thông tin người dùng lên giao diện"""
        if hasattr(self, 'current_user'):
            # Hiển thị thông tin trong trang tài khoản
            self.ui.label_52.setText(self.current_user.ho_va_ten)
            self.ui.label_47.setText(self.current_user.ngay_sinh)
            # Thiết lập radio button giới tính
            if self.current_user.gioi_tinh == "Nam":
                self.ui.radioButton_2.setChecked(True)
            else:
                self.ui.radioButton.setChecked(True)
            self.ui.label_59.setText(self.current_user.CCCD)
            self.ui.label_49.setText(self.current_user.email)
            self.ui.label_60.setText(self.current_user.sdt)
            self.ui.label_61.setText(self.current_user.tai_khoan_ngan_hang)
            self.ui.label_63.setText(str(self.current_user.balance))
            
            # Hiển thị username
            self.ui.label_57.setText(self.current_user.username)
            
            # Hiển thị thông báo chào mừng trong màn hình chính
            self.ui.label_mhc_tb1.setText(f"Xin chào, {self.current_user.ho_va_ten}!")
            self.ui.label_mhc_tb2.setText(f"Số dư tài khoản: {self.current_user.balance} VND")

    def go_to_account_page(self):
        """Chuyển đến trang thông tin tài khoản"""
        if hasattr(self, 'current_user'):
            self.display_user_info()
            self.ui.stackedWidget.setCurrentIndex(6)
        else:
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập để xem thông tin tài khoản!")
            self.ui.stackedWidget.setCurrentIndex(1)  # Chuyển đến trang đăng nhập
            
    def load_transaction_history(self):
        """Tải và hiển thị lịch sử giao dịch của người dùng hiện tại"""
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not hasattr(self, 'current_user'):
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập để xem lịch sử giao dịch!")
            self.ui.stackedWidget.setCurrentIndex(1)  # Chuyển đến trang đăng nhập
            return
            
        # Đặt lại các bộ lọc về mặc định
        self.ui.dateTimeEdit_lsgd_bd.setDateTime(QDateTime.currentDateTime().addDays(-30))  # Mặc định 30 ngày trước
        self.ui.dateTimeEdit_lsgd_kt.setDateTime(QDateTime.currentDateTime())  # Mặc định ngày hiện tại
        self.ui.comboBox_lsgd_tttt.setCurrentIndex(0)  # Mặc định "Tất cả"
        
        # Lấy danh sách vé của người dùng
        user_tickets = self.ticket_manager.get_user_tickets(self.current_user.username)
        
        # Lọc vé theo khoảng thời gian mặc định (30 ngày gần đây)
        start_date = self.ui.dateTimeEdit_lsgd_bd.dateTime().toString("yyyy-MM-dd")
        end_date = self.ui.dateTimeEdit_lsgd_kt.dateTime().toString("yyyy-MM-dd")
        
        filtered_tickets = []
        for ticket in user_tickets:
            # Lấy ngày mua vé từ chuỗi thời gian
            purchase_date = ticket.purchase_time.split()[0] if ticket.purchase_time else ""
            
            # Kiểm tra điều kiện lọc
            if purchase_date and start_date <= purchase_date <= end_date:
                filtered_tickets.append(ticket)
        
        # Xóa tất cả các dòng hiện có
        self.ui.tableWidget_lsgd.setRowCount(0)
        
        # Thêm dữ liệu mới
        for i, ticket in enumerate(filtered_tickets):
            self.ui.tableWidget_lsgd.insertRow(i)
            
            # Thời gian mua vé
            purchase_time = ticket.purchase_time if ticket.purchase_time else "N/A"
            self.ui.tableWidget_lsgd.setItem(i, 0, QTableWidgetItem(purchase_time))
            
            # Mã vé
            self.ui.tableWidget_lsgd.setItem(i, 1, QTableWidgetItem(ticket.ticket_id))
            
            # Lộ trình
            self.ui.tableWidget_lsgd.setItem(i, 2, QTableWidgetItem(ticket.route))
            
            # Số tiền
            price_text = f"{ticket.price:,} VND" if ticket.price else "N/A"
            self.ui.tableWidget_lsgd.setItem(i, 3, QTableWidgetItem(price_text))
            
            # Trạng thái thanh toán
            self.ui.tableWidget_lsgd.setItem(i, 4, QTableWidgetItem(ticket.payment_status))
        
        # Hiển thị thông báo nếu không có kết quả
        if len(filtered_tickets) == 0:
            selected_datetime = self.ui.dateTimeEdit.dateTime()
            date = selected_datetime.toString("yyyy-MM-dd")
            time = selected_datetime.toString("HH:mm")
            QMessageBox.information(
                self, 
                "Thông báo", 
                f"Không tìm thấy chuyến tàu phù hợp sau {time} ngày {date}!\n\n"
            )

    def go_to_edit_page(self):
        """Chuyển đến trang chỉnh sửa thông tin và hiển thị thông tin người dùng"""
        if hasattr(self, 'current_user'):
            # Hiển thị thông tin người dùng trong các trường nhập liệu
            self.ui.lineEdit_cs_ho_va_ten.setText(self.current_user.ho_va_ten)
            
            # Chuyển đổi chuỗi ngày sinh thành đối tượng QDate
            try:
                # Giả sử định dạng ngày sinh là yyyy-MM-dd
                date_parts = self.current_user.ngay_sinh.split('-')
                if len(date_parts) == 3:
                    year, month, day = map(int, date_parts)
                    birth_date = QDate(year, month, day)
                    self.ui.dateEdit_cs_ngay_sinh.setDate(birth_date)
            except Exception as e:
                print(f"Lỗi khi chuyển đổi ngày sinh: {e}")
                # Nếu có lỗi, đặt ngày mặc định là ngày hiện tại
                self.ui.dateEdit_cs_ngay_sinh.setDate(QDate.currentDate())
            
            self.ui.lineEdit_cs_cccd.setText(self.current_user.CCCD)
            self.ui.lineEdit_cs_email.setText(self.current_user.email)
            self.ui.lineEdit_cs_sdt.setText(self.current_user.sdt)
            
            # Thiết lập comboBox tài khoản ngân hàng
            index = self.ui.comboBox_cs_tknh.findText(self.current_user.tai_khoan_ngan_hang)
            if index >= 0:
                self.ui.comboBox_cs_tknh.setCurrentIndex(index)
            
            # Chuyển đến trang chỉnh sửa thông tin
            self.ui.stackedWidget.setCurrentIndex(7)
            
    def save_user_info(self):
        """Lưu thông tin người dùng sau khi chỉnh sửa"""
        if hasattr(self, 'current_user'):
            # Lấy thông tin từ các trường nhập liệu
            ho_va_ten = self.ui.lineEdit_cs_ho_va_ten.text()
            ngay_sinh = self.ui.dateEdit_cs_ngay_sinh.date().toString("yyyy-MM-dd")
            CCCD = self.ui.lineEdit_cs_cccd.text()
            email = self.ui.lineEdit_cs_email.text()
            sdt = self.ui.lineEdit_cs_sdt.text()
            tai_khoan_ngan_hang = self.ui.comboBox_cs_tknh.currentText()
            
            # Kiểm tra các trường bắt buộc
            if not all([ho_va_ten, CCCD, email, sdt, tai_khoan_ngan_hang]):
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
                return
            
            # Kiểm tra email đã tồn tại chưa (nếu thay đổi)
            if email != self.current_user.email and self.manager.is_email_exist(email):
                QMessageBox.warning(
                    self,
                    "Lỗi",
                    "Email đã tồn tại! Vui lòng sử dụng email khác.",
                    QMessageBox.StandardButton.Ok
                )
                return
            
            # Cập nhật thông tin người dùng
            self.current_user.ho_va_ten = ho_va_ten
            self.current_user.ngay_sinh = ngay_sinh
            self.current_user.CCCD = CCCD
            self.current_user.email = email
            self.current_user.sdt = sdt
            self.current_user.tai_khoan_ngan_hang = tai_khoan_ngan_hang
            
            # Lưu thông tin vào file
            self.manager.save_users_to_file()
            
            # Cập nhật hiển thị thông tin trong trang tài khoản
            self.display_user_info()
            
            # Hiển thị thông báo thành công
            QMessageBox.information(
                self,
                "Thành công",
                "Thông tin đã được cập nhật thành công!",
                QMessageBox.StandardButton.Ok
            )
            
            # Quay lại trang tài khoản
            self.ui.stackedWidget.setCurrentIndex(6)

    def go_to_deposit_page(self):
        """Chuyển đến trang nạp tiền"""
        # Xóa nội dung trường nhập tiền
        self.ui.lineEdit_nt_nhap_tien.clear()
        # Chuyển đến trang nạp tiền
        self.ui.stackedWidget.setCurrentIndex(8)
        
    def deposit_money(self):
        """Xử lý nạp tiền vào tài khoản"""
        if hasattr(self, 'current_user'):
            # Lấy số tiền từ trường nhập liệu
            amount_text = self.ui.lineEdit_nt_nhap_tien.text().strip()
            payment_method = self.ui.comboBox_nt_pttt.currentText()
            
            # Kiểm tra số tiền có hợp lệ không
            if not amount_text:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập số tiền!")
                return
                
            try:
                amount = int(amount_text)
                if amount <= 0:
                    QMessageBox.warning(self, "Lỗi", "Số tiền phải lớn hơn 0!")
                    return
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "Số tiền không hợp lệ! Vui lòng nhập số nguyên.")
                return
                
            # Cập nhật số dư tài khoản
            self.current_user.balance += amount
            
            # Lưu thông tin vào file
            self.manager.save_users_to_file()
            
            # Cập nhật hiển thị thông tin trong trang tài khoản
            self.display_user_info()
            
            # Hiển thị thông báo thành công
            QMessageBox.information(
                self,
                "Thành công",
                f"Nạp thành công {amount} VND vào tài khoản qua {payment_method}!",
                QMessageBox.StandardButton.Ok
            )
            
            # Xóa nội dung trường nhập tiền
            self.ui.lineEdit_nt_nhap_tien.clear()
            
            # Quay lại trang tài khoản
            self.ui.stackedWidget.setCurrentIndex(6)

    def go_to_change_password_page(self):
        """Chuyển đến trang đổi mật khẩu"""
        # Xóa nội dung các trường nhập liệu
        self.ui.lineEdit_dkt_mkht.clear()
        self.ui.lineEdit_dmk_mkm.clear()
        self.ui.lineEdit_dmk_mktt.clear()
        # Chuyển đến trang đổi mật khẩu
        self.ui.stackedWidget.setCurrentIndex(9)
        
    def change_password(self):
        """Xử lý đổi mật khẩu"""
        if hasattr(self, 'current_user'):
            # Lấy thông tin từ các trường nhập liệu
            current_password = self.ui.lineEdit_dkt_mkht.text()
            new_password = self.ui.lineEdit_dmk_mkm.text()
            confirm_password = self.ui.lineEdit_dmk_mktt.text()
            
            # Kiểm tra mật khẩu hiện tại
            if current_password != self.current_user.password:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu hiện tại không đúng!")
                return
                
            # Kiểm tra mật khẩu mới
            if not new_password:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập mật khẩu mới!")
                return
                
            # Kiểm tra xác nhận mật khẩu
            if new_password != confirm_password:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu mới và xác nhận mật khẩu không khớp!")
                return
                
            # Kiểm tra mật khẩu mới khác mật khẩu cũ
            if new_password == current_password:
                QMessageBox.warning(self, "Lỗi", "Mật khẩu mới phải khác mật khẩu hiện tại!")
                return
                
            # Cập nhật mật khẩu
            self.current_user.password = new_password
            
            # Lưu thông tin vào file
            self.manager.save_users_to_file()
            
            # Hiển thị thông báo thành công
            QMessageBox.information(
                self,
                "Thành công",
                "Đổi mật khẩu thành công!",
                QMessageBox.StandardButton.Ok
            )
            
            # Xóa nội dung các trường nhập liệu
            self.ui.lineEdit_dkt_mkht.clear()
            self.ui.lineEdit_dmk_mkm.clear()
            self.ui.lineEdit_dmk_mktt.clear()
            
            # Quay lại trang tài khoản
            self.ui.stackedWidget.setCurrentIndex(6)

    def search_trains(self):
        """Tìm kiếm chuyến tàu theo các tiêu chí"""
        # Lấy các tiêu chí tìm kiếm từ giao diện
        route_id = self.ui.comboBox.currentText()
        departure_station = self.ui.comboBox_tc_di.currentText()
        arrival_station = self.ui.comboBox_tc_den.currentText()
        
        # Lấy ngày và thời gian từ dateTimeEdit
        selected_datetime = self.ui.dateTimeEdit.dateTime()
        date = selected_datetime.toString("yyyy-MM-dd")
        time = selected_datetime.toString("HH:mm")
        
        # Nếu chọn "Tất cả" thì đặt giá trị là None
        if route_id == "Tất cả":
            route_id = None
        if departure_station == "Tất cả":
            departure_station = None
        if arrival_station == "Tất cả":
            arrival_station = None
            
        # Tìm kiếm chuyến tàu với điều kiện lịch trình sau thời gian chọn
        results = self.train_manager.search_trains(route_id, departure_station, arrival_station, date, time)
        
        # Hiển thị thông báo cho người dùng
        if results:
            QMessageBox.information(self, "Thông báo", f"Đã tìm thấy {len(results)} chuyến tàu.")
        else:
            QMessageBox.information(self, "Thông báo", "Không tìm thấy chuyến tàu nào phù hợp với tiêu chí tìm kiếm.")
        
        # Hiển thị kết quả lên bảng
        self.display_search_results(results)
        
    def display_search_results(self, trains):
        """Hiển thị kết quả tìm kiếm lên bảng"""
        # Xóa tất cả các dòng hiện có
        self.ui.tableWidget_tc.setRowCount(0)
        
        # Cập nhật số lượng cột và tiêu đề cột
        self.ui.tableWidget_tc.setColumnCount(6)  # Tăng số cột lên 6
        
        # Thiết lập tiêu đề cột
        self.ui.tableWidget_tc.setHorizontalHeaderItem(0, QTableWidgetItem("Mã tàu"))
        self.ui.tableWidget_tc.setHorizontalHeaderItem(1, QTableWidgetItem("Tuyến tàu"))
        self.ui.tableWidget_tc.setHorizontalHeaderItem(2, QTableWidgetItem("Ga xuất phát"))
        self.ui.tableWidget_tc.setHorizontalHeaderItem(3, QTableWidgetItem("Ga đến"))
        self.ui.tableWidget_tc.setHorizontalHeaderItem(4, QTableWidgetItem("Lịch trình"))
        self.ui.tableWidget_tc.setHorizontalHeaderItem(5, QTableWidgetItem("Ghế trống"))
        
        # Thêm dữ liệu mới
        for i, train in enumerate(trains):
            self.ui.tableWidget_tc.insertRow(i)
            self.ui.tableWidget_tc.setItem(i, 0, QTableWidgetItem(train.train_id))
            self.ui.tableWidget_tc.setItem(i, 1, QTableWidgetItem(train.route_id))
            self.ui.tableWidget_tc.setItem(i, 2, QTableWidgetItem(train.departure_station))
            self.ui.tableWidget_tc.setItem(i, 3, QTableWidgetItem(train.arrival_station))
            self.ui.tableWidget_tc.setItem(i, 4, QTableWidgetItem(train.schedule))
            self.ui.tableWidget_tc.setItem(i, 5, QTableWidgetItem(str(train.available_seats)))
        
        # Hiển thị thông báo nếu không có kết quả
        if len(trains) == 0:
            selected_datetime = self.ui.dateTimeEdit.dateTime()
            date = selected_datetime.toString("yyyy-MM-dd")
            time = selected_datetime.toString("HH:mm")
            QMessageBox.information(
                self, 
                "Thông báo", 
                f"Không tìm thấy chuyến tàu phù hợp sau {time} ngày {date}!\n\n"
            )

    def go_to_buy_ticket_page(self):
        """Chuyển đến trang mua vé"""
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not hasattr(self, 'current_user'):
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập để mua vé!")
            self.ui.stackedWidget.setCurrentIndex(1)  # Chuyển đến trang đăng nhập
            return
            
        # Hiển thị số dư tài khoản
        self.ui.label_40.setText(f"Số dư tài khoản: {self.current_user.balance:,} VND")
            
        # Chuyển đến trang mua vé
        self.ui.stackedWidget.setCurrentIndex(4)
        
        # Đặt lại trạng thái ban đầu cho tất cả các nút ghế
        for button in self.seat_buttons:
            button.setEnabled(True)
            button.setStyleSheet("")
        
        # Xóa danh sách ghế đã chọn
        self.selected_seats = []
        
        # Đặt lại các bộ lọc về mặc định
        self.ui.comboBox_mv_ma_tau.blockSignals(True)
        self.ui.comboBox_mv_tuyen_tau.blockSignals(True)
        self.ui.dateEdit_mv_ngay_di.blockSignals(True)
        
        self.ui.comboBox_mv_ma_tau.setCurrentIndex(0)  # Đặt về "Tất cả"
        self.ui.comboBox_mv_tuyen_tau.setCurrentIndex(0)  # Đặt về "Tất cả"
        
        # Đặt ngày hiện tại cho dateEdit
        current_date = QDate.currentDate()
        self.ui.dateEdit_mv_ngay_di.setDate(current_date)
        
        self.ui.comboBox_mv_ma_tau.blockSignals(False)
        self.ui.comboBox_mv_tuyen_tau.blockSignals(False)
        self.ui.dateEdit_mv_ngay_di.blockSignals(False)
        
        # Đảm bảo dateEdit hiển thị và đặt ở vị trí đúng
        self.ui.dateEdit_mv_ngay_di.setVisible(True)
        
        # Lấy gridLayout chứa các thành phần
        grid_layout = self.ui.gridLayoutWidget_5.layout()
        
        # Xóa các thành phần khỏi gridLayout
        grid_layout.removeWidget(self.ui.comboBox_mv_chuyen)
        grid_layout.removeWidget(self.ui.dateEdit_mv_ngay_di)
        grid_layout.removeWidget(self.ui.label_35)
        grid_layout.removeWidget(self.ui.label_29)
        
        # Thêm lại các thành phần vào gridLayout với vị trí mới
        # Thêm comboBox_mv_chuyen vào vị trí của dateEdit_mv_ngay_di (dòng 3)
        grid_layout.addWidget(self.ui.comboBox_mv_chuyen, 3, 2, 1, 1)
        # Thêm dateEdit_mv_ngay_di vào vị trí của comboBox_mv_chuyen (dòng 5)
        grid_layout.addWidget(self.ui.dateEdit_mv_ngay_di, 5, 2, 1, 1)
        # Thêm label_35 (Chọn chuyến tàu) vào vị trí của label_29 (dòng 3)
        grid_layout.addWidget(self.ui.label_35, 3, 0, 1, 1)
        # Thêm label_29 (Ngày đi) vào vị trí của label_35 (dòng 5)
        grid_layout.addWidget(self.ui.label_29, 5, 0, 1, 1)
        
        # Đổi tên label thành "Ngày đi:"
        self.ui.label_29.setText("Ngày đi:")
        
        # Ẩn comboBox thời gian nếu nó tồn tại
        if hasattr(self.ui, 'comboBox_mv_thoi_gian'):
            self.ui.comboBox_mv_thoi_gian.setVisible(False)
            # Xóa comboBox thời gian khỏi UI
            self.ui.comboBox_mv_thoi_gian.deleteLater()
            delattr(self.ui, 'comboBox_mv_thoi_gian')
        
        # Cập nhật giá vé
        self.update_ticket_price()
        
        # Tải danh sách chuyến tàu cho ngày đã chọn
        self.load_trains_for_route()
        
        # Kết nối sự kiện thay đổi mã tàu
        self.ui.comboBox_mv_ma_tau.currentIndexChanged.connect(self.load_trains_for_route)
        
        # Kết nối sự kiện thay đổi ngày đi
        self.ui.dateEdit_mv_ngay_di.dateChanged.connect(self.load_trains_for_route)

    def setup_seat_buttons(self):
        """Thiết lập các nút ghế"""
        # Danh sách tất cả các nút ghế
        self.seat_buttons = []
        
        # Danh sách các nút ghế cần kiểm tra
        seat_patterns = [
            # Ghế thường (g)
            ["g1", "g2", "g3", "g4", "g5"],
            ["g11", "g12", "g13", "g14", "g15"],
            ["g21", "g22", "g23", "g24", "g25"],
            ["g31", "g32", "g33", "g34", "g35"],
            
            # Ghế VIP (k)
            ["k1", "k2", "k3", "k4", "k5"],
            ["k11", "k12", "k13", "k14", "k15"],
            ["k21", "k22", "k23", "k24", "k25"],
            ["k31", "k32", "k33", "k34", "k35"]
        ]
        
        # Thêm các nút ghế vào danh sách nếu chúng tồn tại
        for pattern_group in seat_patterns:
            for seat_id in pattern_group:
                button_name = f"pushButton_{seat_id}"
                if hasattr(self.ui, button_name):
                    self.seat_buttons.append(getattr(self.ui, button_name))
        
        # Thiết lập text và kết nối sự kiện click cho từng nút
        for button in self.seat_buttons:
            seat_id = button.objectName().replace("pushButton_", "")
            button.setText(seat_id.upper())
            button.clicked.connect(lambda checked, btn=button: self.toggle_seat_selection(btn))
    
    def toggle_seat_selection(self, button):
        """Xử lý sự kiện khi người dùng chọn/bỏ chọn ghế"""
        seat_id = button.objectName().replace("pushButton_", "")
        
        if seat_id in self.selected_seats:
            # Bỏ chọn ghế
            self.selected_seats.remove(seat_id)
            button.setStyleSheet("")
        else:
            # Chọn ghế
            self.selected_seats.append(seat_id)
            button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        # Cập nhật giá vé
        self.update_ticket_price()
    
    def reset_seat_selection(self):
        """Đặt lại trạng thái chọn ghế"""
        self.selected_seats = []
        
        # Đặt lại màu sắc cho các nút ghế đã chọn
        for button in self.seat_buttons:
            if button.isEnabled():  # Chỉ đặt lại màu sắc cho các ghế chưa bị vô hiệu hóa
                button.setStyleSheet("")
        
        # Cập nhật giá vé
        self.update_ticket_price()
    
    def update_ticket_price(self):
        """Cập nhật giá vé dựa trên số ghế đã chọn"""
        # Giá vé cơ bản cho mỗi ghế
        base_price = 50000  # 50,000 VND
        
        # Tính tổng giá vé
        total_price = 0
        for seat_id in self.selected_seats:
            # Ghế VIP có giá cao hơn
            if seat_id.startswith("k"):
                total_price += base_price * 1.5
            else:
                total_price += base_price
        
        # Hiển thị giá vé
        self.ui.label_mv_gia_ve.setText(f"{total_price:,.0f} VND")
    
    def load_trains_for_route(self):
        """Tải danh sách chuyến tàu cho ngày đã chọn"""
        # Xóa danh sách chuyến tàu hiện tại
        self.ui.comboBox_mv_chuyen.clear()
        
        # Lấy ngày đã chọn - đây là bộ lọc chính
        selected_date = self.ui.dateEdit_mv_ngay_di.date().toString("yyyy-MM-dd")
        
        # Lấy tuyến tàu đã chọn
        route_id = self.ui.comboBox_mv_tuyen_tau.currentText()
        
        # Lấy mã tàu đã chọn
        code_prefix = self.ui.comboBox_mv_ma_tau.currentText()
        
        # Lọc tất cả các chuyến tàu theo ngày đã chọn
        all_trains = self.train_manager.trains
        trains_for_date = []
        
        # Lọc theo ngày trước
        for train in all_trains:
            # Lấy phần ngày từ lịch trình (yyyy-MM-dd HH:mm)
            train_date = train.schedule.split()[0] if ' ' in train.schedule else train.schedule
            if train_date == selected_date:
                trains_for_date.append(train)
        
        # Sau đó lọc theo mã tàu nếu cần
        if code_prefix != "Tất cả":
            trains_for_date = [train for train in trains_for_date if train.train_id.startswith(code_prefix)]
            
        # Lọc thêm theo tuyến nếu cần
        if route_id != "Tất cả":
            trains_for_date = [train for train in trains_for_date if train.route_id == route_id]
        
        # Thêm các chuyến tàu vào comboBox
        for train in trains_for_date:
            # Trích xuất thông tin thời gian từ lịch trình
            schedule_parts = train.schedule.split()
            time_info = ""
            if len(schedule_parts) >= 2:
                time_part = schedule_parts[1]
                # Chỉ hiển thị phần thời gian (không hiển thị ngày vì đã được lọc theo ngày)
                time_info = f"| Thời gian: {time_part}"
            
            # Hiển thị đầy đủ thông tin: Mã, Lộ trình và Thời gian
            display_text = f"Mã: {train.train_id} | Lộ trình: {train.departure_station} → {train.arrival_station} {time_info}"
            
            # Lưu cả train_id và schedule vào userData để có thể truy xuất sau này
            self.ui.comboBox_mv_chuyen.addItem(display_text, [train.train_id, train.schedule])
        
        # Tải thông tin chi tiết của chuyến tàu đầu tiên (nếu có)
        if self.ui.comboBox_mv_chuyen.count() > 0:
            self.load_train_details()
        else:
            # Nếu không có chuyến tàu nào, hiển thị thông báo
            self.ui.label_34.setText("Số ghế trống: 0")
            self.reset_seat_selection()
    
    def load_train_details(self):
        """Tải thông tin chi tiết của chuyến tàu đã chọn"""
        # Kiểm tra xem có chuyến tàu nào được chọn không
        if self.ui.comboBox_mv_chuyen.count() == 0:
            return
            
        # Lấy dữ liệu của chuyến tàu đã chọn (train_id và schedule)
        train_data = self.ui.comboBox_mv_chuyen.currentData()
        
        # Kiểm tra xem dữ liệu có đúng định dạng không
        if isinstance(train_data, list) and len(train_data) >= 2:
            train_id = train_data[0]
            schedule = train_data[1]
        else:
            # Nếu dữ liệu không đúng định dạng, chỉ lấy train_id
            train_id = train_data
            schedule = None
        
        # Tìm chuyến tàu phù hợp với cả train_id và schedule
        train = None
        for t in self.train_manager.trains:
            if t.train_id == train_id and (schedule is None or t.schedule == schedule):
                train = t
                break
        
        if train:
            # Hiển thị thông tin chuyến tàu
            self.ui.label_34.setText(f"Số ghế trống: {train.available_seats}")
            
            # Hiển thị lộ trình chi tiết
            route_info = f"{train.departure_station} đến {train.arrival_station}"
            self.ui.label_35.setText(f"Chuyến tàu: ")
            
            # Đặt lại danh sách ghế đã chọn
            self.reset_seat_selection()
            
            # Cập nhật các ghế đã được đặt
            self.update_occupied_seats(train.occupied_seats)
            
            # Cập nhật giá vé
            self.update_ticket_price()
            
    def update_occupied_seats(self, occupied_seats):
        """Vô hiệu hóa các ghế đã được đặt"""
        for button in self.seat_buttons:
            seat_id = button.objectName().replace("pushButton_", "")
            if seat_id in occupied_seats:
                # Vô hiệu hóa ghế đã đặt
                button.setEnabled(False)
                button.setStyleSheet("background-color: #FF5252; color: white;")
            else:
                # Kích hoạt ghế còn trống
                button.setEnabled(True)
                button.setStyleSheet("")

    def buy_ticket(self):
        """Xử lý sự kiện mua vé"""
        # Kiểm tra xem người dùng đã chọn ghế chưa
        if not self.selected_seats:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn ít nhất một ghế!")
            return
            
        # Lấy dữ liệu của chuyến tàu đã chọn (train_id và schedule)
        train_data = self.ui.comboBox_mv_chuyen.currentData()
        
        # Kiểm tra xem dữ liệu có đúng định dạng không
        if isinstance(train_data, list) and len(train_data) >= 2:
            train_id = train_data[0]
            schedule = train_data[1]
        else:
            # Nếu dữ liệu không đúng định dạng, chỉ lấy train_id
            train_id = train_data
            schedule = None
        
        # Tìm chuyến tàu phù hợp với cả train_id và schedule
        train = None
        for t in self.train_manager.trains:
            if t.train_id == train_id and (schedule is None or t.schedule == schedule):
                train = t
                break
        
        if not train:
            QMessageBox.warning(self, "Lỗi", "Không tìm thấy thông tin chuyến tàu!")
            return
            
        # Tính tổng giá vé
        base_price = 50000  # 50,000 VND
        total_price = 0
        for seat_id in self.selected_seats:
            # Ghế VIP có giá cao hơn
            if seat_id.startswith("k"):
                total_price += base_price * 1.5
            else:
                total_price += base_price
        
        # Kiểm tra số dư tài khoản
        if self.current_user.balance < total_price:
            QMessageBox.warning(self, "Lỗi", "Số dư tài khoản không đủ để thanh toán!")
            return
            
        # Cập nhật số ghế trống
        if not self.train_manager.update_available_seats(train_id, self.selected_seats):
            QMessageBox.warning(self, "Lỗi", "Không đủ ghế trống!")
            return
            
        # Tạo vé mới
        route = f"{train.departure_station} - {train.arrival_station}"
        
        ticket = self.ticket_manager.create_ticket(
            self.current_user.username,
            train_id,
            route,
            train.schedule,
            self.selected_seats,
            total_price
        )
        
        # Trừ tiền từ tài khoản người dùng
        self.current_user.balance -= total_price
        self.manager.save_users_to_file()
        
        # Hiển thị thông báo thành công
        QMessageBox.information(
            self,
            "Thành công",
            f"Đặt vé thành công!\n\nMã vé: {ticket.ticket_id}\nTuyến: {train.route_id}\nLộ trình: {train.departure_station} - {train.arrival_station}\nLịch trình: {train.schedule}\nGhế: {', '.join(self.selected_seats)}\nGiá vé: {total_price:,.0f} VND"
        )
        
        # Cập nhật số dư tài khoản hiển thị
        self.ui.label_40.setText(f"Số dư tài khoản: {self.current_user.balance:,} VND")
        
        # Đặt lại trạng thái chọn ghế
        self.reset_seat_selection()
        
        # Tải lại danh sách chuyến tàu
        self.load_trains_for_route()
        
        # Hỏi người dùng có muốn xem lịch sử giao dịch không
        reply = QMessageBox.question(
            self,
            "Xem lịch sử giao dịch",
            "Bạn có muốn xem lịch sử giao dịch không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.go_to_transaction_history_page()

    def go_to_transaction_history_page(self):
        """Chuyển đến trang lịch sử giao dịch"""
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not hasattr(self, 'current_user'):
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập để xem lịch sử giao dịch!")
            self.ui.stackedWidget.setCurrentIndex(1)  # Chuyển đến trang đăng nhập
            return
            
        # Chuyển đến trang lịch sử giao dịch
        self.ui.stackedWidget.setCurrentIndex(5)
        
        # Cập nhật danh sách tuyến tàu
        self.populate_transaction_train_routes()
        
        # Tải lịch sử giao dịch
        self.load_transaction_history()
        
    def populate_transaction_train_routes(self):
        """Cập nhật danh sách tuyến tàu trong trang lịch sử giao dịch"""
        # Xóa tất cả các mục hiện có
        self.ui.comboBox_lsgd_chuyen_tau.clear()
        
        # Thêm tùy chọn "Tất cả"
        self.ui.comboBox_lsgd_chuyen_tau.addItem("Tất cả")
        
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not hasattr(self, 'current_user'):
            return
            
        # Lấy danh sách vé của người dùng
        user_tickets = self.ticket_manager.get_user_tickets(self.current_user.username)
        
        # Tạo tập hợp các tuyến tàu duy nhất
        unique_routes = set()
        for ticket in user_tickets:
            if ticket.route:
                unique_routes.add(ticket.route)
        
        # Thêm các tuyến tàu vào comboBox
        for route in sorted(unique_routes):
            self.ui.comboBox_lsgd_chuyen_tau.addItem(route)

    def validate_transaction_date_range(self):
        """Kiểm tra tính hợp lệ của khoảng thời gian"""
        start_date = self.ui.dateTimeEdit_lsgd_bd.dateTime()
        end_date = self.ui.dateTimeEdit_lsgd_kt.dateTime()
        
        if start_date > end_date:
            QMessageBox.warning(self, "Lỗi", "Ngày bắt đầu phải nhỏ hơn hoặc bằng ngày kết thúc!")
            # Đặt ngày kết thúc bằng ngày bắt đầu
            self.ui.dateTimeEdit_lsgd_kt.setDateTime(start_date)
            return False
        return True

    def search_transactions(self):
        """Tìm kiếm giao dịch theo các tiêu chí"""
        # Kiểm tra tính hợp lệ của khoảng thời gian
        if not self.validate_transaction_date_range():
            return
        
        # Kiểm tra xem người dùng đã đăng nhập chưa
        if not hasattr(self, 'current_user'):
            QMessageBox.warning(self, "Lỗi", "Vui lòng đăng nhập để xem lịch sử giao dịch!")
            self.ui.stackedWidget.setCurrentIndex(1)  # Chuyển đến trang đăng nhập
            return
            
        # Lấy danh sách vé của người dùng
        user_tickets = self.ticket_manager.get_user_tickets(self.current_user.username)
        
        # Lấy các tiêu chí tìm kiếm từ giao diện
        start_date = self.ui.dateTimeEdit_lsgd_bd.dateTime().toString("yyyy-MM-dd")
        end_date = self.ui.dateTimeEdit_lsgd_kt.dateTime().toString("yyyy-MM-dd")
        payment_status = self.ui.comboBox_lsgd_tttt.currentText()
        train_route = self.ui.comboBox_lsgd_chuyen_tau.currentText()
        
        # Lọc vé theo khoảng thời gian, trạng thái thanh toán và tuyến tàu
        filtered_tickets = []
        for ticket in user_tickets:
            # Lấy ngày mua vé từ chuỗi thời gian
            purchase_date = ticket.purchase_time.split()[0] if ticket.purchase_time else ""
            
            # Kiểm tra điều kiện lọc
            date_match = purchase_date and start_date <= purchase_date <= end_date
            status_match = payment_status == "Tất cả" or ticket.payment_status == payment_status
            route_match = train_route == "Tất cả" or ticket.route == train_route
            
            if date_match and status_match and route_match:
                filtered_tickets.append(ticket)
        
        # Hiển thị thông báo cho người dùng
        if filtered_tickets:
            QMessageBox.information(self, "Thông báo", f"Đã tìm thấy {len(filtered_tickets)} giao dịch.")
        else:
            QMessageBox.information(self, "Thông báo", "Không tìm thấy giao dịch nào phù hợp với tiêu chí tìm kiếm.")
        
        # Hiển thị kết quả lên bảng
        self.display_filtered_transactions(filtered_tickets)
        
    def display_filtered_transactions(self, tickets):
        """Hiển thị kết quả tìm kiếm lên bảng"""
        # Xóa tất cả các dòng hiện có
        self.ui.tableWidget_lsgd.setRowCount(0)
        
        # Thêm dữ liệu mới
        for i, ticket in enumerate(tickets):
            self.ui.tableWidget_lsgd.insertRow(i)
            
            # Thời gian mua vé
            purchase_time = ticket.purchase_time if ticket.purchase_time else "N/A"
            self.ui.tableWidget_lsgd.setItem(i, 0, QTableWidgetItem(purchase_time))
            
            # Mã vé
            self.ui.tableWidget_lsgd.setItem(i, 1, QTableWidgetItem(ticket.ticket_id))
            
            # Lộ trình
            self.ui.tableWidget_lsgd.setItem(i, 2, QTableWidgetItem(ticket.route))
            
            # Số tiền
            price_text = f"{ticket.price:,} VND" if ticket.price else "N/A"
            self.ui.tableWidget_lsgd.setItem(i, 3, QTableWidgetItem(price_text))
            
            # Trạng thái thanh toán
            self.ui.tableWidget_lsgd.setItem(i, 4, QTableWidgetItem(ticket.payment_status))

    def handle_page_change(self):
        """Xử lý sự kiện khi chuyển trang"""
        if self.ui.stackedWidget.currentIndex() == 1:
            self.ui.lineEdit_dp_pw.setFocus()

    def go_to_login_page(self):
        """Chuyển đến trang đăng nhập"""
        self.ui.stackedWidget.setCurrentIndex(1)

    def go_to_registration_page(self):
        """Chuyển đến trang đăng ký"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def handle_logout(self):
        """Xử lý sự kiện đăng xuất"""
        # Xóa thông tin người dùng hiện tại
        self.current_user = None
        
        # Hiển thị thông báo đăng xuất thành công
        QMessageBox.information(
            self,
            "Thành công",
            "Đăng xuất thành công!",
            QMessageBox.StandardButton.Ok
        )
        
        # Xóa nội dung các trường đăng nhập
        self.ui.lineEdit_dp_un.clear()
        self.ui.lineEdit_dp_pw.clear()
        
        # Chuyển đến trang đăng nhập
        self.ui.stackedWidget.setCurrentIndex(1)
        
        # Đặt focus vào trường mật khẩu
        self.ui.lineEdit_dp_pw.setFocus()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
