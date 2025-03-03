import datetime

class Ticket:
    def __init__(self, ticket_id, user_id, train_id, route, schedule, seats, price, payment_status="Đã thanh toán", purchase_time=None):
        self.ticket_id = ticket_id
        self.user_id = user_id
        self.train_id = train_id
        self.route = route
        self.schedule = schedule
        self.seats = seats  # Danh sách các ghế đã đặt
        self.price = price
        self.payment_status = payment_status
        self.purchase_time = purchase_time or datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 