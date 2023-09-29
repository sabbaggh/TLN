import pandas as pd
import spacy
from spacy.lang.es.examples import sentences
import matplotlib.pyplot as plt
import nltk
from nltk.stem.porter import *
from nltk.stem import SnowballStemmer

#Funcion para leer el archivo
def leerArchivo(nombreArchivo):
    #SE LEE EL ARCHIVO Y SE REGRESA
    with open(nombreArchivo, encoding='utf-8') as f:
        contenido = f.read()
    contenido.strip()
    return contenido

#funcion para obtener los tokens del texto
def obtenerTokens(texto):
    #SE CONSIGUEN LOS TOKENS DENTRO DEL DOCUMENTO Y SE VAN METIENDO DENTRO DE UNA LISTA
    tokens = []
    for token in texto:
        tokens.append(token.text)
    return tokens

#FUNCION PARA PASAR LOS TOKENS A MINUSCULAS
#ESTA FUNCION FORMA PARTE  DEL PROCESO DE NORMALIZACION
def pasarAminusculas(lista):
    #SE RECORRE UNA LISTA DE TOKENS Y SE VA PASANDO CADA UNO A MINUSCULAS
    nuevosTookens = []
    for palabra in lista:
        nuevosTookens.append(palabra.lower())
    return nuevosTookens
#Esta funcion sirve para quitar los espacios en blanco y signos de puntuacion de la lista de tokens
#TAMBIEN FORMA PARTE DEL PROCESO DE NORMALIZACION
def quitarCaracteresEspeciales(lista):
    #SI ALGUN TOKEN DENTRO DE LA LISTA FORMA PARTE DE LA LISTA DE SIMBOLOS ESPECIALES QUE DEFINIMOS ENTONCES NO SE METEN DENTRO DE LA NUEVA LISTA, DE ESTA MANERA MANTENEMOS SOLO LOS TOKENS IMPORTANTES
    signos = [".","-", ",", "(", ")", " ", "'", ' ', '‘', '’', '…', '\n', '“', '.','”',':','—']
    nuevosTokens = []
    #quitando espacios en blanco y signos
    for i in lista:
        if (i not in signos) and ("’" not in i) :
            nuevosTokens.append(i)
    #AL FINAL JUNTAMOS TODOS LOS TOKENS DE LA LISTA DENTRO DE UN STRING PARA USARLO ESTE EN LOS OTROS PROCESOS DE LA NORMALIZACION
    nuevoStr =' '.join(map(str,nuevosTokens))
    return nuevoStr

#Funcion para obtener los tokens unicos y meterlos a una lista
def obtenerTokensUnicos(lista):
    visto = []
    for token in lista:
        if token not in visto:
            visto.append(token)
    return visto

#EN ESTA FUNCION OBTENEMOS LA FRECUENCIA DE APARICION DE LOS TOKENS Y SE METE SU FRECUENCIA DENTRO DE UNA LISTA, ESTO SERVIRA PARA CREAR LOS HIS
def obtenerFrecuenciadeToekens(listaUnicos, lista):
    frecuencia = []
    for i in range(len(listaUnicos)):
        cuenta = 0
        for j in range(len(lista)):
            if listaUnicos[i] == lista[j]:
                cuenta = cuenta+1
        frecuencia.append(cuenta)
    return frecuencia

#FUNCION PARA GENERAR LOS HISTOGRAMAS
def crearHistograma(tokensUnicos,frecuencia,titulo):
    plt.bar(tokensUnicos, frecuencia)
    plt.xlabel("Palabras")
    plt.ylabel("Frecuencia")
    plt.title(titulo)
    plt.xticks(rotation=90)  # Rotar las etiquetas del eje x para una mejor legibilidad
    plt.tight_layout()  # Ajustar el diseño del gráfico
    plt.show()

#EN ESTA FUNCION SE OBTIENEN LOS TOKENS MAS COMUNES Y SE METE LA FRECUENCIA DE CADA UNO DE ESTOS, ADEMAS SE IMPRIME UNA LISTA INDICANCO EL TOKEN Y SU FRECUENCIA DE APARICION, SE METEN EN UN DATAFRAME PARA FACILITAR EL PROCESO DE IMPRESION
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
    print(df)
    return listaTokensMF,cantidadMaximos

def obtenerTokensMenosComunes(tokensUnicos,frecuencia,maximo):
    listaTokensMF = []
    listaMaximos = []
    cantidadMaximos =[]
    for i in range(30):
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
    return listaTokensMF,cantidadMaximos

def removerStopWords(doc):
    tokensSS = ""
    for token in doc:
        if not token.is_stop:
            tokensSS = tokensSS + " " + token.text
    return tokensSS
def lematizar(doc):
    tokensNuevos = []
    for token in doc:
        tokensNuevos.append(token.lemma_)
    return tokensNuevos

def stemming(doc):
    tokensNuevos = []
    stemmer = SnowballStemmer("spanish")
    for token in doc:
        tokensNuevos.append(stemmer.stem(token))
    return tokensNuevos

def stemmingIng(doc):
    tokensNuevos = []
    stemmer = SnowballStemmer("english")
    for token in doc:
        tokensNuevos.append(stemmer.stem(token))
    return tokensNuevos

def posTag(doc):
    etiquetasAMantener = ['NOUN', 'VERB','ADJ']
    nuevosTokens = []
    for token in doc:
        if token.pos_ in etiquetasAMantener:
            nuevosTokens.append(token)
    return nuevosTokens


def normalizacionEsp(doc):
    normalizado = obtenerTokens(doc)
    normalizado = pasarAminusculas(normalizado)
    normalizado = nlp(quitarCaracteresEspeciales(normalizado))
    normalizado = posTag(normalizado)
    normalizado = nlp(removerStopWords(normalizado))
    normalizado = lematizar(normalizado)
    normalizado = stemming(normalizado)
    return normalizado

def normalizacionEng(doc):
    normalizado = obtenerTokens(doc)
    normalizado = pasarAminusculas(normalizado)
    normalizado = nlpEn(quitarCaracteresEspeciales(normalizado))
    print(normalizado)
    print()
    normalizado = posTag(normalizado)
    normalizado = nlpEn(removerStopWords(normalizado))
    normalizado = lematizar(normalizado)
    normalizado = stemmingIng(normalizado)
    return normalizado

####Anexo A
#SE CARGA EL MODULO DE SPACY PARA ESPANOL
nlp = spacy.load("es_core_news_md")
#Se lee el archivo
doc1 = leerArchivo("AnexoES.txt")
print(doc1)
doc1N = nlp(doc1)
#Se obtienen los tokens del documento
tokensAnexoA = obtenerTokens(doc1N)
#Se obtienen los tokens unicos
tokensUnicosA = obtenerTokensUnicos(tokensAnexoA)
frecuenciaAnexoA = obtenerFrecuenciadeToekens(tokensUnicosA,tokensAnexoA)
normalizado = normalizacionEsp(doc1N)
normalizado.pop(0)

######TOKENS ANTES DE NORMALIZAR
print(f'El numero total de tokens para el Anexo A es {len(tokensAnexoA)}')
print(f'El numero total de tokens unicos para el Anexo A es {len(tokensUnicosA)}')
print("Lista 10 tokens mas comunes antes de normalizar")
tokensMC,frecMC = obtenerTokensMasComunes(tokensUnicosA,frecuenciaAnexoA)
print("Lista 10 tokens menos comunes antes de normalizar")
obtenerTokensMenosComunes(tokensUnicosA,frecuenciaAnexoA,max(frecuenciaAnexoA))
crearHistograma(tokensUnicosA,frecuenciaAnexoA,'Tokens antes de normalizar')
crearHistograma(tokensMC,frecMC,'30 tokens mas comunes antes de normalizar')

######TOKENS DESPUES DE NORMALIZAR
print(f'El numero total de tokens para el Anexo A despues de normalizar es {len(normalizado)}')
print(normalizado)
tokensUnicosA = obtenerTokensUnicos(normalizado)
frecuenciaAnexoA = obtenerFrecuenciadeToekens(tokensUnicosA,normalizado)
print(f'El numero total de tokens unicos para el Anexo A despues de normalizar es {len(tokensUnicosA)}')
print(tokensUnicosA)
print("Lista 10 tokens mas comunes despues de normalizar")
tokensMC,frecMC = obtenerTokensMasComunes(tokensUnicosA,frecuenciaAnexoA)
print("Lista 10 tokens menos comunes despues de normalizar")
obtenerTokensMenosComunes(tokensUnicosA,frecuenciaAnexoA,max(frecuenciaAnexoA))
crearHistograma(tokensUnicosA,frecuenciaAnexoA,'Tokens despues de normalizar')
crearHistograma(tokensMC,frecMC,'30 tokens mas comunes despues de normalizar')


##################################################################

##ANEXO B
#SE CARGA EL MODULO DE SPACY PARA INGLES
nlpEn = spacy.load('en_core_web_md')
#SE LEE EL ARCHIVO
doc1 = leerArchivo("AnexoEn.txt")
doc1N = nlpEn(doc1)
tokensAnexoB = obtenerTokens(doc1N)
tokensUnicosB = obtenerTokensUnicos(tokensAnexoB)
frecuenciaAnexoB = obtenerFrecuenciadeToekens(tokensUnicosB,tokensAnexoB)
print(tokensUnicosB)
normalizado = normalizacionEng(doc1N)
######TOKENS ANTES DE NORMALIZAR
print(f'El numero total de tokens para el Anexo B es {len(tokensAnexoB)}')
print(f'El numero total de tokens unicos para el Anexo B es {len(tokensUnicosB)}')
print("Lista 10 tokens mas comunes antes de normalizar")
tokensMC,frecMC = obtenerTokensMasComunes(tokensUnicosB,frecuenciaAnexoB)
print("Lista 10 tokens menos comunes antes de normalizar")
obtenerTokensMenosComunes(tokensUnicosB,frecuenciaAnexoB,max(frecuenciaAnexoB))
crearHistograma(tokensUnicosB,frecuenciaAnexoB,'Tokens antes de normalizar')
crearHistograma(tokensMC,frecMC,'30 tokens mas comunes antes de normalizar')

######TOKENS DESPUES DE NORMALIZAR
print(f'El numero total de tokens para el Anexo A despues de normalizar es {len(normalizado)}')
print(normalizado)
tokensUnicosB = obtenerTokensUnicos(normalizado)
frecuenciaAnexoB = obtenerFrecuenciadeToekens(tokensUnicosB,normalizado)
print(f'El numero total de tokens unicos para el Anexo B despues de normalizar es {len(tokensUnicosB)}')
print(tokensUnicosB)
print("Lista 10 tokens mas comunes despues de normalizar")
tokensMC,frecMC = obtenerTokensMasComunes(tokensUnicosB,frecuenciaAnexoB)
print("Lista 10 tokens menos comunes despues de normalizar")
obtenerTokensMenosComunes(tokensUnicosB,frecuenciaAnexoB,max(frecuenciaAnexoB))
crearHistograma(tokensUnicosB,frecuenciaAnexoB,'Tokens despues de normalizar')
crearHistograma(tokensMC,frecMC,'30 tokens mas comunes despues de normalizar')