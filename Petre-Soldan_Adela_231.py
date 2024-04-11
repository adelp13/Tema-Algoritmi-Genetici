import math
import random

# citim datele de intrare
with open("Evolutie.in", "r") as file:
    nrCromozomi = int(file.readline().strip())
    capatStanga, capatDreapta = [int(x) for x in file.readline().strip().split()]
    if capatStanga > capatDreapta:
        capatDreapta, capatStanga = capatStanga, capatDreapta
    a, b, c = [int(x) for x in file.readline().strip().split()]
    precizie = int(file.readline().strip())
    probRecombinare = float(file.readline().strip())
    probMutatie = float(file.readline().strip())
    nrEtape = int(file.readline().strip())

functie = lambda x: (a * x * x) + b * x + c # functie lambda pentru  functia care trebuie maximizata
lungimeCromozom = math.ceil(math.log2((capatDreapta - capatStanga) * (10**precizie)))
tipMutatie = 1
numeFisierIesire = "Evolutie.out"
listaCromozomi = probabilitatiSelectie = intervaleSelectie = []

def initializareListaCromozomi():
    listaCromozomi = []  # aici vor fi retinuti cromozomii
    for i in range(nrCromozomi):
        binar = bin(random.randint(0, 2**lungimeCromozom))[2:]
        # adaugam zero-uri pana ajungem la lungimea necesara cromozomului
        lungimeDeAdaugat = lungimeCromozom - len(binar)
        binar = '0' * lungimeDeAdaugat + binar
        listaCromozomi.append(binar)
    return listaCromozomi
def binarToX(binar): # ia valoarea binara a unui  cromozom si afla x ul
    return capatStanga + int(binar, 2) * (capatDreapta - capatStanga) / 2**lungimeCromozom

def calculareMaximMedieFitnessEtapa():
    valoriFitness = [functie(binarToX(cromozom)) for cromozom in listaCromozomi] # o lista care are f ul pentru fiecare cromozom
    return max(valoriFitness), (sum(valoriFitness) / nrCromozomi)
def calculareProbabilitatiSelectie():
    performantaTotala = sum([functie(binarToX(cromozom)) for cromozom in listaCromozomi])  # performanta totala a populatiei
    return [(functie(binarToX(listaCromozomi[i])) / performantaTotala) for i in range(nrCromozomi)]

def calculareIntervaleProbabilitatiSelectie(): # intervalul de selectie i este suma probabilitatilor cromozomilor din intervalul [0, i]
    return [0] + ([sum(probabilitatiSelectie[:i+1]) if i != nrCromozomi - 1 else 1.0 for i in range(nrCromozomi)])

def cautareBinaraIndice(u):
    st, dr = 0, (nrCromozomi + 1) - 1
    indiceCautat = -1
    while st <= dr:
        mid = (st + dr) // 2
        if intervaleSelectie[mid] >= u:
            indiceCautat = mid
            dr = mid - 1
        else:
            st = mid + 1

    return indiceCautat - 1
def determinarePopulatieP1(): # prima populatie intermediara, dintre acestia vom alege cativa cromozomi
    listaU = [] # valoarea u generata random pentru determinarea noului cromozom de pe fiecare pozitie din lista
    indici = [] # retinem pozitiile trecute ale cromozomilor alesi pentru prima parte a selectiei, pentru a le afisa pentru prima etapa a algoritmului
    listaCromozomiP1 = [] # noua lista de cromozomi dupa selectia 1
    for i in range(nrCromozomi):
        # generam un u random intre [0, 1)
        u = random.uniform(0, 1)
        listaU.append(u)
        indice = cautareBinaraIndice(u) # folosim cautarea binara in lista de intervale de selectie pentru a gasi prima valoare >= u
        indici.append(indice + 1)
        listaCromozomiP1.append(listaCromozomi[indice]) # noul cromozom care va fi pe pozitia i in populatie
    return listaU, listaCromozomiP1, indici # lista de cromozomi va avea acum valorile pt populatia P1
def afisareListaCromozomi(f):
  for i in range(nrCromozomi):
        x = binarToX(listaCromozomi[i])
        f.write(f"{i + 1}: {listaCromozomi[i]} x= {x} f= {functie(x)}\n")

def determinareParticipantiLaIncrucisare():
    listaU = []
    listaIndiciRecombinare = [] # indicii din populatia P1 a cromozomilor care vor participa la incrucisare
    for i in range(nrCromozomi):
        u = random.uniform(0, 1)
        listaU.append(u)
        if u < probRecombinare:
            listaIndiciRecombinare.append(i + 1)

    return listaU, listaIndiciRecombinare

class Recombinare: # pentru a retine recombinarile facute pentru determinarea populatiei P2
    # si afisarea in fisier a informatiilor pt fiecare recombinare in cazul primei etape
    def __init__(self, indice1, indice2, cromozom1, cromozom2, punctTaietura, rezultat1, rezultat2):
        self.indice1 = indice1
        self.indice2 = indice2
        self.cromozom1 = cromozom1
        self.cromozom2 = cromozom2
        self.punctTaietura = punctTaietura
        self.rezultat1 = rezultat1
        self.rezultat2 = rezultat2

def recombinare(listaIndici):
    recombinari = []
    random.shuffle(listaIndici) # amestecam random indicii cromozomilor care vor fi recombinati

    for i in range(1, len(listaIndici), 2): # luam perechi consecutive de cromozomi din lista amestecata si ii recombinam
        cromozom1, cromozom2 = listaCromozomi[listaIndici[i - 1] - 1], listaCromozomi[listaIndici[i] - 1]
        punctTaietura = random.randint(0, lungimeCromozom) # daca e 0 cromozomii nu se modifica, daca e lungimea maxima cromozomii fac swap complet
        rezultat1, rezultat2 = cromozom2[:punctTaietura] + cromozom1[punctTaietura:], cromozom1[:punctTaietura] + cromozom2[punctTaietura:]

        recombinari.append(Recombinare(listaIndici[i - 1], listaIndici[i], cromozom1, cromozom2, punctTaietura, rezultat1, rezultat2))
        # modificam lista de cromozomi din populatia p1 ca sa cream p2:
        listaCromozomi[listaIndici[i - 1] - 1], listaCromozomi[listaIndici[i] - 1] = rezultat1, rezultat2

    return recombinari # returnez lista de cromozomi pt populatia p2 si recombinarile care au avut loc(lista de obiecte)

def mutatie(variantaMutatie):
    indiciMutatie = []
    if variantaMutatie == 0: # mutatie rara
        for i in range(nrCromozomi):
            u = random.uniform(0, 1)
            if u < probMutatie: # are loc mutatie
                pozitie = random.randint(0, lungimeCromozom - 1) # generam o pozitie din cromozom si calculam complementul
                listaCromozomi[i] = listaCromozomi[i][:pozitie] + str(1 - int(listaCromozomi[i][pozitie])) + listaCromozomi[i][pozitie + 1:]
                indiciMutatie.append(i + 1)
    else: #pentru fiecare cromozom luam fiecare bit si vedem daca il modificam
        for i in range(nrCromozomi):
            bitiSchimbati = 0 # cati biti dintr-un cromozom vor suferi mutatii
            for pozitie in range(lungimeCromozom):
                u = random.uniform(0, 1)
                if u < probMutatie:
                    listaCromozomi[i] = listaCromozomi[i][:pozitie] + str(1 - int(listaCromozomi[i][pozitie])) + listaCromozomi[i][pozitie + 1:]
                    bitiSchimbati += 1
            if bitiSchimbati:
                indiciMutatie.append(i + 1)
    return indiciMutatie

def calculareElementeElitiste(maximPopulatie):
    elementeElitiste, indiciElementeElitiste = [], []
    for i in range(nrCromozomi):
        if functie(binarToX(listaCromozomi[i])) == maximPopulatie: # daca fitness ul unui cromozom din lista e egal cu maximul, este element elitist
            elementeElitiste.append(listaCromozomi[i])
            indiciElementeElitiste.append(i + 1)

    return elementeElitiste, indiciElementeElitiste

def adaugareElementeElitiste(elementeElitiste, indiciElementeElitiste): # adaugam la populatia P + 1 elementele elitiste obtinute inainte de prelucrarea populatiei P
    for i in range(len(elementeElitiste)):
        listaCromozomi[indiciElementeElitiste[i] - 1] = elementeElitiste[i]

#DUPA CITIRE:
listaCromozomi = initializareListaCromozomi()
maximPopulatie, mediePopulatie = calculareMaximMedieFitnessEtapa() # pentru etapa 1, initiala

with open(numeFisierIesire, "w") as f:
    f.write("Populatia initiala\n")
    afisareListaCromozomi(f)

    elementeElitiste, indiciElementeElitiste = calculareElementeElitiste(maximPopulatie)
    f.write(f"\nElementele elitiste (cu fitness-ul maxim = {maximPopulatie}):\n")
    for i in range(len(elementeElitiste)):
        f.write(f"Cromozomul {indiciElementeElitiste[i]}: {elementeElitiste[i]}\n")

    probabilitatiSelectie = calculareProbabilitatiSelectie()
    f.write("\nProbabilitati selectie\n")
    for i in range(nrCromozomi):
        f.write(f"cromozom {i + 1} probabilitate {probabilitatiSelectie[i]}\n")

    intervaleSelectie = calculareIntervaleProbabilitatiSelectie()
    f.write("\nIntervale probabilitati selectie\n")
    for i in range(nrCromozomi + 1): # pentru n cromozomi avem n+1 intervale
        f.write(str(intervaleSelectie[i]) + "\n")

    listaU, listaCromozomi, indici = determinarePopulatieP1()
    for i in range(nrCromozomi):
        f.write(f"u = {listaU[i]} selectam cromozomul {indici[i]}\n")
    f.write("\nDupa selectie:\n")
    afisareListaCromozomi(f)

    f.write(f"\n\nProbabilitatea de incrucisare: {probRecombinare}\n")
    listaU, listaIndiciRecombinare = determinareParticipantiLaIncrucisare()
    for i in range(nrCromozomi):
        f.write(f"{i + 1}: {listaCromozomi[i]} u = {listaU[i]}")
        if listaU[i] < probRecombinare:
            f.write(f"<{probRecombinare} participa")
        f.write("\n")

    recombinari = recombinare(listaIndiciRecombinare) # are loc recombinarea in perechi a cromozomilor participanti
    for r in recombinari: # un obiect din clasa Recombinare
        f.write(f"\nRecombinare dintre cromozomul {r.indice1} cu cromozomul {r.indice2}:\n {r.cromozom1} {r.cromozom2} punct {r.punctTaietura}\n")
        f.write(f"Rezultat {r.rezultat1} {r.rezultat2}\n")
    f.write("\n\nDupa recombinare\n")
    afisareListaCromozomi(f)

    f.write(f"\nProbabilitate de mutatie pentru fiecare gena {probMutatie}\n")
    indiciMutatie = mutatie(tipMutatie) #parametrul functiei determina  tipul de mutatie
    if not len(indiciMutatie):
        f.write("Nu a fost modificat niciun cromozom\n")
    else:
        f.write(f"Au fost modificati cromozomii\n")
    for indice in indiciMutatie:
        f.write(str(indice) + "\n")
    f.write("Dupa mutatie:\n")
    afisareListaCromozomi(f) # am obtinut populatia pentru etapa 2

    adaugareElementeElitiste(elementeElitiste, indiciElementeElitiste)
    f.write("\nDupa adaugarea elementelor elitiste:\n")
    afisareListaCromozomi(f)  # am obtinut populatia pentru etapa 2 si i-am adaugat elementele elitiste din prima etapa



    #TRECEM LA POPULATIILE 2, 3, 4, .......
    #AFISAM DOAR MAX SI AVF DE F
    f.write(f"\n\nPopulatia 1: maximul = {maximPopulatie} media = {mediePopulatie}\n")

    for populatie in range(2, nrEtape + 1):
        maximPopulatie, mediePopulatie = calculareMaximMedieFitnessEtapa()
        f.write(f"Populatia {populatie}: maximul = {maximPopulatie} media = {mediePopulatie}\n")

        elementeElitiste, indiciElementeElitiste = calculareElementeElitiste(maximPopulatie)
        probabilitatiSelectie = calculareProbabilitatiSelectie()
        intervaleSelectie = calculareIntervaleProbabilitatiSelectie()
        listaU, listaCromozomi, indici = determinarePopulatieP1()
        listaU, listaIndiciRecombinare = determinareParticipantiLaIncrucisare()
        recombinari = recombinare(listaIndiciRecombinare)
        indiciMutatie = mutatie(tipMutatie)  # parametrul functiei determina  tipul de mutatie
        adaugareElementeElitiste(elementeElitiste, indiciElementeElitiste) # elementele elitiste vor avea aceleasi pozitii ca in etapa trecuta
