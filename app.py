# Análise Estastística de Dados Textuais - NLP - Streamlit
# Autor: Robson Ricardo 
# Para a disciplina de Tópicos em NLP, do curso de graduação em Ciência de Dados e Inteligência Artificial do IESB.

# Importando as bibliotecas necessárias
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from nltk import ngrams
from collections import Counter

# Nome do App
st.set_page_config(page_title='Análise Estatística de Dados Textuais', layout='wide')


# SIDEBAR

st.sidebar.title('Análise Estatística de Dados Textuais')
st.sidebar.caption('Idiomas suportados: Português e Inglês')

# Upload de arquivo de texto (PDF, DOCX)
file = st.sidebar.file_uploader('Selecione o arquivo que deseja analisar:', type=['pdf', 'docx'])

# Textbox para que o usuário insira o texto manualmente
text_disabled = file is not None # Desabilita o campo de texto se um arquivo for carregado
text = st.sidebar.text_area('Se preferir, insira o texto que deseja analisar:',  disabled=text_disabled, height=130)

if st.sidebar.button('Carregar texto',  disabled=text_disabled):
    if text == '':
        st.sidebar.write(f':red[Insira um texto válido!]')
    else:
        st.sidebar.write(f':green[Texto carregado com sucesso!]')

st.sidebar.divider()
st.sidebar.caption('🧑‍💻 Made by [**Robson Ricardo**](https://github.com/jobsrobson)')



# SEÇÃO PRINCIPAL

# Carregamento do Conteúdo do Arquivo (PDF ou DOCX)
if file is not None:
    if file.type == 'application/pdf':
        text = ''
        import pdfplumber
        with st.spinner('Carregando arquivo...'):
            pdf = pdfplumber.open(file)
            for page in pdf.pages:
                text += page.extract_text()
            pdf.close()

    elif file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        import docx2txt
        with st.spinner('Carregando arquivo...'):
            doc = docx2txt.process(file)
            text = ''
            for paragraph in doc:
                text += paragraph

# Exibe mensagem se não houver texto definido
if not text:
    st.write('##### 👈 Faça upload ou digite um texto para começar!')
    st.stop()

# Limpa o app se o texto for descarregado
if not text:
    st.stop()



# BACKEND ANÁLISE ESTATÍSTICA

# 1. Limpeza do Texto
def clean_text(text):
    text = text.lower() # Converte para minúsculas
    text = re.sub(r'\d+', '', text) # Remove números
    # Remove pontuação (exceto hífen quando entre letras)
    text = re.sub(r'[^\w\s-]', '', text)
    text = text.strip() # Remove espaços em branco
    return text

text_clean = clean_text(text)

# 2. Tokenização usando Expressões Regulares
def tokenize_text(text):
    tokens = re.findall(r'\b\w+\b', text)
    return tokens

tokens = tokenize_text(text_clean)

# 3. Remoção de Stopwords e Palavras com 2 ou menos caracteres
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        stop_words = set(f.read().splitlines())
    return stop_words

# Carregar stopwords em Português e Inglês
stop_words_portuguese = load_stopwords('data/stopwords_portuguese.txt')
stop_words_english = load_stopwords('data/stopwords_english.txt')
stop_words = stop_words_portuguese.union(stop_words_english)

tokens = [word for word in tokens if word not in stop_words and len(word) > 2]

# 4. Frequência de Palavras
freq_dist = FreqDist(tokens)

# 5. Bigramas
bigrams = list(ngrams(tokens, 2))
bigram_freq = Counter(bigrams)



# EXIBIÇÃO DOS RESULTADOS

st.write('### Resultado da Análise Estatística do Texto')

with st.container():
    col1, col2, col3, col4 = st.columns(4, border=True, vertical_alignment="center")
    col1.metric("Palavras", len(text.split()))
    col2.metric("Caracteres", len(text))
    col3.metric("Vocabulário Único", len(set(text.split())))
    col4.metric("Tokens", len(tokens))


with st.expander("📄 Ver conteúdo do arquivo"):
    # Cria duas colunas para exibição dos resultados
    col1, col2 = st.columns(2)

    # Exibição do Texto Original
    col1.text_area('Texto Original', text, height=300)

    # Exibição do Texto Limpo
    col2.text_area('Texto Processado', text_clean, height=300)


with st.container(height=425):
    col1, col2 = st.columns([3, 1], gap="medium")

    col1.write('###### Palavras mais Frequentes')

    # Gráfico de Barras com as 15 palavras mais frequentes
    import altair as alt
    df = pd.DataFrame(freq_dist.most_common(15), columns=['Palavra', 'Frequência'])
    df = df.sort_values(by='Frequência', ascending=True)
    chart = alt.Chart(df).mark_bar(color="#ff7657").encode(
        x=alt.X("Frequência:Q", title=""),
        y=alt.Y("Palavra:N", title="", sort="-x"),
    )
    col1.altair_chart(chart, use_container_width=True)

    # Tabela com as 15 palavras mais frequentes
    col2.write('######')
    # Ordernar em ordem decrescente
    df = df.sort_values(by='Frequência', ascending=False)
    col2.dataframe(df.set_index('Palavra'), height=326, width=250)
    

with st.container(height=425):
    col1, col2 = st.columns([2, 1], gap="medium")

    col1.write('###### Bigramas mais Frequentes')

    # Gráfico de Barras com os 15 bigramas mais frequentes
    df = pd.DataFrame(bigram_freq.most_common(15), columns=['Bigrama', 'Frequência'])
    df = df.sort_values(by='Frequência', ascending=True)
    chart = alt.Chart(df).mark_bar(color="#ff7657").encode(
        x=alt.X("Frequência:Q", title=""),
        y=alt.Y("Bigrama:N", title="", sort="-x"),
    )
    col1.altair_chart(chart, use_container_width=True)

    # Tabela com os 15 bigramas mais frequentes
    col2.write('######')
    # Ordernar em ordem decrescente
    df = df.sort_values(by='Frequência', ascending=False)
    col2.dataframe(df.set_index('Bigrama'), height=326, width=340)


with st.container(height=580):
    st.write('###### Nuvem de Palavras')
    wordcloud = WordCloud(width=800, height=400, background_color='white', colormap='autumn').generate(' '.join(tokens))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    st.pyplot(plt)
