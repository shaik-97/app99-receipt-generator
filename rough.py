import pandas as pd
df = pd.read_csv("items.csv", dtype={"item_id": str})
item_id = "2"
price = df.loc[df["item_id"] == item_id, "item_price"]
price2 = df.loc[df["item_id"].astype(str) == item_id, "item_price"].values[0]
print("price-------->",price,)
print("price  2 -------->",price2,type(price2))

stock = 1
if df.loc[df["item_id"].astype(str) == "2", "in_stock"].values[0] >=1:
    print("stock-->",stock,"type--->",type(stock))

print("stock number--->",df.loc[df['item_id'] == item_id, 'in_stock'].squeeze()-1)
#5 -= 1
df.to_csv("items.csv", index=False)
print("updated list---->",df)

# from fpdf import FPDF
#
# # 1. Create a blank PDF document
# pdf = FPDF()
#
# # 2. You MUST add a page first before typing anything
# pdf.add_page()
#
# # 3. Choose your font (Font name, size)
# # Standard fonts built into Python: 'Arial', 'Times', 'Courier'
# pdf.set_font('Arial', size=16)
#
# # 4. Write a single line of text
# # w=0 means "stretch text box all the way to the right side of the page"
# # h=10 is the height of the line box
# # ln=1 means "hit Enter and move to the next line when done"
# pdf.cell(w=0,txt="Receipt for user John Doe", ln=1)
#
# # 5. Add a blank space (like pressing Enter an extra time)
# pdf.ln(10)
#
# # 6. Change font size for regular body text
# pdf.set_font('Arial', size=12)
#
# # 7. Write a paragraph using multi_cell
# # multi_cell is smart—if a sentence is too long, it automatically wraps it
# paragraph_text = (
#     "This is"
# )
# pdf.multi_cell(w=0, h=8, txt=paragraph_text)
#
# # 8. Save your creation to a file
# pdf.output("my_first_pdf.pdf")
#
# print("Success! Your PDF has been saved.")
