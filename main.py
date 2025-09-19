import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime

def register_unicode_font():
    """Try to register a Unicode font that supports the ₹ symbol."""
    possible_fonts = [
        # Windows
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialuni.ttf",  # Arial Unicode MS
    ]

    for font_path in possible_fonts:
        if os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont("CustomFont", font_path))
            return "CustomFont"
    
    # fallback
    print("⚠️ No Unicode font found. Using default Helvetica (₹ may not display).")
    return "Helvetica"

FONT_NAME = register_unicode_font()

def generate_receipt(customer_name, payment_mode, receipt_number, items):
    file_name = f"Payment_Receipt_{receipt_number}.pdf"
    c = canvas.Canvas(file_name, pagesize=A4)
    
    width, height = A4
    c.setTitle("Payment Receipt")

    # Header
    c.setFont(FONT_NAME, 20)
    c.drawCentredString(width / 2, height - 50, "Payment Receipt")

    # Receipt Info
    c.setFont(FONT_NAME, 12)
    c.drawString(50, height - 100, f"Receipt Number: {receipt_number}")
    c.drawString(50, height - 120, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.drawString(50, height - 140, f"Customer Name: {customer_name}")
    c.drawString(50, height - 160, f"Payment Mode: {payment_mode}")

    # Table header
    c.setFont(FONT_NAME, 12)
    c.drawString(50, height - 200, "Item")
    c.drawString(250, height - 200, "Quantity")
    c.drawString(350, height - 200, "Price per Unit (₹)")
    c.drawString(500, height - 200, "Total (₹)")

    y_position = height - 220
    total_amount = 0

    # Items list
    c.setFont(FONT_NAME, 12)
    for item in items:
        item_name = item['name']
        quantity = item['quantity']
        price = item['price']
        item_total = quantity * price
        total_amount += item_total

        c.drawString(50, y_position, item_name)
        c.drawString(250, y_position, str(quantity))
        c.drawString(350, y_position, f"{price:.2f}")
        c.drawString(500, y_position, f"{item_total:.2f}")

        y_position -= 20

    # Grand total
    c.setFont(FONT_NAME, 12)
    c.drawString(350, y_position - 20, "Grand Total:")
    c.drawString(500, y_position - 20, f"₹{total_amount:.2f}")

    # Footer
    c.setFont(FONT_NAME, 10)
    c.drawString(50, y_position - 60, "Thank you for your payment!")
    c.drawString(50, y_position - 80, "Contact us for any inquiries.")

    c.save()
    print(f"\nReceipt generated successfully: {file_name}")


def main():
    print("=== Payment Receipt Generator ===")
    customer_name = input("Enter customer name: ")
    payment_mode = input("Enter payment mode (e.g., Cash, Card, UPI): ")
    receipt_number = input("Enter receipt number: ")

    items = []
    while True:
        print("\nEnter item details:")
        item_name = input("Item name: ")
        try:
            quantity = int(input("Quantity: "))
            price = float(input("Price per unit (₹): "))
        except ValueError:
            print("Invalid input. Please enter numeric values for quantity and price.")
            continue

        items.append({'name': item_name, 'quantity': quantity, 'price': price})

        more = input("Add another item? (yes/no): ").strip().lower()
        if more != 'yes':
            break

    generate_receipt(customer_name, payment_mode, receipt_number, items)


if __name__ == "__main__":
    main()
