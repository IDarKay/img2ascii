from cv2 import cv2
import numpy as np
from PIL import Image, ImageFont, ImageDraw, ImageOps


def main():
    font = ImageFont.truetype("DejaVuSansMono.ttf", size=10 * 1)
    chars = '@%#*+=-:. '
    #chars = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
    char_mat = []
    char_width, char_height = font.getsize("A")
    for c in chars:
        img = Image.new("L", (char_width, char_height), 255)
        draw = ImageDraw.Draw(img)
        draw.text((0,0), c, fill=0, font = font)
        img = img.crop(img.getbbox())
        char_mat.append(np.array(img))
    num_char = len(char_mat)
    char_part = num_char / 255

    vc = cv2.VideoCapture(0)

    if vc.isOpened():
        rval, frame = vc.read()
    else:
        rval = False

    while rval:
        rval, frame = vc.read()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        width, height = frame.shape
        char_height, char_width = font.getsize("A")
        clear_height = (char_height * (height // char_height))
        clear_width = (char_width * (width // char_width))

        # clear useless
        frame[clear_width:, clear_height:] = 0
        for x in range(0, clear_width, char_width):
            for y in range(0, clear_height, char_height):
                frame[x: x + char_width, y: y + char_height] = char_mat[min(int(np.mean(frame[x: x + char_width, y: y + char_height]) * char_part), num_char - 1)]

        cv2.imshow("yop", frame)

        key = cv2.waitKey(33)  # 50ms pause -> ~20fps
        # Press echap to end
        if key == 27:
            break


if __name__ == '__main__':
    main()