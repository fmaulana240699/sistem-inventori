import qrcode
from io import BytesIO
import base64

qr = qrcode.QRCode(
    version=1,
    box_size=10,
    border=4
)
qr.add_data("testing")
qr.make(fit=True)
img = qr.make_image(fill_color="black", back_color="white")
buffer = BytesIO()
img.save(buffer, format='PNG')
base64_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
print(base64_image)
# decoded_image = base64.b64decode(base64_image)

# with open('output_image.png', 'wb') as file:
#     file.write(decoded_image)


