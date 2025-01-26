from colorthief import ColorThief

def extract_main_colors(image_path: str, num_colors=9):
    """
    Extrai as cores principais de uma imagem.

    Args:
        image_path (str): Caminho para a imagem.
        num_colors (int): Número de cores principais a extrair.

    Returns:
        list: Lista de cores principais em formato RGB.
    """
    color_thief = ColorThief(image_path)
    return color_thief.get_palette(color_count=num_colors)



if __name__ == "__main__":
    colors = extract_main_colors("image.png", num_colors=8)
    print(colors)