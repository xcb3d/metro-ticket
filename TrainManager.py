class Train:
    def __init__(self, train_id, route_id, departure_station, arrival_station, schedule, available_seats, occupied_seats=None):
        self.train_id = train_id
        self.route_id = route_id
        self.departure_station = departure_station
        self.arrival_station = arrival_station
        self.route = f"{departure_station} - {arrival_station}"  # Tạo lộ trình từ ga xuất phát và ga đến
        self.schedule = schedule
        self.available_seats = available_seats
        self.occupied_seats = occupied_seats or []  # Danh sách các ghế đã được đặt

class TrainManager:
    TRAINS_FILE_PATH = "train.txt"
    
    def __init__(self):
        self.trains = self.load_trains_from_file()
        self.stations = self.extract_stations()
        
    def load_trains_from_file(self):
        """Tải danh sách chuyến tàu từ file"""
        trains = []
        try:
            with open(self.TRAINS_FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split("|")
                    if len(data) >= 6:
                        train_id = data[0]
                        route_id = data[1]
                        departure_station = data[2]
                        arrival_station = data[3]
                        schedule = data[4]
                        available_seats = int(data[5])
                        
                        # Kiểm tra xem có thông tin về ghế đã đặt không
                        occupied_seats = []
                        if len(data) > 6 and data[6]:
                            occupied_seats = data[6].split(",")
                            
                        trains.append(Train(train_id, route_id, departure_station, arrival_station, schedule, available_seats, occupied_seats))
        except FileNotFoundError:
            # Tạo file nếu chưa tồn tại
            with open(self.TRAINS_FILE_PATH, "w", encoding="utf-8") as file:
                pass
        return trains
    
    def extract_stations(self):
        """Trích xuất danh sách các ga từ lộ trình của các chuyến tàu"""
        stations = set()
        for train in self.trains:
            stations.add(train.departure_station)
            stations.add(train.arrival_station)
        return sorted(list(stations))
    
    def get_routes(self):
        """Lấy danh sách các tuyến tàu"""
        routes = set()
        for train in self.trains:
            routes.add(train.route_id)
        return sorted(list(routes))
    
    def search_trains(self, route_id=None, departure_station=None, arrival_station=None, date=None, time=None):
        """Tìm kiếm chuyến tàu theo các tiêu chí"""
        results = []
        
        for train in self.trains:
            # Kiểm tra tuyến tàu nếu được chỉ định
            if route_id and train.route_id != route_id:
                continue
                
            # Kiểm tra ga xuất phát nếu được chỉ định
            if departure_station and departure_station != "Tất cả" and train.departure_station != departure_station:
                continue
                
            # Kiểm tra ga đến nếu được chỉ định
            if arrival_station and arrival_station != "Tất cả" and train.arrival_station != arrival_station:
                continue
                
            # Kiểm tra lịch trình so với thời gian hiện tại hoặc thời gian người dùng chọn
            train_datetime = train.schedule  # Format: "yyyy-MM-dd HH:mm"
            
            # Nếu có ngày và thời gian được chỉ định, kiểm tra lịch trình sau thời gian đó
            if date and time:
                search_datetime = f"{date} {time}"
                if train_datetime < search_datetime:
                    continue
            
            results.append(train)
            
        return results
        
    def get_train_by_id(self, train_id):
        """Lấy thông tin chuyến tàu theo ID"""
        for train in self.trains:
            if train.train_id == train_id:
                return train
        return None
        
    def get_all_times_for_train(self, train_id):
        """Lấy tất cả các thời gian khả dụng cho một mã tàu cụ thể"""
        available_times = []
        
        for train in self.trains:
            if train.train_id == train_id:
                # Lấy phần thời gian từ lịch trình (định dạng: "yyyy-MM-dd HH:mm")
                schedule_parts = train.schedule.split()
                if len(schedule_parts) >= 2:
                    date_part = schedule_parts[0]  # Ngày
                    time_part = schedule_parts[1]  # Thời gian
                    available_times.append((date_part, time_part, train.schedule))
        
        # Sắp xếp theo thời gian
        available_times.sort(key=lambda x: x[2])
        return available_times
        
    def update_available_seats(self, train_id, seats_to_book):
        """Cập nhật số ghế trống và danh sách ghế đã đặt sau khi mua vé"""
        train = self.get_train_by_id(train_id)
        if train:
            # Kiểm tra xem có đủ ghế trống không
            if train.available_seats >= len(seats_to_book):
                # Kiểm tra xem các ghế đã chọn có bị trùng với ghế đã đặt không
                for seat in seats_to_book:
                    if seat in train.occupied_seats:
                        return False  # Ghế đã được đặt
                
                # Cập nhật số ghế trống và danh sách ghế đã đặt
                train.available_seats -= len(seats_to_book)
                train.occupied_seats.extend(seats_to_book)
                self.save_trains_to_file()
                return True
            else:
                return False
        return False
        
    def save_trains_to_file(self):
        """Lưu danh sách chuyến tàu vào file"""
        with open(self.TRAINS_FILE_PATH, "w", encoding="utf-8") as file:
            for train in self.trains:
                file.write(f"{train.train_id}|{train.route_id}|{train.departure_station}|{train.arrival_station}|{train.schedule}|{train.available_seats}|{','.join(train.occupied_seats)}\n")
                
    def get_trains_by_route(self, route_id):
        """Lấy danh sách chuyến tàu theo tuyến"""
        return [train for train in self.trains if train.route_id == route_id]
    
    def get_train_code_prefixes(self):
        """Lấy danh sách các mã tiền tố của tàu (ví dụ: M1, M2, etc.)"""
        prefixes = set()
        
        for train in self.trains:
            # Tìm tiền tố mã tàu (ví dụ: M1, M2, etc.)
            train_id = train.train_id
            # Tìm các ký tự đầu tiên là chữ cái và số theo sau
            import re
            match = re.match(r'^([A-Za-z]\d+)', train_id)
            if match:
                prefix = match.group(1)
                prefixes.add(prefix)
        
        # Sắp xếp các tiền tố
        return sorted(list(prefixes))
        
    def search_trains_by_code_prefix(self, code_prefix, date=None):
        """Tìm kiếm chuyến tàu theo tiền tố mã (ví dụ: M1, M2) và ngày"""
        results = []
        
        for train in self.trains:
            # Kiểm tra xem train_id có bắt đầu bằng code_prefix không
            if train.train_id.startswith(code_prefix):
                # Nếu có ngày được chỉ định, kiểm tra lịch trình
                if date:
                    train_date = train.schedule.split()[0]  # Lấy phần ngày từ lịch trình
                    if train_date != date:
                        continue
                results.append(train)
                
        return results
