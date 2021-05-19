from time import sleep, time
from hashlib import sha256


def sha256_str(tekst):
    '''Muudab hashi hex digest'iks nii, et saaks seda lugeda. 

    Ja kasutada tekstina järgmise hashimiseks.'''
    return sha256(str(tekst).encode('utf-8')).hexdigest()


def kaeva_naivselt(transaktsioon, last_hash, n=4, t=5):
    '''
    Parameetrid:
    hash : string
        antud transaktsiooni eelmine hash
    transaktsioon : string
        transaktsiooni sisu
    n : int
        mitu nullidega peab hash alustama.
        Default on 4. 7 juba võtab kaua aega
    t : int
        minimum sekundit mis kaevandamine peaks võtma
    '''
    # MAX nonce igaks juhuks, kuigi see võtaks mitu tundi
    MAX_NONCE = 10**100

    prefiks_nullid = '0'*n
    algus = time()
    hetkel = time()
    praegune = ''
    nonce = -1
    while not praegune.startswith(prefiks_nullid) and nonce < MAX_NONCE:
        nonce += 1
        praegune = sha256_str(transaktsioon + last_hash + str(nonce))
        hetkel = time()
    try:
        # Praksi kirjelduses on mõni minimum aeg mis vähemalt peab kaevandama
        # Nii et see ootab kui on varem kaevandamist lõpetanud
        sleep(t - (hetkel - algus))
    except ValueError:
        # See tähendab, et antud aeg on juba mööda läinud
        pass
    print('Kaevandamine aeg: {:.2f} s'.format(time() - algus))
    print('Tegelik kaevandamine aeg: {:.2f} s'.format(hetkel - algus))
    print('Nonce: {}'.format(nonce))
    print('Hash: {}'.format(praegune))
    return praegune


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
