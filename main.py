import spacy
import pathlib as pt
from spacy import displacy
from spacy.lang.es.stop_words import STOP_WORDS


archivo = "AnexoA.txt"
nlp = spacy.load("es_core_news_sm")
documento = nlp(pt.Path(archivo).read_text(encoding='utf-8'))
print([token.text for token in documento])


