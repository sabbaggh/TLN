import pandas as pd
import spacy
from spacy.lang.es.examples import sentences
import matplotlib.pyplot as plt

nlp = spacy.load("es_core_news_md")
#Se lee el documento
anexoA = "AnexoES.txt"

#Funcion para leer el archivo
def leerArchivo(nombreArchivo):
    with open(nombreArchivo, encoding='utf-8') as f:
        contenido = f.read()
    contenido.strip()
    return contenido

#funcion para obtener los tokens del texto
def obtenerTokens(texto):
    tokens = []
    for token in texto:
        tokens.append(token.text)
    return tokens

def pasarAminusculas(lista):
    nuevosTookens = []
    for palabra in lista:
        nuevosTookens.append(palabra.lower())
    return nuevosTookens
#Esta funcion sirve para quitar los espacios en blanco y signos de puntuacion de la lista de tokens
def quitaEspaciosySignos(lista):
    signos = [".", ",", "(", ")", " ", "'", ' ', '‘', '’', '…', '\n', '“', '.','”']
    # quitando espacios en blanco y signos
    for i in lista:
        if i in signos:
            lista.remove(i)
    for i in lista:
        if i in signos:
            lista.remove(i)
    for i in lista:
        if i in signos:
            lista.remove(i)
    nuevoStr =' '.join(map(str,lista))
    return nuevoStr

#Funcion para obtener los tokens unicos y meterlos a una lista
def obtenerTokensUnicos(lista):
    visto = []
    for token in lista:
        if token not in visto:
            visto.append(token)
    return visto

def obtenerFrecuenciadeToekens(listaUnicos, lista):
    frecuencia = []
    for i in range(len(listaUnicos)):
        cuenta = 0
        for j in range(len(lista)):
            if listaUnicos[i] == lista[j]:
                cuenta = cuenta+1
        frecuencia.append(cuenta)
    return frecuencia

#crear histograma
def crearHistograma(tokensUnicos,frecuencia):
    plt.bar(tokensUnicos, frecuencia)
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.title("Histograma de Frecuencia de Palabras")
    plt.xticks(rotation=90)  # Rotar las etiquetas del eje x para una mejor legibilidad
    plt.tight_layout()  # Ajustar el diseño del gráfico
    plt.show()

def obtenerTokensMasComunes(tokensUnicos,frecuencia):
    listaTokensMF = []
    listaMaximos = []
    cantidadMaximos =[]
    for i in range(30):
        maximo = 0
        index = 0
        for j in range(len(frecuencia)):
            if frecuencia[j] > maximo and j not in listaMaximos:
                maximo = frecuencia[j]
                index = j
        listaMaximos.append(index)
        cantidadMaximos.append(maximo)
    for maximos in listaMaximos:
        listaTokensMF.append(tokensUnicos[maximos])
    df = pd.DataFrame({
        'Tokens':listaTokensMF,
        'Cantidad':cantidadMaximos
    })
    return listaTokensMF,cantidadMaximos

def obtenerTokensMenosComunes(tokensUnicos,frecuencia,maximo):
    listaTokensMF = []
    listaMaximos = []
    cantidadMaximos =[]
    for i in range(10):
        maximoI = maximo
        index = 0
        for j in range(len(frecuencia)):
            if frecuencia[j] < maximoI and j not in listaMaximos:
                maximoI = frecuencia[j]
                index = j
        listaMaximos.append(index)
        cantidadMaximos.append(maximoI)
    for maximos in listaMaximos:
        listaTokensMF.append(tokensUnicos[maximos])
    df = pd.DataFrame({
        'Tokens':listaTokensMF,
        'Cantidad':cantidadMaximos
    })
    print(df)

def removerStopWords(doc):
    tokensSS = ""
        #[token.text for token in doc if not token.is_stop]
    for token in doc:
        if not token.is_stop:
            tokensSS = tokensSS + " " + token.text
    return tokensSS
def lematizar(doc):
    tokensNuevos = []
    for token in doc:
        tokensNuevos.append(token.lemma_)
    return tokensNuevos

def normalizacion(doc):
    normalizado = []
#Se lee el archivo, se quitan espacios en blanco
doc1 = leerArchivo(anexoA)
doc1N = doc1.strip()
doc1N = nlp(doc1N)


####Anexo A
#print(doc1N)
#Se obtienen los tokens del documento
tokensAnexoA = obtenerTokens(doc1N)
#Se quitan espacios en blanco y signos de puntuacion
#limpioA = quitaEspaciosySignos(tokensAnexoA)
#Se obtienen los textos unicos
tokensUnicosA = obtenerTokensUnicos(tokensAnexoA)
frecuenciaAnexoA = obtenerFrecuenciadeToekens(tokensUnicosA,tokensAnexoA)
tokensMin = pasarAminusculas(tokensAnexoA)
doc1N = nlp(quitaEspaciosySignos(tokensMin))
tokensSinSS = nlp(removerStopWords(doc1N))
tokensLemas = lematizar(tokensSinSS)
print(tokensLemas)


#print(limpioA)
print(f'El numero total de tokens para el Anexo A es {len(tokensAnexoA)}')
#print(tokensUnicosA)
print(f'El numero total de tokens unicos para el Anexo A es {len(tokensUnicosA)}')
#print(frecuenciaAnexoA)
print("Lista 10 tokens mas comunes")
tokensMC,frecMC = obtenerTokensMasComunes(tokensUnicosA,frecuenciaAnexoA)
print("Lista 10 tokens menos comunes")
obtenerTokensMenosComunes(tokensUnicosA,frecuenciaAnexoA,max(frecuenciaAnexoA))
#xddd
#print(tokensLemas)
crearHistograma(tokensUnicosA,frecuenciaAnexoA)




###############