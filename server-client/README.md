# User script

>Moodul, mis impleminteerib lihtsa server-kliendi ning mis suudab vastu võtta mitu klienti

Suhtlus toimub http päringute kaudu.


# Kasutus
CLI rakendus nõuab ainult 2 parameetrit:
1. Serveri port
2. Kasutaja nimi

Ükskord rakendus on käivitatud CLI's näitab menüü, millega saab valida erinevaid tegusid mille teostada.

Saab kutsuda välja inviduaalselt

Näide:
```bash
python user.py 5000 user1
```

Demoks on abiks fail ini.py, mida saab välja kutsuda käsurealt:
```bash
 python ini.py
```

Nimele ei ole piiranguid, aga porti ei tohi olla reserveeritud.


## Kasutamis näited erinevates terminali akendes

Terminal 1:
```bash
python user.py 5000 user1
```

Terminal 2:
```bash
python user.py 6000 user2
```

Eelmise 2 koodi readega saavad kaks kasutajat rääkida omavahel. Sa saad veel \
lisada kolmanda kasutaja.

Terminal 3:
```bash
python user.py 7000 user3
```

## Tehtud sammud
- [x] Server kliendi kasutaja mitme erineva ühendusega
- [x] Ühendus mitmele ip aadresile(klient)
- [x] Automaatne ühendamine uutesse ip aadresitesse, mis ühendavad user serverisse (client)
- [x] Saab küsida uute klientide aadresseid
- [x] Errorite käsitlemine


## GET requests:
```ip:port/addr```

Teeb päringut küsides mis aktiivsed sõlmed kellega antud ip:port kasutaja on ühendatud. Kui kasutaja teeb seda päringut siis vastu saades lisab automaatselt oma nimekirja ja püüab nendega ühendust saada.
    
```ip:port/getblocks```
        
Teeb päringut küsides ip:port kasutaja kõik blockid.

```ip:port/getblocks/H```

Teeb päringut küsides ip:port kasutaja alates antud hashi "H".

```ip:port/getdata/H```
        
Teeb päringut küsides ip:port kasutaja antud hashi "H" blocki sisut.


## POST requests:
```ip:port/addips```

Selle päringu sisu peab olema ip addresside nimekiri eraldatud \n märkiga. Võiks olla vastus ip:port/addr GET päringule.

```ip:port/addblocks```

Selle päringu sisu peab olema blockide hashide nimekiri eraldatud \n märkiga. Võiks olla vastus ip:port/getblocks GET päringule.

```ip:port/message```

Selle päringu sisu on misiganes sõnum tahab saada antud sõlmele


## Autorid: 
### Fred Oja, Javier Ortín, Artur Kerb