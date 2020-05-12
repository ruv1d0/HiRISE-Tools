#Made by Adriano Tullo :)
#versione 1.0
#Inizio script, buona lettura
import urllib.request, urllib.error, urllib.parse
import os, sys, stat
import re
import fileinput
import shutil

if sys.version_info[0] < 3:
    raise Exception("Per questo script è necessario utilizzare Python 3. \n"
                    "Da terminale: python3 nomescript.py")

print("Il presente script permette di controllare online se immagini HiRISE sono parte di una stereocoppia, e nel caso "
      "cerca l'immagine della stereocoppia corrispondente e stima quale immagine è Left observing e quale Right.")
print("Alcune immagini precedenti al Dicembre 2008, cioè parte della Primary Science Phase (che iniziano per PSP) potrebbero non essere"
      " stimate correttamente ma possono essere gestite comunque dallo script.")
print("I risultati verrano riportati in un report testuale.")
print("Per comodità, le immagini devono essere collocate in un file lista nel quale si riporta un ID (Ad es. ESP_047158_2"
      "020) per riga.")
print("(Se il file si trova nella stessa cartella di questo script (Consigliato) basta riportare il nome)")


def yesno(answer="Nada"):
    yes= {"Y", "y", "yes", "Yes", "Fuck yeah", "Si", "s"}
    no = {"n", "N", "no", "No", "Naaa"}
    while True:
        scelta = input()
        if scelta in yes:
            return True
        if scelta in no:
            return False
        if scelta == "" and answer == "Hole":
            return ""
        else:
            print("Errore di input, si prega di rispondere Y o N")

def impostaRadice():
    print("Prego inserire posizione e nome del file con la lista:")
    radice = input()
    while True:
        if os.path.exists(radice) is True:
            return radice
        else:
            print("File non trovato!")
            print("Prego inserire un file valido.")

radice = impostaRadice()

lista = open(radice, "r")
imago = []
for row in lista:
    imago.append(row)
x = 0
y = len(imago)
while x < y:
    if imago[x][0:4] == "ESP_" or imago[x][0:4] == "PSP_":
        imago[x] = imago[x][0:15]
        x += 1
    else:
        print(imago[x] + "non è un formato valido e riconosciuto")
        print("Si vuole sostituire l'immagine?")
        risposta = yesno()
        if risposta is True:
            print("Con quale immagine?")
            imago[x] = input()
        else:
            print("L'immagine verrà ignorata.")
            imago.remove(imago[x])
            y = y-1

x = 0
y = len(imago)
stereos=[]
gemello=[]
while x < y:
    url = 'https://www.uahirise.org/' + imago[x]
    response = urllib.request.urlopen(url)
    webContent = response.read()
    flag = os.O_RDWR | os.O_CREAT
    path = './temp'
    mode = 0o666
    fileprova = os.open(path, flag, mode)
    encoding = 'utf-8'
    os.write(fileprova, (webContent.decode(encoding)).encode())
    os.close(fileprova)
    with open("temp")as f:
        if 'This is a stereo pair with ' in f.read():
            isstereopair = 1
        else:
            isstereopair = 0

    if isstereopair == 1:
        stereos.append(1)
        with open("./temp")as f:
            gemellocattivo = str(re.search('is a stereo pair with (.+?)title', f.read()))
            gemellocattivo = str(gemellocattivo[-19:-4])
        os.remove("./temp")
        gemello.append(gemellocattivo)
        print("L'immagine " + imago[x] + " è parte di una stereocoppia con " + gemellocattivo)
    else:
        stereos.append(0)
        gemello.append("Nada")
    x += 1

if 1 not in stereos:
    print("Purtroppo nessuna delle immagini è parte di una stereo coppia.")
    input("Premere un tasto qualsiasi per chiudere.")
    exit()

print("Stimare le immagini Left Observing e quelle Right Observing? (Y o N)")
rispostaAuto = yesno()
if rispostaAuto is True:
    print("Un attimo di pazienza...")
    x = 0
    y = len(imago)
    sinistra = []
    destra = []

    while x < y:
        if stereos[x] == 1:
            numImageImago = int(imago[x][4:10])
            numImageGeme = int(gemello[x][4:10])
            if numImageImago < numImageGeme:
                urlanag = "https://www.uahirise.org/anaglyph/singula.php?ID=" + imago[x]
            else:
                urlanag = "https://www.uahirise.org/anaglyph/singula.php?ID=" + gemello[x]
            response = urllib.request.urlopen(urlanag)
            webContent = response.read()
            flag = os.O_RDWR | os.O_CREAT
            path = './temp2'
            mode = 0o666
            fileprova = os.open(path, flag, mode)
            encoding = 'utf-8'
            os.write(fileprova, (webContent.decode(encoding)).encode())
            os.close(fileprova)
            with open("temp2")as f:
                sinistroide = str(re.search('Left observation(.+?)class', f.read()))
                sinistroide = str(sinistroide[-16:-1])
            if sinistroide == imago[x]:
                sinistraTemp = sinistroide
                destraTemp = gemello[x]
            else:
                sinistraTemp = sinistroide
                destraTemp = imago[x]
            if sinistraTemp[0:3] == ("ESP" or "PSP") and destraTemp[0:3] == ("ESP" or "PSP"):
                os.remove("temp2")
                sinistra.append(sinistraTemp)
                destra.append(destraTemp)
            else:
                os.remove("temp2")
                if numImageImago > numImageGeme:
                    urlanag = "https://www.uahirise.org/anaglyph/singula.php?ID=" + imago[x]
                else:
                    urlanag = "https://www.uahirise.org/anaglyph/singula.php?ID=" + gemello[x]
                response = urllib.request.urlopen(urlanag)
                webContent = response.read()
                flag = os.O_RDWR | os.O_CREAT
                path = './temp2'
                mode = 0o666
                fileprova = os.open(path, flag, mode)
                encoding = 'utf-8'
                os.write(fileprova, (webContent.decode(encoding)).encode())
                os.close(fileprova)
                with open("temp2")as f:
                    sinistroide = str(re.search('Left observation(.+?)class', f.read()))
                    sinistroide = str(sinistroide[-16:-1])
                if sinistroide == imago[x]:
                    sinistraTemp = sinistroide
                    destraTemp = gemello[x]
                else:
                    sinistraTemp = sinistroide
                    destraTemp = imago[x]
                sinistra.append(sinistraTemp)
                destra.append(destraTemp)
                os.remove("temp2")
        x += 1

ricreare = False
if os.path.exists("Report.txt"):
    print("Attenzione il file Report.txt già esiste, si vuole specificare un altro nome (o verrà sovrascritto)?")
    ricreare = yesno()
    if ricreare is True:
        print("Quale nome dare al report?")
        nomefile = input()
        report = open(nomefile + ".txt", "w+")
else:
    report = open("Report.txt", "w+")
    ricreare = False

report.write("REPORT STEREO COPPIE HIRISE\n")
report.write("Grazie per aver utilizzato il mio script - A.\n\n")

report.write("IMMAGINE_INPUT      IMMAGINE_SOVRAPPOSTA\n")
x = 0
y = len(imago)
while x < y:
    if stereos[x] == 1:
        report.write(imago[x] + "       " + gemello[x] + "\n")
    x += 1

report.write("\nLe seguenti immagini non sono parte di una stereocoppia:\n")
x = 0
while x < y:
    if stereos[x] != 1:
        report.write(imago[x] + "\n")
    x += 1

report.write("\n\n")

if rispostaAuto is True:
    report.write("Segue la stima delle immagini left e right observing:\n")
    report.write("LEFT_OBSERVING        RIGHT_OBSERVING\n")
    x = 0
    y = len(sinistra)
    while x < y:
        report.write(sinistra[x] + "       " + destra[x] + "\n")
        x += 1

report.close()

print("Processo completato! Si vuole anche in formato compatibile con fogli di calcolo (.csv)? (Y o N)")
calc = yesno()
if calc is True:
    if ricreare is True:
        comic = open(nomefile + ".csv", "w+")
    else:
        comic = open("Report.csv", "w+")
    if rispostaAuto is False:
        comic.write("IMMAGINE_INPUT;IMMAGINE_SOVRAPPOSTA\n")
        x = 0
        y = len(imago)
        while x < y:
            if stereos[x] == 1:
                comic.write(imago[x] + ";" + gemello[x] + "\n")
            x += 1
        comic.write("\nLe seguenti immagini non sono parte di una stereocoppia:\n")
        x = 0
        while x < y:
            if stereos[x] != 1:
                comic.write(imago[x] + "\n")
            x += 1
        comic.write("\n\n")
    if rispostaAuto is True:
        comic.write("ID_COPPIA;LEFT_OBSERVING;RIGHT_OBSERVING\n")
        x = 0
        y = len(sinistra)
        while x < y:
            comic.write(sinistra[x] + "_" + destra[x] + ";" + sinistra[x] + ";" + destra[x] + "\n")
            x += 1
    comic.close()
    input("Processo completato! Premere invio per uscire")
else:
    exit()
