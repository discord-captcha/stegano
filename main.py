# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
from io import BytesIO
from bitstring import BitArray
from PIL import Image
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--filename", required=True, help="Filename to decrypt or encrypt")
parser.add_argument("--decrypt", help="echo the string you use here", action="store_true")
parser.add_argument("--encrypt", help="echo the string you use here", action="store_true")
parser.add_argument("--text_file", help="Message to add if encrypting")
args = parser.parse_args()
path = args.filename
bit_size = 1000000


def asctobit(message_content):
    # Message to binary
    bitMessage = ""
    for i in message_content:
        # print((format(ord(i), '08b')))
        bitMessage += (format(ord(i), '08b'))
    # print("taille en bit :", len(bitMessage))
    #    for i in range(len(newMessage)-1):
    #        print(newMessage[i])
    while len(bitMessage) != bit_size:
        bitMessage += '00000000'
    # print("taille en bit :", len(bitMessage))

    # print("BitMessage = ", bitMessage[:24])
    return bitMessage


def bittoasc(bit_content):
    print("on envoie", len(bit_content))
    n = 8
    bit_content = [bit_content[i:i + 8] for i in range(0, len(bit_content), n)]
    msg = ""
    for char in bit_content:
        if char == "00000000":
            continue
        # print("char is ", char)
        ord_number = int(char, 2)
        # print(ord_number)
        char_value = chr(ord_number)
        msg += char_value
    print(msg.strip())
    return " "


def encrypt(image_path, message_content):
    img = Image.open(image_path)
    bits_total=''

    # print(img.mode)
    msg = asctobit(message_content)
    size = img.width * img.height
    if size < bit_size + 24:
        print("Image need to be at least 1,000,008 pixels")
        quit(0)
    number_char = int(size / 8)
    # print(img.width, img.height, size, "number of char :", number_char)
    usable_len = 0
    count = 0
    enc_type = '1'
    print("Setting type as first 24 bits ")
    for y in range(0, 8):
        pixels = img.getpixel((0, y))
        new_pixels = []
        for pixel in pixels:
            count += 1
            # print("count: ", count)
            # print("len enc_type: ", len(enc_type))
            if count > len(enc_type):
                bit_value = '0'
            else:
                # print(pixel)
                bit_value = enc_type[count - 1]

            bits = format(pixel, '08b')
            # print("bit_value", bit_value)
            bits = bits[:7] + bit_value

            new_pixels.append(int(bits, 2))
            # print(pixels)
        # print(pixels)
        # print("New image __ type: ", tuple(new_pixel))
        img.putpixel((0, y), tuple(new_pixels))

    print("Encoding message")
    while usable_len < bit_size:
        for x in range(img.width):
            # print(usable_len)
            for y in range(0, img.height):
                new_pixels = []
                if x == 0 and y <= 8:
                    #print(x, y)
                    continue
                pixels = img.getpixel((x, y))
                for pixel in pixels:
                    # if usable_len == 24:
                    #     print("good mdg =", msg[:24])
                    #     print("made msg =", bits_total)
                    #     quit(0)
                    usable_len += 1
                    bits = format(pixel, '08b')
                    # print("previous:",  bits)
                    try:
                        bits = bits[:7] + msg[usable_len-1]
                        bits_total += msg[usable_len-1]
                        #print("MSG = ", bits)
                        if usable_len > bit_size:
                            break
                    except IndexError:
                        bits = bits
                    # print("then:",  bits)
                    new_pixel = int(bits, 2)
                    new_pixels.append(new_pixel)
                # print(pixels)
                # print("New image __ content:", tuple(new_pixel))
                img.putpixel((x, y), tuple(new_pixels))
                pixels_new = img.getpixel((x, y))
                #print("OldPixels(", x, ",", y, ") is ", pixels)
                #print("NewPixels(", x, ",", y, ") is ", pixels_new)
                if usable_len > bit_size:
                    print(usable_len)
                    return img
                # quit(0)


def decrypt(image_path):
    img = Image.open(image_path)
    msg = ""
    size = img.width * img.height
    if size < bit_size + 24:
        print("Image need to be at least 1,000,008 pixels")
        quit(0)
    number_char = int(size / 8)
    # print(img.width, img.height, size, "number of char :", number_char)
    usable_len = 0
    dec_type = ''
    print("Getting type from first 24 bits ")
    for y in range(0, 8):
        #print("y = ", y)
        pixels = img.getpixel((0, y))
        for pixel in pixels:
            bits = format(pixel, '08b')
            dec_type += bits[:7]

    dec_type = dec_type[::-1]

    # print('type is :', len(dec_type), dec_type)
    print("Decoding message", dec_type)
    while usable_len < bit_size:
        for x in range(img.width):
            print(usable_len)
            for y in range(0, img.height):
                new_pixel = []
                if x == 0 and y <= 8:
                    #print(x, y)
                    continue
                pixels = img.getpixel((x, y))
                # print(pixel)
                for pixel in pixels:
                    # if usable_len == 24:
                    #     print(msg)
                    #     quit(0)
                    usable_len += 1
                    bits = format(pixel, '08b')
                    #print("MSG = ", bits)
                    #print(bits[-1])
                    msg += bits[-1]
                    # print("msg", msg)
                    if usable_len > bit_size:
                        msg = msg[0:bit_size:1]
                        #print(usable_len)
                        print("on sort de la boucle")
                        # print(bittoasc(msg))
                        #print(msg[:24])
                        return bittoasc(msg)
                #print("ReadPixels(", x, ",", y, ")  is ", pixels)


if __name__ == '__main__':
    if args.decrypt and args.encrypt:
        print("You need to chose between decrypt or encrypt.")
        quit(1)

    if args.decrypt:
        if args.text_file is not None:
            print("Do not add a message if decrypting... Ignoring.")

        message = decrypt(path)
        print(message.strip())

    if args.encrypt:

        if args.text_file is not None:
            # print(args.encrypt)
            text_file = args.text_file
            with open(text_file) as f:
                message = f.read()
                # print(message)
            img_enc = encrypt(path, message)
            img_enc.save("elephant2.png")
            print("Image saved to elephant2.png")

        else:
            print("Message needs to have a value ")
