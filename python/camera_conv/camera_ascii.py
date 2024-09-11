import math

import cv2
import numpy as np
import os

muito = [
    '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ' ',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ':', ';', '<', '=', '>', '?',
    '@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    '[', '\\', ']', '^', '_', '`',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '{', '|', '}', '~'
]
small_norm = [
    '@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' '
]
small_inv = [
    ' ', '.', ',', ':', ';', '+', '*', '?', '%', 'S', '#', '@'
]

ASCII_CHARS = small_inv

def nothing(x):
    pass
def gray_to_ascii(image, new_width):
    divisor = 255 // (len(ASCII_CHARS) - 1)

    (original_width, original_height) = image.shape
    aspect_ratio = original_width / original_height
    new_height = int(aspect_ratio * new_width * 0.5)
    resized_image = cv2.resize(image, (new_width, new_height))

    ascii_str = ""
    for row in resized_image:
        for pixel in row:
            index = math.floor(pixel / divisor)
            if index >= len(ASCII_CHARS):
                index = len(ASCII_CHARS) - 1
            ascii_str += ASCII_CHARS[index] # relativo ao ascii_chars
        ascii_str += "\n"
    return ascii_str

def main():
    #define a camera acessada (0 é padrão do dispositivo)
    cam = cv2.VideoCapture(0)
    slider = cv2.namedWindow('Slider')
    cv2.createTrackbar('widsld', 'Slider', 100, 1000, nothing)

    #loop deixa aberto
    while True:
        #dois valores, um pra checar se, de fato, está carregando, e frame é a imagem da câmera em si
        check, frame = cam.read()

        if not check:
            break

        width = cv2.getTrackbarPos('widsld', 'Slider')

        if width == 0:
            width = 200

        #seta um fram cinza,
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        #usa o cinza pra rodar transformar em ascii (facilitando -> deixa em apenas uma reta 0 à 255)
        ascii_art = gray_to_ascii(gray_frame, width) # 16 -> 200; 5 -> 640

        #mostra o original e o cinza, por motivos de debug
        cv2.imshow('Original', frame)
        cv2.imshow('Cinza', gray_frame)

        #e, no cmd, o ascii
        print(ascii_art)

        if cv2.waitKey(1) == 27:  # esc
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
