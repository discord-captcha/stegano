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
        bitMessage += (format(ord(i), '08b'))
    # print("taille en bit :", len(bitMessage))
    #    for i in range(len(newMessage)-1):
    #        print(newMessage[i])
    # print("taille en bit :", len(bitMessage))
    byte_array = "abc".encode()
    binary_int = int.from_bytes(byte_array, "big")
    bitMessage = bin(binary_int)

    while len(bitMessage) != bit_size:
        bitMessage += '00000000'
    return bitMessage


def bittoasc(bit_content):
    print("on envoie", len(bit_content))
    binary_int = int(bit_content, 2)
    byte_number = binary_int.bit_length() + 7 // 8
    binary_array = binary_int.to_bytes(byte_number, "big")
    msg = binary_array.decode()
    print(msg)
    return "C'est ok mais c'est long"


def encrypt(image_path, message_content):
    img = Image.open(image_path)
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
        new_pixel = []
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

            new_pixel.append(int(bits, 2))
            # print(pixels)
        # print(pixels)
        # print("New image __ type: ", tuple(new_pixel))
        img.putpixel((0, y), tuple(new_pixel))

    print("Encoding message")
    while usable_len < bit_size:
        for x in range(img.width):
            print(usable_len)
            for y in range(0, img.height):
                new_pixel = []
                if x == 0 and y <= 8:
                    # print(x, y)
                    continue
                pixels = img.getpixel((x, y))
                # print(pixel)
                for pixel in pixels:
                    usable_len += 1
                    bits = format(pixel, '08b')
                    # print("previous:",  bits)
                    try:
                        bits = bits[:7] + msg[usable_len]
                        if usable_len > bit_size:
                            break
                    except IndexError:
                        bits = bits
                    # print("then:",  bits)
                    new_pixel.append(int(bits, 2))
                # print(new_pixel)
                # print(pixels)
                # print("New image __ content:", tuple(new_pixel))
                img.putpixel((x, y), tuple(new_pixel))
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
        pixels = img.getpixel((0, y))
        for pixel in pixels:
            bits = format(pixel, '08b')
            dec_type += bits
    print('type is :', dec_type)
    print("Decoding message")
    while usable_len < bit_size:
        for x in range(img.width):
            print(usable_len)
            for y in range(0, img.height):
                new_pixel = []
                if x == 0 and y <= 8:
                    # print(x, y)
                    continue
                pixels = img.getpixel((x, y))
                # print(pixel)
                for pixel in pixels:
                    usable_len += 1
                    bits = format(pixel, '08b')
                    msg += bits[-1]
                    # print("msg", msg)
                    if usable_len > bit_size:
                        msg = msg[0:bit_size:1]
                        print(usable_len)
                        print("on sort de la boucle")
                        #print(bittoasc(msg))
                        return bittoasc(msg)
    print(msg)


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
            img = encrypt(path, message)
            img.save("elephant2.png")

        else:
            print("Message needs to have a value ")
