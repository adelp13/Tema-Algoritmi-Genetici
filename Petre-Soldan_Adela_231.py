import math

# citim datele de intrare
with open("Evolutie.in", "r") as file:
    nrCromozomi = int(file.readline().strip())
    capatStanga, capatDreapta = [int(x) for x in file.readline().strip().split()]
    a, b, c = [int(x) for x in file.readline().strip().split()]
    precizie = int(file.readline().strip())
    probRecombinare = int(file.readline().strip())
    probMutatie = int(file.readline().strip())
    nrEtape = int(file.readline().strip())

functie = lambda x: (a * x * x) + b * x + c # functie lambda pentru  functia care trebuie maximizata

class Cromozom:
    lungimeCromozom = math.ceil(math.log2((capatDreapta - capatStanga) * (10**precizie)))
    def __init__(self, binar, x, f, indice):
        self.binar = binar  # reprezentarea binara a unui cromozom
        self.x = x  # valoarea cromozomului cuprinsa intre a si b
        self.f = f
        self.indice = indice
