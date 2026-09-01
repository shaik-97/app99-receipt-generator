# create an app to generate a pdf receipt if user buys an item
from pathlib import Path
import pandas as pd
from fpdf import FPDF

class Receipt:
    count = 0

    def __init__(self):
        self.item_id= None
        self.user_name = None
        self.item_name = None
        self.item_price = None

    def get_all_details(self,item_id:str)-> None:
        self.item_name = df.loc[df["item_id"].astype(str) == item_id, "item_name"].values[0]
        self.item_price = df.loc[df["item_id"].astype(str) == item_id, "item_price"].values[0]

    def buy_item(self):
        if df.loc[df["item_id"].astype(str) == self.item_id, "in_stock"].values[0] >= 1:
            self.update_list()
            print("Item list updated.")
            return True
        return False

    def update_list(self):
        item_row = df.loc[df["item_id"].astype(str) == self.item_id, "in_stock"]
        df.loc[df["item_id"].astype(str) == self.item_id, "in_stock"] = item_row.values[0] - 1
        df.to_csv("items.csv", index=False)
        return

    def pdf_receipt_generator(self):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Receipt for user {self.user_name}", ln=1, align="C")
        pdf.ln(10)
        receipt_text = f"User name : {self.user_name}\nItem ID : {self.item_id}\nItem name : {self.item_name}\nItem price : {self.item_price}\n\nThank you for your purchase!"
        pdf.multi_cell(200, 10, txt=receipt_text)
        pdf_name = f"receipt_{self.user_name}.pdf"
        save_dir = Path("E:\\PythonProject\\receipt_generator\\pdf_docs")
        save_dir.mkdir(parents=True, exist_ok=True)
        pdf.output(str(save_dir/pdf_name))
        Receipt.count += 1
        print(f"pdf generated for user {self.user_name}")

    @classmethod
    # this is a class method which is used only for class level logic and not for instance level logic. It is used to get the total receipt count.
    def get_total_receipt_count(cls):
        return cls.count


df = pd.read_csv("items.csv")
def main():
    print(df.to_string(index=False))
    user_name = input("Please enter your name: ")
    item_id = input("Please enter the item id you want to buy : ")
    receipt = Receipt()
    receipt.user_name = user_name
    receipt.item_id = item_id
    receipt.get_all_details(item_id)
    if receipt.buy_item():
        receipt.pdf_receipt_generator()
        print("please find updated items list", df.to_string(index=False))
        print("Total receipt count:", Receipt.get_total_receipt_count())
    else:   
        print("Item is out of stock. Please try again later.")


if __name__ == "__main__":
    main()