#Made by Adriano Tullo :)
#versione 1.0
#Inizio script, buona lettura
import urllib.request, urllib.error, urllib.parse
import os
import re
import fileinput
import shutil
import sys

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

if sys.version_info[0] < 3:
    raise Exception("Per questo script è necessario utilizzare Python 3. \n"
                    "Da terminale: python3 nomescript.py")

try:
    import requests
except:
    print("Si prega di installare la requests library via 'pip install requests'")
    print("Si vuole installarlo ora?")
    rensponse =  yesno()
    if rensponse is True:
        try:
            import subprocess
            def install(package):
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            install("requests")
        except:
            print(Exception)
            input()
    else:
        quit()

print("Il presente script permette di scaricare immagini HiRISE in vari formati (per ora solo bw in jp2) con i relativi label.")
print("E' in programma l'integrazione con gli altri script.")
print("Per comodità, le immagini devono essere collocate in un file lista nel quale si riporta un ID (Ad es. ESP_047158_2"
      "020) per riga.")
print("(Se il file si trova nella stessa cartella di questo script (Consigliato) basta riportare il nome)")



def impostaRadice():
    print("Prego inserire posizione e nome del file con la lista:")
    radice = input()
    while True:
        if os.path.exists(radice) is True:
            return radice
        else:
            print("File non trovato!")
            print("Prego inserire un file valido.")
            radice = input()

def downloader(nomefile, url):
    with open(nomefile, "wb") as file:
        downloadFile = requests.get(url, stream=True)
        print("\nDownloading ", nomefile)
        total_size = downloadFile.headers.get("content-length")
        if total_size == None:
            print("Downloading in progress...")
            for chunck in downloadFile.iter_content(chunk_size=4096):
                file.write(chunck)
        else:
            progress = 0
            total_size = int(total_size)
            for pezzetto in downloadFile.iter_content(chunk_size=4096):
                progress += len(pezzetto)
                file.write(pezzetto)
                fatto = int(50 * progress / total_size)
                sys.stdout.write("\r[%s%s]%s" % ('=' * fatto, ' ' * (50-fatto), str((fatto*2))+"%" ) )
                sys.stdout.flush()


def download(id):
    orbit = id[4:8]
    typology = id[0:3]
    flUrl = "https://hirise-pds.lpl.arizona.edu/download/PDS/RDR/" + typology + "/ORB_" + orbit + "00_" + orbit +"99/" + id + "/"+ id + "_RED.JP2"
    flName = flUrl[-23:]
    labelUrl = "https://hirise-pds.lpl.arizona.edu/PDS/RDR/" + typology + "/ORB_" + orbit + "00_" + orbit + "99/"+ id +"/"+ id +"_RED.LBL"
    labelName = labelUrl[-23:]
    try:
        downloader(flName,flUrl)
        downloader(labelName,labelUrl)
    except:
        print("Download error: " + id + " non sembra disponibile al download.")


radice = impostaRadice()
imago = []

if not os.path.isdir("Immagini"):
    os.makedirs('Immagini')

os.chmod('Immagini', 0O777)

with open(radice,"r") as lista:
    for row in lista:
        imago.append(row)

os.chdir("Immagini")

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

for id in imago:
    download(id)

input("Processo completato, premere un tasto qualsiasi per uscire")