# -*- coding: utf-8 -*-

from flask import Flask, redirect, render_template, render_template_string, request, redirect, session
from random import randint
import hashlib

# MODULES PERSO 

from .model import bdd as bdd
from .controller import function as f
from .config import URL_PATHS

app = Flask(__name__)

app.template_folder= "template"
app.static_folder= "static"
app.config.from_object('App.config')

# PAGE Index 

@app.route("/")
@app.route("/index")
@app.route("/index/<infoMsg>")
def index(infoMsg=''): 
    return render_template("index.html", info=infoMsg)

# PAGE ADMINISTRATEUR

@app.route("/admin", methods=['GET'])
def admin(): 

    if f.is_connected() == "Connected" and f.is_admin() == "Admin":

        search_element = request.args.get("search")
        page = int(request.args.get("page")) 

        listeSats = []

        if search_element != "none": 
            msg_sat, listeSats = bdd.get_SatelliteDataWhere("nomSatellite LIKE '%{}%'".format(search_element))
        else: 
            msg_sat, listeSats = bdd.get_SatelliteData()

        msg_membre, listeMembre = bdd.get_membreData()
        msg_pays, listePays = bdd.get_paysData()
        msg_gp, listeGroupes = bdd.get_groupesData()

        n_sat = len(listeSats)

        if page<1:
            page = 1

        return render_template("/admin.html", membre=listeMembre, sats=listeSats, pays=listePays, n_sat=n_sat, groupes=listeGroupes, page=page, search=search_element, UP = URL_PATHS)

    else: 
        return redirect("/")

# PAGE SELECTIONNER SATELLITES A MONTRER
@app.route("/select_sat", methods=['GET'])
def select_sat(): 

    # ou on envoie le resultat de la selection de satellite
    action = request.args.get("action")
    sort = request.args.get("sort")

    msg_gp, listeGroupe = bdd.get_groupesData()

    msg_sat, listeSats = bdd.get_SatelliteData()

    return render_template("/select_sat.html", sats=listeSats, groupes=listeGroupe, action=action, sort=sort)

@app.route("/select_sat_add", methods=['GET'])
def select_sat_add(): 

    groupe = request.args.get("gp_nom") 
    msg_sat, listeSats = bdd.get_SatelliteData()

    return render_template("/select_sat_add.html", sats=listeSats, groupe_nom=groupe)

@app.route("/showAppGroups", methods=['POST'])
def satsInGroup(): 

    listeIDgroup = list(request.form.values())
    time = int(request.form["timeCompute"])
    deltaT = int(request.form["deltaT"])

    chaine = ""
    for i in range(len(listeIDgroup)): 
        if i != len(listeIDgroup)-1: 
            chaine+="idGroupe = {} OR ".format(listeIDgroup[i]) 
        else: 
            chaine+="idGroupe = {}".format(listeIDgroup[i])

    msg, listeIDSats = bdd.get_assGroupeSatelliteWhere(chaine)

    chaine2 = ""
    for j in range(len(listeIDSats)): 
        if j != len(listeIDSats)-1: 
            chaine2 += "idSatellite = {} OR ".format(listeIDSats[j]["idSatellite"])
        else: 
            chaine2 += "idSatellite = {}".format(listeIDSats[j]["idSatellite"])

    msg2, sat_data = bdd.get_SatelliteDataWhere(chaine2) 

    jsonliste = f.editTLEConfig(sat_data, time, deltaT)

    info = f.is_connected()
    if info != "needAuth":
        return render_template("cesium_app.html", data=jsonliste)
    else: 
        return render_template("index.html")

@app.route("/showApp", methods=['POST'])
def showApp():

    satnames = (list(request.form.keys()))
    time = int(request.form["timeCompute"])
    deltaT = int(request.form["deltaT"])

    chaine = "" 
    for i in range(len(satnames)):
        if i != len(satnames)-1:
            chaine += "nomSatellite = '{}' OR ".format(satnames[i])
        else: 
            chaine += "nomSatellite = '{}' ".format(satnames[i])


    msg, listeSats = bdd.get_SatelliteDataWhere(chaine)

    jsonliste = f.editTLEConfig(listeSats, time, deltaT) 

    info = f.is_connected()
    if info != "needAuth":
        return render_template("cesium_app.html", data=jsonliste)
    else: 
        return render_template("index.html")

# CONNEXION - DECONNEXION

@app.route("/signin")
def signin():
    return render_template("signin.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/index")

@app.route("/signup") 
def signup():
    return render_template("/signup.html")

@app.route("/connect", methods=['POST'])
def connect(): 

    login = request.form['login'] 
    password = request.form['mdp'] 
    
    msg = f.verify_user(login, password)
    

    if "idUser" in session: 
        return redirect("/index")
    else: # echec authentification
        return redirect("/signin")

@app.route("/parametres")
def param(): 

    return render_template("parametres.html")



# CONTACT

@app.route("/contact")
def contact(): 

    return render_template("/contact.html")

# SATELLITES 

@app.route("/deleteAllSats")
def del_all_sat():

    msg = bdd.del_AllSatData()
    return redirect("/admin?page=1&search=none")

@app.route("/deleteSat", methods=['POST'])
def deleteSat(): 

    idsat = request.form["deleteRowId"] 
    msg = bdd.del_SatData(idsat)

    return redirect("/admin?page=1&search=none")
    
@app.route("/addTLEinDB", methods=['POST']) 
def addTLEinDB():

    tle = request.form["tleInput"].split("\r\n")

    idUser = None
    if "idUser" in session:
        sat_data = f.getSatDataFromTLE(tle, "Ukn", "User")

        msg = bdd.addUp_SatData(sat_data, session["idUser"])

    else: 
        print("not connected")

    return redirect("/admin?page=1&search=none")

@app.route("/update_groupe", methods=['GET'])
def update_groupe(): 

    nom_groupe = request.args.get("gp_nom")

    try:
        tle_list = f.getTLEListFromURL(URL_PATHS[nom_groupe])
 
        chaine = ""
        for i in range(len(tle_list)): 
            sat_data = f.getSatDataFromTLE(tle_list[i], nom_groupe)

            if i != len(tle_list)-1:
                chaine += "nomSatellite = '{}' OR ".format(sat_data[0].replace("'", "")) 
            else: 
                chaine+= "nomSatellite = '{}'".format(sat_data[0].replace("'", "")) 
                    
            msg_addup = bdd.addUp_SatData(sat_data, session["idUser"]) 

        msg_sat, listeIDSat = bdd.get_satelliteIdWhere(chaine)
    
    except: 
        msg = "Fail to update groupe: NO URL known to update database"

    return redirect("/admin?page=1&search=none")

# a retravailler (plutot 'import')
"""@app.route("/update", methods=['GET'])
def update_gp(): 

    url_key = request.args.get("gp_nom")

    tle_list = get.getTLEListFromURL(URL_PATHS[url_key])
 
    # creer un groupe avec les satellites en question 
    nom_groupe = url_key
    couleur_groupe = "#fbff00"

    msg, groupeId = bdd.add_groupesData(nom_groupe, couleur_groupe)

    chaine = ""
    for i in range(len(tle_list)): 
        sat_data = get.getSatDataFromTLE(tle_list[i], nom_groupe)

        if i != len(tle_list)-1:
            chaine += "nomSatellite = '{}' OR ".format(sat_data[0].replace("'", "")) 
        else: 
            chaine+= "nomSatellite = '{}'".format(sat_data[0].replace("'", "")) 
                
        msg_addup = bdd.addUp_SatData(sat_data, session["idUser"]) 

    msg_sat, listeIDSat = bdd.get_satelliteIdWhere(chaine)

    msg_asso = bdd.add_assoGroupeSatellite(groupeId, listeIDSat)

    return redirect("/admin?page=1&search=none")"""


# AJOUTER UN MEMBRE

@app.route("/addMembre", methods=['POST'])
def addMembre(): 
    
    nom = request.form['nom'] 
    prenom = request.form['prenom'] 
    login = request.form['login'] 
    mdp = request.form['mdp'] 
    mail = request.form['mail'] 
    avatar = request.form['avatar'] 
    statut = request.form['statut']

    msg, lastId = bdd.add_membreData(nom, prenom, mail, login, mdp, statut, avatar)

    print(msg)
    return redirect("/")

@app.route("/turn_admin", methods=['POST'])
def turnAdmin(): 

    if f.is_connected() and f.is_admin(): 

        idUser = request.form["idmembre"]

        chaine = "idUser = {}".format(idUser)
        msg_get, membre = bdd.get_membreDataWhere(chaine)

        id = idUser
        nom = membre[0]["nom"]
        prenom = membre[0]["prenom"]
        login = membre[0]["login"]
        mail = membre[0]["mail"]
        motPasse = membre[0]["motPasse"]
        statut = 0
        avatar = membre[0]["avatar"] 

        msg_update = bdd.update_membreData(id, nom, prenom, mail, login, motPasse, statut, avatar)

        return redirect("/admin?page=1&search=none")
    
    else:
        return redirect("/")

@app.route("/update_membre", methods=['POST'])
def updateMembre(): 

    if f.is_connected(): 

        id = request.form["id"]
        nom = request.form["nom"]
        prenom = request.form["prenom"]
        mail = request.form["mail"]
        login = request.form["login"]
        statut = session["statut"] 
        avatar = request.form["avatar"] 

        ancien_mdp = request.form["ancien_mdp"]
        nouveau_mdp = request.form["nouveau_mdp"] 

        msg_auth, user = bdd.verifAuthData(login, ancien_mdp)

        if msg_auth == "authOK":

            h = hashlib.sha256()
            h.update(nouveau_mdp.encode("utf-8")) 
            mdp_hash = h.hexdigest()

            msg = bdd.update_membreData(id, nom, prenom, mail, login, mdp_hash, statut, avatar)
        else: 
            msg = "Mauvais mot de passe"

        return redirect("/")

    else: 
        return redirect("/parametres")

# GROUPES

@app.route("/addGroupe", methods=['POST']) 
def addGroupe(): 

    nom = request.form['gp_name']
    color = request.form['color']

    msg, lastId = bdd.add_groupesData(nom, color)

    return redirect("/select_sat_add?gp_nom={}".format(nom))

# UTILE ?
@app.route("/add_assoGroupeSatellite", methods=['GET','POST'])
def add_assoGS():

    groupe_nom = request.form["groupe_nom"]
    msg, groupe = bdd.get_groupeIdWhere("nomGroupe='{}'".format(groupe_nom))
    
    satnames = (list(request.form.keys()))
    chaine = "" 
    for i in range(len(satnames)):
        if i != len(satnames)-1:
            chaine += "nomSatellite = '{}' OR ".format(satnames[i])
        else: 
            chaine += "nomSatellite = '{}' ".format(satnames[i])

    msg_sat, listeSats = bdd.get_satelliteIdWhere(chaine)

    msg_asso = bdd.add_assoGroupeSatellite(groupe["idGroupe"], listeSats)

    return redirect("/admin?page=1&search=none")

@app.route("/deleteAllGroups")
def del_all_gp(): 

    msg = bdd.del_allGroupesData()

    return redirect("/admin?page=1&search=none")

@app.route("/deleteAsso", methods=['POST'])
def del_asso():

    idgroupe = request.form["deleteRowId"]
    msg = bdd.del_assoGroupeSatellite(idgroupe)
    
    if msg == "suppAssoOK":
        msg_del_gp = bdd.del_groupesData(idgroupe)

    return redirect("/admin?page=1&search=none")

@app.route("/detailAsso", methods=['POST'])
def get_details(): 

    groupe_id = request.form["getDetRow"]
    msg_gp, groupe_name = bdd.get_groupesDataWhere("idGroupe={}".format(groupe_id))

    validity = []

    msg_sat_id, listeIdSat = bdd.get_assoGroupeSatelliteWhere(groupe_id)
    if msg_sat_id == "OKSatWhereGroupe":

        chaine = "" 
        for i in range(len(listeIdSat)):
            if i != len(listeIdSat)-1:
                chaine += "idSatellite = '{}' OR ".format(listeIdSat[i]["idSatellite"])
            else: 
                chaine += "idSatellite = '{}' ".format(listeIdSat[i]["idSatellite"])

        msg_sat_data, listeSat = bdd.get_SatelliteDataWhere(chaine)

        for sat in listeSat: 
            validity.append(f.get_ageTLE(sat["tle"]))

        return render_template("/details.html", listeSat = listeSat, validity=validity, info=groupe_name[0]["nomGroupe"])
    
    else: 
        return redirect("/admin?page=1&search=none")