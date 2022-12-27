from PIL import Image, ImageDraw, ImageFont


def imagens_pericia(valor, pericia, resultado, nome):
    calibriz_font = r'CALIBRIZ.TTF'
    imagem = Image.open('Imagens/dado.png')
    font_num = ImageFont.truetype(calibriz_font, 55 if len(valor) < 2 else 110//len(valor))
    font_value = ImageFont.truetype(calibriz_font, 30)
    draw = ImageDraw.Draw(imagem)
    val_num = (186 if len(valor) == 1 else 172 + len(valor), 115 + len(valor)*4)
    preto = (0, 0, 0)
    draw.text(val_num, valor, font=font_num, fill=(23, 73, 110))
    response = [nome, pericia, resultado]
    for c, item in enumerate(response):
        draw.text((10, 255 + (30*c)), item, font=font_value, fill=preto)
    imagem.save(f'Imagens/resultado.png')