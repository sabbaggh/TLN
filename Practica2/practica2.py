import re

#expresion regular para punto 1
rg = re.compile('r.*g')
#expresion regular para punto 2
costo = re.compile('[1-9]\d\d[.]\d\d')
#expresion regular para punto 3

#expresion regular para punro 4
anumero = re.compile('.*:.*:.*:.*[\d]+a|a+[\d]')
#expresion regular para punto 5
di = re.compile('d.*i')
#espresion regular para punto 6
anios = re.compile('[(][0-1][0-9][0-9][0-9][)]|[(][2][0][0][0-1][)]')
#expresion regular para punto 7
chocho = re.compile('[cC][hH][oO][cC][oO][lL][aA][tT][eE]')
#\b(?![cC][hH][oO][cC][oO][lL][aA][tT][eE]\b)\w+
#expresion regular para punto 8
poblaciones = re.compile('[0-9][0-9][0-9][0-9][0-9][0-9]')
#expresion regular para punto 9 inciso a
cerosA = re.compile(':0')
#expresion regular para punto 9 inciso b
cerosB = re.compile(':0{4}')
cerosB2 = re.compile('(:0([0-9]|[a-z]))')


def leerArchivo(name):
    lineas = []
    with open(name) as archivo:
        for linea in archivo:
            lineas.append(linea.strip())
    return lineas
def comprobar(expresion,texto):
    count = 0
    for linea in texto:
        if expresion.search(linea):
            print(linea)
            count=count+1
    print(f'Se encontraron {count} lineas que coinciden')

def encontrarRecSinChoco(expresion,texto):
    for linea in texto:
        if not expresion.search(linea):
            print(linea)
def ponerComasEntreNums(expresion,texto):
    lineas = []
    for linea in texto:
        x = (re.findall(expresion,linea))
        nuevaLinea = linea
        #print(x)
        for numero in x:
            nuevaLinea = re.sub(numero,numero[:3]+','+numero[3:]+',',nuevaLinea)
        lineas.append(nuevaLinea)
        print(nuevaLinea)
    return lineas

def quitarCerosIPS(expresion,texto):
    for linea in texto:
        while re.search(expresion,linea) is not None:
            linea = re.sub(expresion,":",linea)
        print(linea)

def quitarCerosInicio(expresion,texto):
    nuevo = []
    for linea in texto:
        while re.search(expresion,linea) is not None:
            linea = re.sub(expresion, ":0", linea)
        nuevo.append(linea)
        print(linea)
    for linea in nuevo:
        x = (re.findall(cerosB2, linea))
        print(x)
        for nuevo in x:
            linea = re.sub(cerosB2,':'+nuevo[1],linea)
            print(linea)



texto = leerArchivo("peliculas.txt")
texto2 = leerArchivo("recetas.txt")
texto3 = leerArchivo("poblaciones.txt")
texto4 = leerArchivo("ips.txt")
comprobar(anios,texto)
print('Recetas que no contienen chocolate')
encontrarRecSinChoco(chocho,texto2)
print()
ponerComasEntreNums(poblaciones,texto3)
print()
quitarCerosInicio(cerosB,texto4)