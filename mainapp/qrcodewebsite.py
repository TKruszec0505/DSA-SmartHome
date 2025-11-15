import qrcode
def make_qr():
    img = qrcode.make('http://192.168.100.7:5000')
    img.save('qrcode1.png')
make_qr()