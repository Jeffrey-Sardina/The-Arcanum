import qrcode
import sys

if __name__ == '__main__':
    # get user data
    text = sys.argv[1]
    filename = sys.argv[2]

    # get file format
    ext = filename.split('.')[-1].lower()
    if ext == 'svg':
        image_factory=qrcode.image.svg.SvgPathImage
    elif ext == 'png':
        image_factory = None
    else:
        assert False, 'File name must end in .svg or .png'
    
    # generate qr code
    qr = qrcode.QRCode(
        version=1, # 1 to 40 -- the larger the more complex the code becomes. Keeping at 1 and using simple text is best!
        error_correction=qrcode.constants.ERROR_CORRECT_H, #_L, _M, _Q, _H in order of increasing error correction ability
        box_size=100, # higher number -- more pixels / higher res
        border=1, # if you are going to print this on white paper, a thick border is not needed -- the extra space on the paper already creates that!
        image_factory=image_factory # to create a png or svg
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    # write to disk
    img.save(filename)
