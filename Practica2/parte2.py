#CALDERON SABBAGH JUAN ALBERTO
#5BV1
#INTELIGENCIA ARTIFICIAL
#10/10/2023
#EN ESTE PROGRAMA SE REALIZARAN TAREAS SIMPLES PARA EL ANALISIS DE UN TEXTO, SE OBTENDRAN LOS TOKENS DE CADA TEXTO Y COMPARAREMOS LOS RESULTADOS ANTES Y DESPUES DE NORMALIZAR
import math
import pandas as pd
import spacy
from nltk.stem import SnowballStemmer
pd.set_option('display.max_columns', None,'display.width',None)

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
    nuevoStr = ' '.join(map(str, nuevosTookens))
    return nuevoStr
#Esta funcion sirve para quitar los espacios en blanco y signos de puntuacion de la lista de tokens
#TAMBIEN FORMA PARTE DEL PROCESO DE NORMALIZACION
'''def quitarCaracteresEspeciales(lista):
    #SI ALGUN TOKEN DENTRO DE LA LISTA FORMA PARTE DE LA LISTA DE SIMBOLOS ESPECIALES QUE DEFINIMOS ENTONCES NO SE METEN DENTRO DE LA NUEVA LISTA, DE ESTA MANERA MANTENEMOS SOLO LOS TOKENS IMPORTANTES
    signos = [".","-", ",", "(", ")", " ", "'", ' ', '‘', '’', '…', '\n', '“', '.','”',':','—']
    nuevosTokens = []
    #quitando espacios en blanco y signos
    for i in lista:
        if (i not in signos) and ("’" not in i) :
            nuevosTokens.append(i)
    #AL FINAL JUNTAMOS TODOS LOS TOKENS DE LA LISTA DENTRO DE UN STRING PARA USARLO ESTE EN LOS OTROS PROCESOS DE LA NORMALIZACION
    nuevoStr =' '.join(map(str,nuevosTokens))
    return nuevoStr'''
#ESTA FUNCION REMUEVE LAS STOPWORDS, COMPRUEBA QUE NO SEA UNA STOPWORD Y SE VAN JUNTANDO EN UN STRING
def removerStopWords(doc):
    tokensSS = []
    for token in doc:
        if not token.is_stop:
            tokensSS.append(token.text)
    return tokensSS
#SE OBTIENE EL LEMA DE CADA TOKEN Y SE VAN A METIENDO A UNA NUEVA LISTA
def lematizar(doc):
    tokensNuevos = []
    for token in doc:
        tokensNuevos.append(token.lemma_)
    return tokensNuevos
#FUNCION PARA REALIZAR STEMMING, SE LE HACE STEMMING A CADA TOKEN Y SE VAN METIENDO A NUEVA LISTA
def stemming(doc):
    tokensNuevos = []
    stemmer = SnowballStemmer("spanish")
    for token in doc:
        tokensNuevos.append(stemmer.stem(token))
    return tokensNuevos
#LO MISMO PERO PARA EL DE INGLES
def stemmingIng(doc):
    tokensNuevos = []
    stemmer = SnowballStemmer("english")
    for token in doc:
        tokensNuevos.append(stemmer.stem(token))
    nuevoStr = ' '.join(map(str, tokensNuevos))
    return nuevoStr
#FUNCION PARA HACER POSTAGGING DONDE SE MANTENDRAN LOS TOKENS QUE TENGAN UNA ETIQUETA DE MAYOR RELEVANCIA
def posTag(doc):
    etiquetasAMantener = ['NOUN', 'VERB','ADJ','ADV','ADP']
    nuevosTokens = []
    for token in doc:
        if token.pos_ in etiquetasAMantener:
            nuevosTokens.append(token)
    return nuevosTokens

#SE JUNTAN TODOS LOS PROCESOS DE LA NORMALIZACION Y RECORRIENDO LA MATRIZ DONDE ESTAN NUESTROS DOCUMENTOS SE VA NORMALIZANDO CADA UNO
def normalizacion(corpus):
    nuevoCorpus = []
    for doc in corpus:
        normalizado = obtenerTokens(nlpEn(doc))
        normalizado = nlpEn(pasarAminusculas(normalizado))
        #normalizado = nlpEn(quitarCaracteresEspeciales(normalizado))
        normalizado = removerStopWords(normalizado)
        normalizado = nlpEn(stemmingIng(normalizado))
        normalizado = posTag(normalizado)
        normalizado = lematizar(normalizado)
        nuevoCorpus.append(normalizado)
    print(nuevoCorpus)
    return nuevoCorpus

#FUNCION PARA CREAR EL DICCIONARIO DE TERMINOS UNICOS DE TODO EL CORPUS
def generarDiccionario(corpus):
    diccionario = []
    for doc in corpus:
        for palabra in doc:
            if palabra not in diccionario:
                diccionario.append(palabra)
    print(diccionario)
    return diccionario

#FUNCION PARA HACER EL ONE-HOT ENCODING, SE VA RECORRIENDO CADA VECTOR Y LUEGO CADA PALABRA DEL DICCIONARIO, SI LA PALABRA ESTA EN DOCUMENTO ENTONCES SE LE PONE UN 1
def oneHotEncoding(diccionario, corpus):
    oneHot = []
    for doc in corpus:
        vector = []
        for palabra in diccionario:
            if palabra in doc:
                vector.append(1)
            else:
                vector.append(0)
        oneHot.append(vector)
    df = pd.DataFrame(oneHot,columns=diccionario,index=['doc 1','doc 2','doc 3'])
    print("\nOne-Hot encoding")
    print(df)
    return oneHot

#PARECIDO A ONE-HOT PERO SE CUENTAN CUANTAS VECES APARECE ESE TERMINO EN EL DOCUMENTO
def termCount(diccionario,corpus):
    termCountArr = []
    for doc in corpus:
        vector = []
        for palabra in diccionario:
            if palabra in doc:
                vector.append(doc.count(palabra))
            else:
                vector.append(0)
        termCountArr.append(vector)
    df = pd.DataFrame(termCountArr, columns=diccionario, index=['doc 1', 'doc 2', 'doc 3'])
    print("\nTerm Count")
    print(df)
    return termCountArr

#SE SACA LA PROBABILIDAD DE TERMINO PRIMERO VIENDO LA CANTIDAD TOTAL DE TERMINOS EN EL CORPUS Y LUEGO SE RECORRE CADA PALABRA DEL DICCIONARIO Y SE VA CONTANDO LA CANTIDAD DE VECES QUE APARECE EN CADA DOCUMENTO
def termProb(diccionario,corpus):
    totalTerms = 0
    tparr = []
    vector = []
    for doc in corpus:
        totalTerms = totalTerms+len(doc)
    for palabra in diccionario:
        count = 0
        for doc in corpus:
            if palabra in doc:
                count = count+doc.count(palabra)
        vector.append(count/totalTerms)
    tparr.append(vector)
    df = pd.DataFrame(tparr, columns=diccionario, index=['Term Prob'])
    print('\nTerm Probability')
    print(df)
    return vector

#EN TERM FREQUENCY SE HACE ALGO PARECIDO A TERMCOUNT PERO ESTA VEZ SE DIVIDE LA CANTIDAD DE VECES QUE APARECE EL TERMINO ENTRE EL TOTAL DE TERMINOS DEL DOCUMENTO
def termFrequency(diccionario,corpus):
    termFrecArr = []
    for doc in corpus:
        vector = []
        for palabra in diccionario:
            if palabra in doc:
                vector.append(doc.count(palabra)/len(doc))
            else:
                vector.append(0)
        termFrecArr.append(vector)
    df = pd.DataFrame(termFrecArr, columns=diccionario, index=['doc 1', 'doc 2', 'doc 3'])
    print("\nTerm Frequency")
    print(df)
    return termFrecArr

#PARA IDF SE VE CUANTAS VECES APARECE CADA TERMINO EN LOS DOCUMENTOS, LUEGO SE APLICA LA FORMULA DEL IDF QUE ES LOG(CANTIDAD DE TERMINOS EN EL CORPUS/CANTIDAD DE VECES QUE SE HAYO CIERTO TERMINO)
def idf(diccionario,corpus):
    idfArr = []
    vector = []
    for palabra in diccionario:
        count = 0
        for doc in corpus:
            if palabra in doc:
                count = count+1
        vector.append(math.log10(((len(corpus)/count)+1)))
    idfArr.append(vector)
    df = pd.DataFrame(idfArr, columns=diccionario,index=['IDF'])
    print('\nIDF')
    print(df)
    return idfArr

#FINALMENTE PARA TF-IDF SE VA RECORRIENDO LA MATRIZ DE TERM FREQUENCY Y SE MULTIPLICA POR SU RESPECTIVO IDF
def tfidf(diccionario,tf,idf):
    tfidfArr = []
    for i in range(len(tf)):
        vector = []
        for j in range(len(tf[0])):
            vector.append(tf[i][j]*idf[0][j])
        tfidfArr.append(vector)
    df = pd.DataFrame(tfidfArr, columns=diccionario, index=['doc 1', 'doc 2', 'doc 3'])
    print("\nTerm Frequency")
    print(df)
    return tfidfArr

#SE CARGA EL MODULO DE SPACY EN INGLES
nlpEn = spacy.load('en_core_web_md')
#SE CREA EL CORPUS
corpus = ["Pancreatic cancer with metastasis. Jaundice with  transaminitis, evaluate for obstruction process.",
          "Pancreatitis. Breast cancer. No output from enteric  tube. Assess tube.",
          'Metastasis pancreatic cancer. Acute renal failure,  evaluate for hydronephrosis or obstructive uropathy.']
#SE NORMALIZA EL CORPUS
corpusNorm = normalizacion(corpus)
#SE CREA EL DICCIONARIO
diccionario = generarDiccionario(corpusNorm)
#SE REALIZAN TODAS LAS VECTORIZACIONES DE ACUERDA A LAS DIVERSAS TECNICAS VISTAS EN CLASE
oneHotEncoding(diccionario,corpusNorm)
termCount(diccionario,corpusNorm)
termProb(diccionario,corpusNorm)
tf = termFrequency(diccionario,corpusNorm)
iDF = idf(diccionario,corpusNorm)
tfidf(diccionario,tf,iDF)

