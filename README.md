[TOC]
  
Authors: Aymerick Bres, Sarah Costa, Romain DUSI, Thomas Le Martelot, Maël Turon

# How it works 

The python script imports several packages that are listed in requirements.txt 
First the message is encrypted using fernet algorithm and then setting each char as bytes. The bytes message is then iterated through one bit at a time and each are written on the least significant bits of each pixel. 
Using png RGB format an image is composed of pixels which are in turn composed as such : (0-255;0-255;0-255). Each pixel uses a total of 3 bytes and on each bytes the least significant bit can be modified without really altering the image. 

# Script usage

Script is used to encrypt and set a message into an image. 
The message is encrypted using a [fernet](https://cryptography.io/en/latest/fernet/) algorithm.

## Decrypting : 
```bash
stegano.exe --decrypt --input <image_path> --password <password>
```
## Encrypting :
```bash
stegano.exe --encrypt --input <image_path> --output <output_image_path> --text_file <test_file_path> --password <password>
```
