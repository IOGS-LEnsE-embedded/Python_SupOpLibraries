# Convertit un nombre a en une chaîne de bits d'une longueur l
# Remarque : un entier est codé sur 32 bits sur ces machines

def to_bitstring(a,l):
    b=bin(a)[2:]
    padding=l-len(b)
    b='0'*padding+b

    return b

# Convertit une chaîne de bits en un tableau d'octets représentant le nombre associé à cette chaîne
# Remarque : la convention 'big endian' est utilisée i.e. l'octet le plus significatif (MSB) est au début du tableau

def bits_to_bytes(a):
    bytelist=[]
    if len(a)%8!=0:
        padding=8-len(a)%8
        a='0'*padding+a
    for i in range(len(a)//8):
        bytelist.append(int(a[8*i:8*(i+1)],2))

    bytelist.reverse()

    return bytelist
