import nltk
from nltk.corpus import stopwords

# Baixar as stopwords
nltk.download('stopwords')

# Salvar as stopwords em arquivos de texto
languages = ['portuguese', 'english']
for lang in languages:
    stop_words = set(stopwords.words(lang))
    with open(f'stopwords_{lang}.txt', 'w', encoding='utf-8') as f:
        for word in stop_words:
            f.write(word + '\n')