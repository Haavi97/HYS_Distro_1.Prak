import os
import sys

sys.path.insert(1, os.pardir + os.sep + "kaevandamine")
from kaevandamine import sha256_str


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

    def ehita_nimekirjast(self, nimekiri):
        pikkus = len(nimekiri)
        assert pikkus > 0

        if pikkus == 1:
            self.hash = MerklePuu(hash=nimekiri[0])
        elif pikkus == 2:
            self.hash = MerklePuu(vasak=nimekiri[0], parem=nimekiri[1])
        elif pikkus == 3:
            self.vasak = MerklePuu(vasak=nimekiri[0], parem=nimekiri[1])
            self.parem = MerklePuu(vasak=nimekiri[2], parem=nimekiri[2])
            self.arvuta_hash()
        elif pikkus == 4:
            self.vasak = MerklePuu(vasak=nimekiri[0], parem=nimekiri[1])
            self.parem = MerklePuu(vasak=nimekiri[2], parem=nimekiri[3])
            self.arvuta_hash()
        elif pikkus == 5:
            self.vasak = MerklePuu()
            self.parem = MerklePuu()
            self.vasak.ehita_nimekirjast(nimekiri[:3])
            self.parem.ehita_nimekirjast(nimekiri[4]*4)
            self.arvuta_hash()
        else:
            self.vasak = MerklePuu()
            self.parem = MerklePuu()
            self.vasak.ehita_nimekirjast(nimekiri[:3])
            self.parem.ehita_nimekirjast(nimekiri[4]*4)
            self.arvuta_hash()
            

