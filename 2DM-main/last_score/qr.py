import qrcode

def get_qr(text):
    qr_code = qrcode.QRCode(version=1,box_size=10,border=5)

    qr_code.add_data(text)

    qr_code.make(fit=True)
    
    image = qr_code.make_image(fill_color='white',back_color='black')

    image.save('last_score/qr.png')
    return

get_qr("ahoj")

