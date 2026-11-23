class payment:
    def __init__(self, amount, method):
        self.amount = amount
        self.method = method



    def process_payment(self, amount, method):
        if method == "credit_card":
            print(f"Processing credit card payment of {amount}")
        elif method == "paypal":
            print(f"Processing PayPal payment of {amount}")
        else:
            print("Payment method not supported")
payment(100, "paypal").process_payment(100, "paypal")

