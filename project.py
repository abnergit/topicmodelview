#!/bin/python3
import os
import sys
import time
import nltk

### VERIFICA SE HA UM CORPUS DEFINIDO #####
if not os.path.exists("corpus"):
	print("Você ainda não possui um corpus.")
	print("Posso buscar para você na wikipedia um corpus a partir de um artigo inicial da wikipedia.")
	tamanho = input("Informe o tamanho do corpus desejado: ")
	wiki_url = input("Informe o artigo da Wikipedia que será o ponto de partida: ")

	print("Aguarde enquanto o corpus está sendo gerado...")
	os.system(f"python3 wiki_scraping_corpus.py {wiki_url} {tamanho}")
	#os.wait()

	
##### VERIFICA SE O MODELO JÁ FOI EXECUTADO ######
nome_projeto = " "
app_conexao = open("app/conexao.php","r").read()
password = input("MySQL root password: ")
if ("nome_database" not in app_conexao):
	#print("Esse projeto já foi executado anteriormente. Se quiser um novo projeto, clone do git https://github.com/abnergit/topicmodelview..")
	print("Esse projeto já foi compilado anteriormente.")
	print("Pressione ENTER para iniciar a visualização.")
	print("Caso deseje avaliar as redações, digite [Y/y]: ",end='')
	nome_projeto = app_conexao.split("base = \"")[1].split("\"")[0]
	recompilar = input()
	if recompilar.lower() != "y":
		os.system("cd app/;php -S localhost:2000")
		sys.exit(0)
	
	
else:
    ####### CRIANDO BANCO DE DADOS #####################
	
	
    while(" " in nome_projeto):
        nome_projeto = input("Informe o nome do Projeto sem espaços: ")
    senha_valida = os.system(f"echo \"create database {nome_projeto};\" | mysql -u root -p{password} 2>/dev/null")
    if (senha_valida != 0):
        print("Erro ao criar projeto. Verifique se a senha está correta ou se já não existe um projeto com o mesmo nome")
        exit()
    
    ################# Parâmetros do MODELO ###############
    num_topics = int(input("Informe a quantidade de tópicos desejado: "))
    
    
    time.sleep(1)
    os.system(f"mysql -u root -p{password} {nome_projeto} < banco.sql 2>/dev/null")
    
    #####################################################




###### CRIANDO ARQUIVOS #############################

import logging
from string import punctuation
from nltk import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from sklearn.datasets import fetch_20newsgroups

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

documentos_lista = []
arquivos = os.listdir("corpus/")
for arquivo in arquivos:
    texto = open("corpus/"+arquivo,"r")
    documentos_lista.append(texto.read())
    texto.close()
print("Total documentos:"+str(len(documentos_lista)))

redacoes_lista = []
try:
    redacoes = os.listdir("redações/")
    for redacao in redacoes:
        texto = open("redações/"+redacao,"r")
        redacoes_lista.append(texto.read())
        texto.close()
    print("Total Redações:"+str(len(redacoes_lista)))
except:
    os.mkdir("redações")

if not os.path.exists("app/redações"):
    os.mkdir("app/redações")
    
lista = [] 
for index, texto in enumerate(redacoes_lista):
    
    saida = open(f"app/redações/red_{index}","w")
    lista.append(f"red_{index}")
    saida.write(texto)
    saida.close()



nltk.download('stopwords')
pt_stopwords = set(stopwords.words('portuguese'))
eng_stopwords = set(stopwords.words('english'))
outros_stopwords = ['inglês','pdf', '1–2','2–3','issn','podem','pode','durante', 'manut', 'link','cs1','pmid','doi','displaystyle','mathbf', 'isbn', 'iii', 'frac', 'left', 'right', 'press', 've', 'consultado', 'arquivada', 'cópia','vec','sen','cos','van']

tokenizer = RegexpTokenizer(r'\s+', gaps=True)
stemmer = PorterStemmer()
#Essa linha mapeia pontuações do módulo punctuation por espaços em branco usando seu respectivo unicode para substituição.
punctuation = punctuation + "»«”“"
translate_tab = {ord(p): u" " for p in punctuation}

def text2tokens(raw_text):
    """Split the raw_text string into a list of stemmed tokens."""
    clean_text = raw_text.lower().translate(translate_tab) #Faz as substituições de pontuações
    tokens = [token.strip() for token in tokenizer.tokenize(clean_text)]
    tokens = [token for token in tokens if token not in pt_stopwords]
    tokens = [token for token in tokens if token not in eng_stopwords]
    tokens = [token for token in tokens if token not in outros_stopwords]
    #stemmed_tokens = [stemmer.stem(token) for token in tokens]
    #return [token for token in stemmed_tokens if len(token) > 2 and not token.isnumeric()]  # skip short tokens and numeric
    return [token for token in tokens if len(token) > 2 and not token.isnumeric()]  # skip short tokens and numeric		  



############## RECARREGA O MODELO PARA AVALIAR REDAÇÕES #################################

if os.path.exists('modelo/modelo.lda'):
    from gensim.models import LdaModel
    lda_fst = LdaModel.load('modelo/modelo.lda')
    arquivo1 = open("redacao_topico_score","w")
    arquivo2 = open("redacao_bow","w")
    ultimo_doc = int(open("lastdoc_in","r").read())
    arquivo_conteudo = []
    bow_conteudo = []
    for redacao in redacoes_lista:
        redacao_word = text2tokens(redacao)
        dicionario = lda_fst.id2word
        redacao_word_bow = dicionario.doc2bow(redacao_word)
        redacao_topics = lda_fst.get_document_topics(redacao_word_bow)
        for registro in redacao_word_bow:
            bow_conteudo.append(f"{ultimo_doc} {registro[0]} {registro[1]}")
        for registro in redacao_topics:
            arquivo_conteudo.append(f"{ultimo_doc} {registro[0]} {registro[1]}")

        ultimo_doc = ultimo_doc + 1
    arquivo1.write("\n".join(arquivo_conteudo))
    arquivo2.write("\n".join(bow_conteudo))
    arquivo1.close()
    arquivo2.close()
    if len(redacoes_lista) == 0:
    	print("As redações não foram adicionadas")
    else:
    	os.system(f"python3 redacao_db.py {nome_projeto} {password} {len(redacoes_lista)}")
    
    os.system("cd app/;php -S localhost:2000")
    sys.exit(0)
########################################################################################




dataset = [text2tokens(txt) for txt in documentos_lista+redacoes_lista]  # convert a documents to list of tokens

from gensim.corpora import Dictionary
#print(dataset)
no_below = int(len(dataset)*0.05)
dictionary = Dictionary(documents=dataset, prune_at=None)
dictionary.filter_extremes(no_below=no_below, no_above=0.10, keep_n=None)  # use Dictionary to remove un-relevant tokens
dictionary.compactify()

d2b_dataset = [dictionary.doc2bow(doc) for doc in dataset]  # convert list of tokens to bag of word representation

######################## GERANDO DOC FILE - CORPUS e REDAÇÃO #################################################

doc_file = open("doc_file.txt","w")

if not os.path.exists("app/corpus"):
    os.mkdir("app/corpus")
for index, texto in enumerate(documentos_lista):
    
    saida = open(f"app/corpus/doc_{index}","w")
    lista.append(f"doc_{index}")
    saida.write(texto)
    saida.close()


doc_file.write("\n".join(lista))
doc_file.close()

############################################################################################

####################### DOC WORDCOUNT #####################################################
print("GERANDO DOC WORDCOUNT...")

arquivo = open("doc_wordcount_file.txt","w")
linhas = []
for index, texto in enumerate(d2b_dataset):
    linha = str(index)
    for palavra in texto:
        linha = linha + " " + str(palavra[0])+":"+str(palavra[1])
    linhas.append(linha)
    
arquivo.write("\n".join(linhas))
arquivo.close()



############################################################################################

############################### VOCAB FILE #################################################
print("GERANDO VOCAB FILE...")
dicionario = open("vocab_file.txt","w")
dic_list = []
for i in range(len(dictionary)):
    dic_list.append(dictionary[i])
dicionario.write("\n".join(dic_list))
dicionario.close()

#print(dictionary[1])
############################################################################################

###########GERANDO MODELO LDA ##############################################################
print("GERANDO MODELO LDA ...")
from gensim.models import LdaMulticore
from gensim.corpora import MmCorpus
from gensim.corpora import Dictionary
#num_topics = 5
alpha = 0.1
eta = 0.1
iterations = 200
passes = 32

lda_fst = LdaMulticore(
    corpus=d2b_dataset, num_topics=num_topics, id2word=dictionary,alpha=alpha, eta=eta,
    workers=8, eval_every=None, passes=passes, batch=True, iterations=iterations
)

os.system("mkdir modelo")
lda_fst.save('modelo/modelo.lda')
#dic_gensim = Dictionary(dic_list)
#dic_gensim.save('modelo/dicionario')
#MmCorpus.serialize('modelo/corpus.mm', d2b_dataset)
############################################################################################

########### GERANDO BETA FILE TXT ##########################################################
print("GERANDO BETA FILE ...")
total_palavras = len(open("vocab_file.txt").readlines())
beta = open("betafile.txt","w")
beta_texto = ""
sorted(lda_fst.get_topic_terms((num_topics-1),topn=total_palavras))
for i in range(num_topics):
    lista_beta_tupla = sorted(lda_fst.get_topic_terms(i,topn=total_palavras))
    for j in range(total_palavras):
        if(j==0):
            beta_texto = beta_texto+str(lista_beta_tupla[j][1])
        else:
            beta_texto = beta_texto+" "+str(lista_beta_tupla[j][1])
    beta_texto = beta_texto+"\n"

beta.write(beta_texto)
beta.close()

############################################################################################
########### GERANDO GAMMA FILE TXT #########################################################
print("GERANDO GAMMA FILE ...")
#for bow in d2b_dataset:
    
#d2b_dataset[1]
total_documentos = len(open("doc_file.txt","r").readlines())
gamma = open("gamma_file.txt","w")
gamma_text = []

#num_topics
for texto_id in range(total_documentos):
    topicid_valor = lda_fst.get_document_topics(d2b_dataset[texto_id])
    linha = []
    for topico in range(num_topics):
        linha.append("0")
    
    for tupla in topicid_valor:
        linha[tupla[0]] = str(tupla[1])
    
    gamma_text.append(" ".join(linha))

gamma.write("\n".join(gamma_text))
gamma.close()

############################################################################################

################### POPULANDO BANCO DE DADOS ###############################################


os.system(f"python3 populate_db.py doc_wordcount_file.txt betafile.txt gamma_file.txt vocab_file.txt doc_file.txt {nome_projeto} {password}")

######### INICIANDO A APLICAÇÃO WEB PHP ###########


conexao = open("app/conexao_modelo.php","r").read()

new_conexao = conexao.replace("senha_banco",password)
new_conexao = new_conexao.replace("login_banco","root")
new_conexao = new_conexao.replace("nome_projeto",nome_projeto)

save = open("app/conexao.php","w")
save.write(new_conexao)
save.close()

#os.system(f"cp -R corpus/ app/")
#MOVE O CORPUS PARA DENTRO DA APLICACAO

os.system("cd app/;php -S 0.0.0.0:2000")
