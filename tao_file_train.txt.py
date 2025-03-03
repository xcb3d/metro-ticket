# Danh sách các ga
stations = [
    "Ga Bến Thành", "Ga Nhà hát Thành phố", "Ga Ba Son", "Ga Công viên Văn Thánh",
    "Ga Tân Cảng", "Ga Thảo Điền", "Ga An Phú", "Ga Rạch Chiếc", "Ga Phước Long",
    "Ga Bình Thái", "Ga Thủ Đức", "Ga Khu Công nghệ cao", "Ga Đại học Quốc gia", "Ga Bến xe Suối Tiên"
]

# Danh sách ID tàu và tuyến tàu
trains = [
    ("T001", "M1"), ("T002", "M2"), ("T003", "M3"), ("T004", "M4"), ("T005", "M5"),
    ("T006", "M6"), ("T007", "M7"), ("T008", "M8"), ("T009", "M9"), ("T010", "M10")
]

import random
from datetime import datetime, timedelta

# Khởi tạo thời gian bắt đầu từ ngày hôm nay
start_time = datetime(2025, 3, 2, 8, 0)  # Ngày giả định 02/03/2025 lúc 08:00

# Tạo dữ liệu
train_data = []
for i, (train_id, route_id) in enumerate(trains):
    ga_di = stations[i % len(stations)]
    ga_den = stations[(i + 1) % len(stations)]  # Điểm đến tiếp theo trong danh sách ga

    # Fake lịch trình: mỗi chuyến cách nhau 75-120 phút
    departure_time = start_time + timedelta(minutes=random.randint(75, 120) * i)
    departure_str = departure_time.strftime("%Y-%m-%d %H:%M")

    # Mỗi tàu có 40 ghế trống
    train_data.append(f"{train_id}|{route_id}|{ga_di} - {ga_den}|{departure_str}|40")

# Đường dẫn file
file_path = "train.txt"

# Ghi dữ liệu vào file trains.txt
with open(file_path, "a", encoding="utf-8") as file:
    file.write("\n".join(train_data))


