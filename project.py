#!/bin/python3
import os
import time

########### VERIFICANDO PERM DO USUÁRIO ############
if (not os.access("/var/www/html",os.W_OK)):
	print("Seu usuário não tem permissão em /var/www/html ou apache2 não está instalado")
	exit()


####### CRIANDO BANCO DE DADOS #####################
nome_projeto = " "
while(" " in nome_projeto):
	nome_projeto = input("Informe o nome do Projeto sem espaços: ")

password = input("MySQL root password: ")
senha_valida = os.system(f"echo \"create database {nome_projeto};\" | mysql -u root -p{password} 2>/dev/null")
if (senha_valida != 0):
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



pt_stopwords = set(stopwords.words('portuguese'))

tokenizer = RegexpTokenizer(r'\s+', gaps=True)
stemmer = PorterStemmer()
translate_tab = {ord(p): u" " for p in punctuation}

def text2tokens(raw_text):
    """Split the raw_text string into a list of stemmed tokens."""
    clean_text = raw_text.lower().translate(translate_tab)
    tokens = [token.strip() for token in tokenizer.tokenize(clean_text)]
    tokens = [token for token in tokens if token not in pt_stopwords]
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return [token for token in stemmed_tokens if len(token) > 2 and not token.isnumeric()]  # skip short tokens and numeric

dataset = [text2tokens(txt) for txt in documentos_lista]  # convert a documents to list of tokens

from gensim.corpora import Dictionary
print(dataset)
dictionary = Dictionary(documents=dataset, prune_at=None)
dictionary.filter_extremes(no_below=5, no_above=0.5, keep_n=None)  # use Dictionary to remove un-relevant tokens
dictionary.compactify()

d2b_dataset = [dictionary.doc2bow(doc) for doc in dataset]  # convert list of tokens to bag of word representation

######################## GERANDO DOC FILE #################################################

doc_file = open("doc_file.txt","w")
lista = []

for index, texto in enumerate(documentos_lista):
    
    saida = open(f"corpus/doc_{index}","w")
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
#num_topics = 5

lda_fst = LdaMulticore(
    corpus=d2b_dataset, num_topics=num_topics, id2word=dictionary,
    workers=4, eval_every=None, passes=10, batch=True,
)

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

######### INICIANDO A APLICAÇÃO PHP NO SERVIDOR APACHE ###########


conexao = open("app/conexao_modelo.php","r").read()

new_conexao = conexao.replace("senha_banco",password)
new_conexao = new_conexao.replace("login_banco","root")
new_conexao = new_conexao.replace("nome_projeto",nome_projeto)

save = open("app/conexao.php","w")
save.write(new_conexao)
save.close()

os.system(f"cp -R corpus/ app/")
os.system("cd app/;php -S localhost:2000")




























