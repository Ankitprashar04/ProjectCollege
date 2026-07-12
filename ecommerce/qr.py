import qrcode
import os

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

folder = os.path.join(
    BASE_DIR,
    "static",
    "images"
)

os.makedirs(
    folder,
    exist_ok=True
)

upi = "upi://pay?pa=studentessentials@upi&pn=StudentEssentials&cu=INR"

img = qrcode.make(upi)

img.save(
    os.path.join(
        folder,
        "payment_qr.png"
    )
)

print(
    "QR Generated Successfully"
)
