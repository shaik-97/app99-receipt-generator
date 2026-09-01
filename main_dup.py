# create an app to generate a pdf receipt if user buys an item
import pandas as pd
from fpdf import FPDF


class Receipt:
    total_receipts = 0

    def __init__(self, user_name=None, item_id=None):
        self.user_name = user_name
        self.item_id = item_id
        self.item_name = None
        self.item_price = None
        Receipt.total_receipts += 1

    def get_all_details(self, item_id):
        item_row = df[df["item_id"] == item_id]
        if item_row.empty:
            raise ValueError("Invalid item ID")

        self.item_id = item_id
        self.item_name = item_row["item_name"].values[0]
        self.item_price = item_row["price"].values[0]
        return self.item_name, self.item_price

    def buying(self, item_id):
        item_row = df[df["item_id"] == item_id]
        if item_row.empty:
            raise ValueError("Invalid item ID")

        if item_row["in_stock"].values[0] >= 1:
            df.loc[df["item_id"] == item_id, "in_stock"] -= 1
            self.get_all_details(item_id)
            print("Item added to receipt.")
            return True

        print("Item out of stock.")
        return False

    def pdf_receipt_generator(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Receipt for user {self.user_name}", ln=1, align="C")
        pdf.ln(10)

        receipt_text = (
            f"User name : {self.user_name}\n\n"
            f"Item ID : {self.item_id}\n\n"
            f"Item Name : {self.item_name}\n\n"
            f"Price : {self.item_price}\n\n"
        )
        pdf.multicell(200, 10, txt=receipt_text)
        pdf.output("receipt.pdf")

    @classmethod
    def get_total_receipt_count(cls):
        return cls.total_receipts


# reading CSV
# careful: item_id in CSV is numeric; avoid .squeeze() here, it can complicate access
# using normal DataFrame is safer for beginners

df = pd.read_csv("items.csv")


def main():
    print(df.to_string(index=False))
    user_name = input("Please enter your name: ")
    item_id = int(input("Please enter the item id you want to buy : "))

    receipt = Receipt(user_name=user_name)
    receipt.buying(item_id)
    receipt.get_all_details(item_id)
    receipt.pdf_receipt_generator()


if __name__ == "__main__":
    main()
