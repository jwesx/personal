import math

import cv2
import numpy as np
import os
import time

muito_norm = [
    '@', '#', 'S', '%', '&', '$', 'B', '8', 'W', 'M', 'O', 'Q', 'G', 'D', 'A', 'E', 'F', 'H', 'K', 'P', 'R', 'T', 'Y', 'U', 'V', 'Z',
    'X', 'I', 'L', 'N', 'C', 'J', '0', '1', '2', '3', '4', '5', '6', '7', '9', '>', '<', '=', '?', '!', '+', '*', ':', ';', '^', '(', ')',
    '[', ']', '{', '}', '|', '\\', '/', '_', '-', '`', '"', "'", ',', '.', '~', ' '
]
muito_inv = [
    ' ', '~', '.', ',', "'", '"', '`', '-', '_', '/', '\\', '|', '{', '}', '[', ']', ')', '(', '^', ';', ':', '*', '+', '!', '?', '=', '<', '>',
    '9', '7', '6', '5', '4', '3', '2', '1', '0', 'J', 'C', 'N', 'L', 'I', 'X', 'Z', 'V', 'U', 'Y', 'T', 'R', 'P', 'K', 'H', 'F', 'E', 'A', 'D', 'G',
    'Q', 'O', 'M', 'W', '8', 'B', '$', '&', '%', 'S', '#', '@'
]

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

ASCII_CHARS = [muito, small_norm, small_inv]

ascii_util = 0
mirror_bool = True

def cycle_ascii():
    global ascii_util
    key = cv2.waitKey(1)

    if key == 119:  # 'g'
        ascii_util += 1
        ascii_util %= len(ASCII_CHARS)
    elif key == 115:  # 'h'
        ascii_util -= 1
        ascii_util %= len(ASCII_CHARS)
    return ascii_util
   
def cycle_mirror():
    global mirror_bool
    key = cv2.waitKey(1)
    
    if key == 97: #should be 'a'
        mirror_bool = not mirror_bool
    
    return mirror_bool

def nothing(x):
    pass

def gray_to_ascii(image, new_width, mirrored):
    ascii_util = cycle_ascii()
    divisor = 255 // (len(ASCII_CHARS[ascii_util]) - 1)

    (original_width, original_height) = image.shape
    aspect_ratio = original_width / original_height
    new_height = int(aspect_ratio * new_width * 0.5)
    resized_image = cv2.resize(image, (new_width, new_height))

    ascii_str = ""
    if mirrored:
        for row in resized_image:
            line_str = "" 
            for pixel in row:
                index = math.floor(pixel / divisor)
                if index >= len(ASCII_CHARS[ascii_util]):
                    index = len(ASCII_CHARS[ascii_util]) - 1
                line_str = ASCII_CHARS[ascii_util][index] + line_str
            ascii_str += line_str + "\n"
    else:
        for row in resized_image:
            for pixel in row:
                index = math.floor(pixel / divisor)
                if index >= len(ASCII_CHARS[ascii_util]):
                    index = len(ASCII_CHARS[ascii_util]) - 1
                ascii_str += ASCII_CHARS[ascii_util][index]
            ascii_str += "\n"

    ascii_str += f"\n{ascii_util}"
    
    return ascii_str

def main():
    i = 0

    prev_frame = 0
    curr_frame = 0

    #define a camera acessada (0 é padrão do dispositivo)
    cam = cv2.VideoCapture(0)
    slider = cv2.namedWindow('Slider')
    cv2.createTrackbar('widsld', 'Slider', 200, 500, nothing)

    #loop deixa aberto
    while True:
        #dois valores, um pra checar se, de fato, está carregando, e frame é a imagem da câmera em si
        check, frame = cam.read()

        if not check:
            break

        curr_frame = time.time()
        fps = 1/(curr_frame - prev_frame)
        prev_frame = curr_frame

        fps = int(fps)
        fps = str(fps)

        width = cv2.getTrackbarPos('widsld', 'Slider')

        if width <= 16:
            width = 200
        
        mirror_bool = cycle_mirror()

        #seta um fram cinza,
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2GRAY)
        #usa o cinza pra rodar transformar em ascii (facilitando -> deixa em apenas uma reta 0 à 255)
        ascii_art = gray_to_ascii(gray_frame, width, mirror_bool) # 16 -> 200; 5 -> 640

        cv2.resizeWindow('Slider', (100, 0))

        if not mirror_bool:
            #mostra o original e o cinza, por motivos de debug
            cv2.imshow('Original', frame)
            cv2.imshow('Cinza', gray_frame)
        else:
            cv2.imshow('Original', cv2.flip(frame, 1))
            cv2.imshow('Cinza', cv2.flip(gray_frame, 1))
        

        #e, no cmd, o ascii
        print((ascii_art) + f'\n{fps}')
        i += 1

        if (i >= 25):
            os.system('cls')
            i = 0

        #if cv2.waitKey(1) == 103:
        #    os.system('cls')

        if cv2.waitKey(1) == 27:  # esc
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()