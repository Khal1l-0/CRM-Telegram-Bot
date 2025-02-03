import logging

from PIL import Image, ImageDraw, ImageFont


async def gen_certificate(name):
    image = Image.open("app/res/pattern/cert.jpg")
    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype(f'app/res/font/Anastasia.ttf', 120)
    image_width, image_height = image.size

    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    x = (image_width - text_width) // 2
    y = 660

    draw.text((x, y), name, font=font, fill="black")
    image.save(f"app/res/certificates/{name}.jpg")

