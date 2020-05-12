import os, sys, stat
import re
import fileinput
import shutil

def impostaRadice2(message="Prego inserire posizione e nome del file con la lista:"):
    print("Prego inserire posizione e nome del file con la lista:")
    radice = input()
    while True:
        if os.path.exists(radice) is True:
            return radice
        else:
            print("File non trovato!")
            print("Prego inserire un file valido.")
            radice = input()

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

def type_analyzer(nome):
    crismTypes = ["ATO", "MSW", "MSP", "FRT", "FRS", "HRL", "HRS", "EPF", "HSP", "HSV"]
    if nome[0:3] == "ESP" or nome[0:3] == "PSP":
        return "HiRISE"
    elif re.match(r"H[0-9][0-9][0-9][0-9]", nome[0:5]):
        return "HRSC"
    elif re.match(r"[A-Z][0-9][0-9]_", nome[0:4]):
        return "CTX"
    elif nome[0:3] in crismTypes:
        return "CRISM"

hirises = set()
hrsc = set()
crism = set()
ctx = set()

print("Si vuole estrarre da un solo file o da più di uno?")
print("1 - Singolo file")
print("2 - Da vari file")
singomulti = input()
while singomulti!="1" and singomulti!= "2":
    print("Si prega di inserire 1 o 2:")
    singomulti = input()

files = []
if singomulti == "1":
    files.append(impostaRadice2("Prego inserire posizione e nome del file:"))
else:
    print("Inserire i file separati da virgole (es. file1.txt,file2.csv,file3.dat)")
    multipli = input().split(",")
    x = 0
    y = len(multipli)
    while x < y:
        if os.path.exists(multipli[x]) is False:
            print("Il file ", multipli[x], "non esiste o non si trova nella posizione indicata. Si vuole sostituire questo elemento?")
            localresponse = yesno()
            if localresponse:
                multipli[x] = impostaRadice2()
            else:
                multipli.remove(multipli[x])
        x += 1
    files = files + multipli

for file in files:
    with open(file, "r") as fileopen:
        for row in fileopen:
            idrow = row[6:-2]
            type = type_analyzer(idrow)
            if type == "HiRISE":
                hirises.add(idrow[0:15])
            elif type == "HRSC":
                hrsc.add(idrow)
            elif type == "CRISM":
                crism.add(idrow)
            elif type == "CTX":
                ctx.add(idrow)

print("Si preferisce l'output in file singoli o in un unico file?")
print("1 - File separati per sensore")
print("2 - File unico")

response = input()
while response!="1" and response!= "2":
    print("Si prega di inserire 1 o 2:")
    response = input()

if response == "1":
    if len(hirises) > 0:
        with open("HiRISEs.txt", "a") as f:
            for x in hirises:
                f.write(x+"\n")
    if len(hrsc)>0:
        with open("HRSCs.txt", "a") as f:
            for x in hrsc:
                f.write(x+"\n")
    if len(crism)>0:
        with open("CRISMs.txt", "a") as f:
            for x in crism:
                f.write(x+"\n")
    if len(ctx)>0:
        with open("CTXs.txt", "a") as f:
            for x in ctx:
                f.write(x+"\n")
else:
    with open("Immagini.txt", "w") as f:
        if len(hirises) > 0:
            f.write("HiRISE\n")
            for x in hirises:
                f.write(x+"\n")
            f.write("\n")
        if len(ctx) > 0:
            f.write("CTX\n")
            for x in ctx:
                f.write(x+"\n")
            f.write("\n")
        if len(hrsc) > 0:
            f.write("HRSC\n")
            for x in hrsc:
                f.write(x+"\n")
            f.write("\n")
        if len(crism) > 0:
            f.write("CRISM\n")
            for x in crism:
                f.write(x+"\n")
            f.write("\n")


input("Processo completato! Premere invio per chiudere")
