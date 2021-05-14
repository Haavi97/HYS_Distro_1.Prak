import os
import sys

sys.path.insert(1, os.pardir + os.sep + "kaevandamine")
from kaevama import sha256_str


class MerklePuu():
    def __init__(self, hash=None, vasak=None, parem=None):
        self.vasak = vasak
        self.parem = parem
        self.hash = self.arvuta_hash() if self.vasak != None and self.parem != None else hash

    def get_hash(self):
        return self.hash

    def get_vasak(self):
        return self.vasak

    def get_parem(self):
        return self.parem

    def set_vasak(self, vasak):
        self.vasak = vasak

    def set_parem(self, parem):
        self.parem = parem

    def set_hash(self, hash):
        self.hash = hash

    def arvuta_hash(self):
        self.hash = sha256_str(self.vasak + self.parem)
        return self.hash

    def ehita_nimekirjast(self, nimekiri, juba_hash=False):
        '''
        Antud transaktsioonide nimekiri peab hashima
        '''
        pikkus = len(nimekiri)
        assert pikkus > 0
        
        if pikkus == 1:
            to_hash = nimekiri[0] if juba_hash else sha256_str(str(nimekiri[0]))
            self.hash = to_hash
            return self.hash
        else:
            if pikkus%2 == 1:
                nimekiri.append(nimekiri[-1])
            uus_nimekiri = []
            for i in range(int(len(nimekiri)/2)):
                praegune = MerklePuu(vasak=sha256_str(nimekiri[i]), parem=sha256_str(nimekiri[i+1]))
                uus_nimekiri.append(praegune.arvuta_hash())
            return self.ehita_nimekirjast(uus_nimekiri, juba_hash=True)
        
            

