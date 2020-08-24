from urllib import request
import re
import time
import socket
def getYear():
    return str(time.gmtime(time.time()).tm_year)

def formatDate(date):
    date = date.split(".")
    date[1] = ["Janvier","Fevrier","Mars","Avril","Mai", "Juin", "Juillet", "Aout","Septembre","Octobre","Novembre", "Decembre"][int(date[1])-1]
    date[2] = "20"+date[2]
    return " ".join(date)
        
        

def getPlayerLastResult(name):
    reponse = str(request.urlopen("http://www.tennisendirect.net/atp/"+name+"/?y="+getYear()).read())
    if "404 -" in reponse: return ""
    debut = reponse.find("tour_head")
    debut = reponse.find("tour_head",debut+1)
    results = re.findall(">[^<^>]+<",reponse[debut:debut+400])
    results = [*map(lambda s: s[1:len(s)-1], results)]
    if len(results)> 5:
        for i in range(5,len(results)):
            if len(results[i])==1: results[i] = '('+results[i]+')'     
        results = results[0:4] + ["".join(results[4:])]
    debut = re.search('rowspan="[0-9]" class="w200"',reponse).span()[0]
    tournoi = re.findall(">[^<^>]+</a>", reponse[debut:debut+400])[0]
    tournoi = tournoi[1:len(tournoi)-4]
    return results + [tournoi]
    


year = getYear()

rafa = "rafael-nadal"
djoko = "novak-djokovic"
fede = "roger-federer"
waw = "stanislas-wawrinka"
players = {"nadal":rafa, "rafa":rafa, "nad":rafa, "djokovic":djoko, "djoko":djoko,
           "djoker":djoko,"nole":djoko,"federer":fede, "roger":fede,"fedex":fede,
           "waw":waw,"wawrinka":waw,"stan":waw,"stanislas":waw, "monfils":"gael-monfils"}

connected = socket.gethostbyname(socket.gethostname())!="127.0.0.1"
if connected:
    player = input("Joueur : ").lower()
    while player not in players and not player.isalpha() and len(player.split())!=2:
        player = input("Veuillez entrer un nom correct :")
        
    if player in players: player = players[player]
    else: player = "-".join(player.split())
    contents = getPlayerLastResult(player)
    if contents:
        date,tour,gagnant,perdant, score,tournoi = contents
        date = formatDate(date)
        print(gagnant, "-", perdant)
        print(score)
        print("Vainqueur :",gagnant)
        print("Tournoi :",tournoi)
        print("Tour : ", tour)
        print(date)
    else:
        print("Désolé ce joueur n'existe pas")
        
else:
    print(":/ Votre ordinateur n'est pas connecté à internet")
input()
