from time import sleep, time
from hashlib import sha256

def sha256_str(tekst):
    return sha256(tekst.encode('utf-8')).hexdigest()

def kaeva_naivselt(transaktsioon, hash, n=4, t=5):
    '''
    Parameetrid:
    hash : string
        antud transaktsiooni eelmine hash
    transaktsioon : string
        transaktsiooni sisu
    n : int
        nonce suurus
    t : int
        minimum sekundit mis kaevandamine peaks võtma
    '''
    MAX_NONCE = 10**100
    prefiks_nullid = '0'*n
    algus = time()
    hetkel = time()
    praegune  = ''
    nonce = 0
    while not praegune.startswith(prefiks_nullid) and nonce < MAX_NONCE:
        praegune = sha256_str(transaktsioon + hash + str(nonce))
        nonce += 1
        hetkel = time()
    try:
        sleep(t - (hetkel - algus))
    except ValueError:
        # See tähendab, et antud aeg on juba mööda läinud
        pass
    print('Kaevandamine aeg: {:.2f} s'.format(time() - algus))
    print('Tegelik kaevandamine aeg: {:.2f} s'.format(hetkel - algus))
    print('Nonce: {}'.format(nonce))
    print('Hash: {}'.format(praegune))
    return hash

if __name__ == '__main__':
    l2pp = False
    while not l2pp:
        if input('\n\nKirjuta 0 lõpetamiseks. Muu jätkamiseks: ') == '0':
            l2pp = True
            break
        in_hash = input('Eelmise transaktsiooni hash: ')
        transaktsioon = input('Transaktsiooni sisu: ')
        n = int(input('Nullid: '))
        t = int(input('Aeg: '))
        kaeva_naivselt(transaktsioon, in_hash, n, t)