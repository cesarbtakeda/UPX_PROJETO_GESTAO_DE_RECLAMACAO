import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import os

def gerar_graficos():
    try:
        # Verifica se o arquivo existe
        if not os.path.exists('reclamacoes/dados.txt'):
            return False, "Arquivo 'dados.txt' não encontrado!"

        # Lê o arquivo TXT 
        with open('dados.txt', 'r', encoding='utf-8') as f:
            linhas = f.readlines()

        # Cria um DataFrame com os dados
        df = pd.DataFrame(linhas, columns=['texto'])

        # Remove linhas inválidas
        df = df[df['texto'].str.len() > 10]
        df = df[~df['texto'].str.contains(r'^[;]+$', regex=True)]

        # Limpeza do texto
        def limpar_texto(texto):
            if "Status da reclamação:" in texto:
                texto = texto.split("Status da reclamação:")[-1]
            texto = re.sub(r'^(Em réplica|Não resolvido|Respondida|Resolvido|Não respondida)', '', texto, flags=re.IGNORECASE)
            texto = re.sub(r'Esta reclamação possui mais de \d+ ano[s]? e não está mais sendo contabilizada no índice da empresaVer todas Reclamações\.?', '', texto, flags=re.IGNORECASE)
            texto = re.sub(r'Essa reclamação foi publicada há mais de 1 anoVer todas Reclamações', '', texto, flags=re.IGNORECASE)
            return texto.strip()

        df['texto_limpo'] = df['texto'].apply(limpar_texto)

        # Configura stopwords
        nltk.download('stopwords', quiet=True)
        stopwords_pt = set(stopwords.words('portuguese'))
        
        stopwords_customizadas = {
            'rua', 'prefeitura', 'casa', 'sorocaba', 'container', 'moradores', 'pra', 'onde',
            'frente', 'pois', 'dia', 'contato', 'fazer', 'fiz', 'resposta', 'imóvel', 'pessoas',
            'nada', 'aqui', 'mesma', 'agora', 'telefone', 'local', 'cid', 'favor', 'novamente',
            'entrar', 'https', 'sempre', 'porém', 'prefeito', 'sp', 'bairro', 'município', 'casas',
            'solicitar', 'falta', 'vezes', 'sobre', 'bom', 'ter', 'reclamação', 'problema', 'dias',
            'desta', 'vários', 'cidade', 'desde', 'número', 'faz', 'encontra', 'meio', 'aguardo',
            'quase', 'via', 'atendimento', 'inclusive', 'vem', 'venho', 'tudo'
        }
        
        stopwords_total = stopwords_pt.union(stopwords_customizadas)

        # Pré-processamento
        def preprocessar_texto(texto):
            texto = texto.lower()
            texto = re.sub(r'[^\w\s]', '', texto)
            texto = re.sub(r'\d+', '', texto)
            palavras = [palavra for palavra in texto.split() if palavra not in stopwords_total]
            return ' '.join(palavras)

        df['texto_preprocessado'] = df['texto_limpo'].apply(preprocessar_texto)

        # Cria pasta para gráficos
        os.makedirs('graficos', exist_ok=True)

        # 1. Nuvem de palavras
        texto_total = ' '.join(df['texto_preprocessado'])
        wordcloud = WordCloud(width=800, height=400, background_color='white', max_words=100).generate(texto_total)
        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        plt.savefig('graficos/wordcloud_reclamacoes.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Top 20 palavras
        vectorizer = CountVectorizer()
        X = vectorizer.fit_transform(df['texto_preprocessado'])
        frequencia = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out()).sum().sort_values(ascending=False)
        top_palavras = frequencia.head(20)
        
        plt.figure(figsize=(10,6))
        top_palavras.plot(kind='barh', color='skyblue')
        plt.xlabel('Frequência')
        plt.title('20 Palavras mais frequentes nas reclamações')
        plt.gca().invert_yaxis()
        plt.savefig('graficos/top_20_barras.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 3. Bigramas
        vectorizer_bigram = CountVectorizer(ngram_range=(2, 2), stop_words=list(stopwords_total))
        X_bigram = vectorizer_bigram.fit_transform(df['texto_preprocessado'])
        df_bigram = pd.DataFrame({
            'bigramas': vectorizer_bigram.get_feature_names_out(),
            'frequencia': X_bigram.sum(axis=0).A1
        }).sort_values(by='frequencia', ascending=False).head(20)
        
        plt.figure(figsize=(12, 8))
        plt.barh(df_bigram['bigramas'], df_bigram['frequencia'], color='mediumseagreen')
        plt.xlabel('Frequência')
        plt.title('Top 20 Bigramas Mais Frequentes')
        plt.gca().invert_yaxis()
        plt.grid(axis='x', linestyle='--', alpha=0.7)
        plt.savefig('graficos/top_20_bigramas.png', dpi=300, bbox_inches='tight')
        plt.close()

        # 4. Histograma de palavras
        df['n_palavras'] = df['texto_preprocessado'].str.split().str.len()
        plt.figure(figsize=(8,6))
        plt.hist(df['n_palavras'], bins=15, color='purple', edgecolor='black')
        plt.title('Distribuição do tamanho dos textos')
        plt.xlabel('Número de palavras')
        plt.ylabel('Quantidade de Reclamações')
        plt.savefig('graficos/histograma_numero_palavras.png', dpi=300, bbox_inches='tight')
        plt.close()

        return True, "Gráficos gerados com sucesso em /graficos/"
        
    except Exception as e:
        return False, f"Erro ao gerar gráficos: {str(e)}"

if __name__ == "__main__":
    gerar_graficos()

## Desenvolvido por Enzo parra e Cesar Augusto - Ideia De Enzo Parra e Cesar Augusto
