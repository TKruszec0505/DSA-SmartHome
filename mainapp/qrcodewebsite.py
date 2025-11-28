import qrcode
def make_qr():
    img = qrcode.make('http://192.168.100.14:5000')
    img.save('qrcode1.png')
make_qr()

if __name__ == '__main__':
    make_qr()
