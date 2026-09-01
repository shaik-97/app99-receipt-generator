# create an app to generate a pdf receipt if user buys an item
from pathlib import Path
import pandas as pd
from fpdf import FPDF
import logging

logging.basicConfig(
    filename="app99.log",
    filemode="w",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s:%(lineno)d: %(message)s",
)
log = logging.getLogger(__name__)


class Item:
    log.debug("Item class initialized")
    def __init__(self, item_id:str):
            self.item_id= item_id
            self.user_name = None
            self.item_name = None
            self.item_price = None

    def get_all_details(self)-> None:
        log.debug("Getting all details for item id: %s", self.item_id)
        self.item_name = df.loc[df["item_id"] == self.item_id, "item_name"]
        self.item_price = df.loc[df["item_id"] == self.item_id, "item_price"]

    def buy_item(self):
        log.debug("Attempting to buy item with id: %s", self.item_id)
        if df.loc[df["item_id"] == self.item_id, "in_stock"].values[0] >= 1:
            self.update_list()
            print("Item list updated.")
            return True
        return False

    def update_list(self):
        log.debug("Updating item list for item id: %s", self.item_id)
        item_row = df.loc[df["item_id"].astype(str) == self.item_id, "in_stock"]
        df.loc[df["item_id"].astype(str) == self.item_id, "in_stock"] = item_row.values[0] - 1
        df.to_csv("items.csv", index=False)
        return

class Receipt:
    log.debug("Receipt class initialized")
    count = 0
    def __init__(self, item):
        self.item_id = item.item_id
        self.user_name = item.user_name
        self.item_name = item.item_name
        self.item_price = item.item_price

    def pdf_receipt_generator(self):
        log.debug("Inside pdf_receipt_generator method for user: %s and for item: %s", self.user_name, self.item_id)
        log.debug("Generating PDF receipt for user: %s", self.user_name)
        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.cell(200, 10, txt=f"Receipt for user {self.user_name}", ln=1, align="C")
            pdf.ln(10)
            receipt_text = f"User name : {self.user_name}\nItem ID : {self.item_id}\nItem name : {self.item_name}\nItem price : {self.item_price}\n\nThank you for your purchase!"
            pdf.multi_cell(200, 10, txt=receipt_text)
            pdf_name = f"receipt_{self.user_name}.pdf"
            save_dir = Path("E:\\PythonProject\\app99-receipt-generator\\pdf_docs")
            save_dir.mkdir(parents=True, exist_ok=True)
            pdf_path = save_dir / pdf_name
            pdf.output(str(pdf_path))
            # verify if the PDF was created successfully
            if pdf_path.exists() and pdf_path.stat().st_size > 0:
                log.debug("PDF receipt generated successfully at: %s", pdf_path)
                log.debug("PDF generated for  user: %s", self.user_name)
                Receipt.count += 1
                return True
            else:
                log.error("Failed to generate PDF receipt for user: %s", self.user_name)
                return False
        except Exception as e:
            log.error("Error generating PDF receipt for user: %s. Error: %s", self.user_name, str(e))
            return False            

    @classmethod
    # this is a class method which is used only for class level logic and not for instance level logic. It is used to get the total receipt count.
    def get_total_receipt_count(cls):
        return cls.count


df = pd.read_csv("items.csv",dtype={"item_id": str})
def main():
    print(df.to_string(index=False))
    user_name = input("Please enter your name: ")
    item_id = input("Please enter the item id you want to buy : ")
    item = Item(item_id)
    item.user_name = user_name
    item.get_all_details()
    receipt = Receipt(item)
    if item.buy_item():
        receipt.pdf_receipt_generator()
        log.debug("Please find the updated items list:")
        log.debug("\n%s", df.to_string(index=False))
        log.debug("Total receipt count: %d", receipt.get_total_receipt_count())
    else:   
        print("Item is out of stock. Please try again later.")


if __name__ == "__main__":
    main()