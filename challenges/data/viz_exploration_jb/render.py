from PIL import Image
from PIL import ImageFont, ImageDraw


def render_text(FLAG):
    char_width = 330 / len("gccctf{data_designer}")
    # FLAG = "gccctf{data_designer}".upper()

    FINAL_W = char_width * len(FLAG)
    FINAL_H = 32

    image = Image.new("RGBA", (3 * FINAL_W, 3 * FINAL_H), (255, 255, 255))
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 75)
    d_usr = ImageDraw.Draw(image)
    d_usr.fontmode = "1" # AA?
    d_usr.text((0, 0), FLAG, (0, 0, 0), font=font)

    img_resized = image.resize((FINAL_W, FINAL_H), Image.ANTIALIAS)
    return img_resized
