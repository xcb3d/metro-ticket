import random
import datetime
from Ticket import Ticket

class TicketManager:
    TICKETS_FILE_PATH = "tickets.txt"
    
    def __init__(self):
        self.tickets = self.load_tickets_from_file()
        
    def load_tickets_from_file(self):
        """Tải danh sách vé từ file"""
        tickets = []
        try:
            with open(self.TICKETS_FILE_PATH, "r", encoding="utf-8") as file:
                for line in file:
                    data = line.strip().split("|")
                    if len(data) >= 8:
                        ticket_id = data[0]
                        user_id = data[1]
                        train_id = data[2]
                        route = data[3]
                        schedule = data[4]
                        seats = data[5].split(",")
                        price = float(data[6])
                        payment_status = data[7]
                        purchase_time = data[8] if len(data) > 8 else None
                        tickets.append(Ticket(ticket_id, user_id, train_id, route, schedule, seats, price, payment_status, purchase_time))
        except FileNotFoundError:
            # Tạo file nếu chưa tồn tại
            with open(self.TICKETS_FILE_PATH, "w", encoding="utf-8") as file:
                pass
        return tickets
    
    def save_tickets_to_file(self):
        """Lưu danh sách vé vào file"""
        with open(self.TICKETS_FILE_PATH, "w", encoding="utf-8") as file:
            for ticket in self.tickets:
                seats_str = ",".join(ticket.seats)
                file.write(f"{ticket.ticket_id}|{ticket.user_id}|{ticket.train_id}|{ticket.route}|{ticket.schedule}|{seats_str}|{ticket.price}|{ticket.payment_status}|{ticket.purchase_time}\n")
    
    def generate_ticket_id(self):
        """Tạo mã vé ngẫu nhiên"""
        while True:
            ticket_id = f"TK{random.randint(1000, 9999)}"
            if not any(ticket.ticket_id == ticket_id for ticket in self.tickets):
                return ticket_id
    
    def create_ticket(self, user_id, train_id, route, schedule, seats, price, payment_status="Đã thanh toán"):
        """Tạo vé mới"""
        ticket_id = self.generate_ticket_id()
        ticket = Ticket(ticket_id, user_id, train_id, route, schedule, seats, price, payment_status)
        self.tickets.append(ticket)
        self.save_tickets_to_file()
        return ticket
    
    def get_user_tickets(self, user_id):
        """Lấy danh sách vé của người dùng"""
        return [ticket for ticket in self.tickets if ticket.user_id == user_id]
    
    def get_ticket_by_id(self, ticket_id):
        """Lấy thông tin vé theo ID"""
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None
    
    def cancel_ticket(self, ticket_id):
        """Hủy vé"""
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            self.tickets.remove(ticket)
            self.save_tickets_to_file()
            return True
        return False 