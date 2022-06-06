ENV = "development"
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 0

#vider le cache
SECRET_KEY="maCleSuperSecurisee"

#Configuration du serveur web
WEB_SERVER = {
    "host": "localhost",
    "port":8080,
    }

#Configuration du serveur de BDD
DB_SERVER = {
    "user": "admin",
    "password": "password",
    "host": "localhost",
    "port": 3306, #8889 si MAC
    "database": "beweb", #nom de la BDD
    "raise_on_warnings": True
    }

URL_PATHS = {
    "starlink" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=starlink&FORMAT=tle",
    "gnss" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=gnss&FORMAT=tle", 
    "meteosat" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=weather&FORMAT=tle",
    "earth_ressources": "https://celestrak.com/NORAD/elements/gp.php?GROUP=resource&FORMAT=tle", 
    "geosync" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=geo&FORMAT=tle", 
    "satnogs" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=satnogs&FORMAT=tle", 
    "sbas" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=sbas&FORMAT=tle", 
    "navynss" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=nnss&FORMAT=tle", 
    "russian_loe" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=musson&FORMAT=tle", 
    "space_earth_science" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=science&FORMAT=tle", 
    "education" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=education&FORMAT=tle", 
    "miscellanious_military" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=military&FORMAT=tle",
    "cubesats" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=cubesat&FORMAT=tle", 
    "radar_calibration" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=radar&FORMAT=tle", 
    "gorizont" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=gorizont&FORMAT=tle", 
    "raduga" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=raduga&FORMAT=tle", 
    "molniya" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=molniya&FORMAT=tle", 
    "geo_protected_zone" : "https://celestrak.com/NORAD/elements/gp.php?SPECIAL=gpz&FORMAT=tle",
    "geo_protected_zone_plus" : "https://celestrak.com/NORAD/elements/gp.php?SPECIAL=gpz-plus&FORMAT=tle",
    "intelsat" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=intelsat&FORMAT=tle", 
    "ses" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=ses&FORMAT=tle", 
    "iridium" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=iridium&FORMAT=tle", 
    "iridium_next" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=iridium-NEXT&FORMAT=tle", 
    "oneweb" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=oneweb&FORMAT=tle",
    "global_star" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=globalstar&FORMAT=tle", 
    "orbcom" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=orbcomm&FORMAT=tle",
    "swarm" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=swarm&FORMAT=tle", 
    "amateur_radio" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=amateur&FORMAT=tle", 
    "exp_com" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=x-comm&FORMAT=tle", 
    "other_com" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=other-comm&FORMAT=tle", 
    "gps_op" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=gps-ops&FORMAT=tle", 
    "glonass_op" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=glo-ops&FORMAT=tle", 
    "galileo" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=galileo&FORMAT=tle", 
    "beidou" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=beidou&FORMAT=tle",
    "planet" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=planet&FORMAT=tle", 
    "spire" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=spire&FORMAT=tle", 
    "search_rescue" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=sarsat&FORMAT=tle", 
    "disaster_monitoring" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=dmc&FORMAT=tle", 
    "noaa" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=noaa&FORMAT=tle", 
    "goes" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=goes&FORMAT=tle", 
    "space_stations" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle", 
    "others" : "https://celestrak.com/NORAD/elements/gp.php?GROUP=other&FORMAT=tle"
}