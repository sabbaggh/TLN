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

texto = leerArchivo("peliculas.txt")
comprobar(anios,texto)