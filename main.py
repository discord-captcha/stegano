# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
import base64
import binascii
import time
import hashlib

from Crypto.Util import Counter
from PIL import Image
import argparse
from cryptography.fernet import Fernet

parser = argparse.ArgumentParser()
parser.add_argument("--input", required=True, help="input to decrypt or encrypt")
parser.add_argument("--password", required=True, help="Pass to encrypt message in image")
parser.add_argument("--output", help="input to decrypt or encrypt")
parser.add_argument("--decrypt", help="echo the string you use here", action="store_true")
parser.add_argument("--encrypt", help="echo the string you use here", action="store_true")
parser.add_argument("--debug", help="echo the string you use here", action="store_true")
parser.add_argument("--text_file", help="Message to add if encrypting")
args = parser.parse_args()
path = args.input
if args.debug is not None:
    debug = args.debug
else:
    debug = False
bit_size = 1000000


def asc_to_bit(message_content):
    message_content=message_content.decode()
    # Message to binary
    bitMessage = ""
    count = 0
    print('Translating messages to bits')
    #print(message_content)
    for i in message_content:
        count += 1
        percent = int((count / len(message_content)) * 100)
        percent_str = str(percent) + '%'
        print(percent_str, end='\r')
        # print((format(ord(i), '08b')))
        bitMessage += (format(ord(i), '08b'))
    # print("taille en bit :", len(bitMessage))
    #    for i in range(len(newMessage)-1):
    #        print(newMessage[i])
    print()
    # print(str(len(message_content)*8))
    count = 0
    while len(bitMessage) != bit_size:
        count += 1
        bitMessage += '00000000'
    # print("taille en bit :", len(bitMessage))
    # print("Added", str(8*count), "bits")
    time.sleep(1)
    # print("BitMessage = ", bitMessage[:24])
    if debug:
        print("First 24: ", bitMessage[:24])
    return bitMessage


def bit_to_asc(bit_content):
    # print(len(bit_content), "bits recieved",)
    n = 8
    bit_content = [bit_content[i:i + 8] for i in range(0, len(bit_content), n)]
    if debug:
        print("First 24: ", "".join(bit_content)[:24])
    msg = ""
    for char in bit_content:
        if char == "00000000":
            continue
        # print("char is ", char)
        ord_number = int(char, 2)
        # print(ord_number)
        char_value = chr(ord_number)
        msg += char_value
    msg = msg.strip()
    #print("------------ message ------------")
    #print(msg)
    #print("------------ message ------------")

    return msg


def encrypt(image_path, message_content, password_value):
    img = Image.open(image_path)
    exif_value = img.info.get("exif")
    img = img.convert(mode='RGB')
    bits_total = ''
    #print(type(message_content))
    message_content = cipher(password_value, message_content)
    #print(message_content)
    # print(img.mode)
    msg = asc_to_bit(message_content)
    size = img.width * img.height
    if size < bit_size + 24:
        print("Image need to be at least 1,000,024 pixels, size is :", size, "pixels")
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
            percent = str(int((usable_len / bit_size) * 100)) + '%'
            print(percent, end='\r')
            for y in range(0, img.height):
                new_pixels = []
                if x == 0 and y <= 8:
                    # print(x, y)
                    continue
                pixels = img.getpixel((x, y))
                for pixel in pixels:
                    if debug:
                        if usable_len == 24:
                            print("good mdg =", msg[:24])
                            print("made msg =", bits_total)
                            quit(0)
                    usable_len += 1
                    bits = format(pixel, '08b')
                    # print("previous:",  bits)
                    try:
                        bits = bits[:7] + msg[usable_len - 1]
                        bits_total += msg[usable_len - 1]
                        if debug:
                            print("MSG = ", bits)
                        if usable_len > bit_size:
                            break
                    except IndexError:
                        bits = bits
                    # print("then:",  bits)
                    new_pixel = int(bits, 2)
                    new_pixels.append(new_pixel)
                if debug:
                    print("New image content is :", pixels)
                img.putpixel((x, y), tuple(new_pixels))
                pixels_new = img.getpixel((x, y))
                if debug:
                    print("OldPixels(", x, ",", y, ") is ", pixels)
                    print("NewPixels(", x, ",", y, ") is ", pixels_new)
                if usable_len > bit_size:
                    print("100%")
                    # print(usable_len)
                    return img, exif_value
                # quit(0)


def decrypt(image_path, password_value):
    img = Image.open(image_path)
    img = img.convert(mode='RGB')
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
        # print("y = ", y)
        pixels = img.getpixel((0, y))
        for pixel in pixels:
            # print(pixel)
            bits = format(pixel, '08b')
            # print(bits[-1])
            dec_type += bits[-1]
            # print(dec_type)
    # print("Dec_type =", dec_type)
    dec_type = dec_type[::-1]
    # print("Dec_type =", dec_type)
    dec_type = int(dec_type, 2)
    # print("Dec_type =", dec_type)
    # print('type is :', len(dec_type), dec_type)
    print("Decoding message")
    while usable_len < bit_size:
        for x in range(img.width):
            percent = int((usable_len / bit_size) * 100)
            percent_str = str(percent) + '%'
            if percent > 100:
                print("100%", end='\r')
                # print(x,y)
                # print("There is an error with the file decrypting please retry, range exceeded :", usable_len)
                break
            print(percent_str, end='\r')
            for y in range(0, img.height):
                new_pixel = []
                if x == 0 and y <= 8:
                    # print(x, y)
                    continue
                pixels = img.getpixel((x, y))
                # print(pixel)
                for pixel in pixels:
                    if debug:
                        if usable_len > 24:
                            print(msg)
                            quit(0)
                    usable_len += 1
                    bits = format(pixel, '08b')
                    if debug:
                        print("MSG = ", bits, "LSB =", bits[-1])
                    msg += bits[-1]
                    # print("msg", msg)
                    if usable_len > bit_size:
                        msg = msg[0:bit_size:1]
                if debug:
                    print("ReadPixels(", x, ",", y, ")  is ", pixels)
    # print(pixels)
    if dec_type == 1:
        print("100%")
        #print("MSG : ", bit_to_asc(msg))
        return decipher(password_value, bit_to_asc(msg))


def cipher(key, plaintext):
    f = Fernet(key)
    plaintext = plaintext.encode('utf-8')
    token = f.encrypt(plaintext)
    return token


def decipher(key, ciphertext):
    ciphertext = ciphertext.encode('utf-8')
    #print("CIPHER TEXT TYPE : ", type(ciphertext))
    f = Fernet(key)
    decrypted = f.decrypt(ciphertext).decode('utf-8')
    return decrypted


def bsd_checksum(string):
    file_content = string.encode()
    checksum = 0
    for char in file_content:
        checksum = (checksum >> 1) + ((checksum & 1) << 15)
        checksum += char
        checksum &= 0xffff
    return checksum


if __name__ == '__main__':

    # print("IV IS:", iv)
    password = args.password
    password = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

    if args.decrypt and args.encrypt:
        print("You need to chose between decrypt or encrypt.")
        quit(1)
    if args.decrypt:
        if args.text_file is not None:
            print("Do not add a message if decrypting... Ignoring.")

        message = decrypt(path, password)
        print("Message is : ")
        print(message.strip())

    if args.encrypt:
        if args.text_file is not None:
            if args.output is not None:
                # print(args.encrypt)
                text_file = args.text_file
                with open(text_file) as f:
                    message = f.read()
                    # print(message)
                img_enc, exif = encrypt(path, message, password)
                picture_rgb = img_enc.convert(mode='RGB')  # convert RGBA to RGB
                # picture_8bit = picture_rgb.quantize(colors=256, method=Image.MAXCOVERAGE)
                picture_rgb.save(args.output, "PNG", exif=exif)
                print("Exif", exif)
                print("Image saved to", args.output)
            else:
                print("--output is needed")
        else:
            print("Message needs to have a value")
