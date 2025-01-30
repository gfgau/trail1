import os
import pandas as pd
import qrcode
import random

def generate_qr_codes(output_dir="qr_codes"):
    os.makedirs(output_dir, exist_ok=True)
    ranges = [list(range(1000, 1431)), list(range(4000, 4431)), list(range(8000, 8431))]
    all_codes = ranges[0] + ranges[1] + ranges[2]
    four_digit_codes = random.sample(all_codes, 125)

    qr_data = []

    for i, code in enumerate(four_digit_codes, start=1):
        secret_code = random.randint(100000, 999999)
        qr_data.append((code, secret_code))
        data = f"{code},{secret_code}"
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        img.save(os.path.join(output_dir, f"qr_code_{i}.png"))

    return qr_data

def save_to_excel(qr_data, excel_file="qr_data.xlsx"):
    df = pd.DataFrame(qr_data, columns=["teamid", "hackode"])
    df.to_excel(excel_file, index=False)
    print(f"Data saved to {excel_file}")

# Generate QR codes and save data to Excel
if __name__ == "__main__":
    qr_data = generate_qr_codes()
    save_to_excel(qr_data)
