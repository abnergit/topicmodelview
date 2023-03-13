import sys
import math
#import sqlite3
import mysql.connector
import functools
import os


### score functions ###

def get_doc_score(doca, docb):
    score = 0
    total = 0
    for topic_id in range(len(doca)):
        thetaa = doca[topic_id]
        thetab = docb[topic_id]
        if not ((thetaa != 0.0 and thetab == 0.0) or (thetaa == 0.0 and thetab != 0.0)):
            score += math.pow(thetaa - thetab, 2)
    return 0.5 * score

def get_topic_score(topica, topicb):
    score = 0
    #print(topica)
    #print(topica.keys())
    total = math.pow(abs(math.sqrt(100) - math.sqrt(0)), 2) * len(topica)
    for term_id in range(len(topica)):
        #print(topica[1])
        #print(topica[1][1])
        thetaa = abs(topica[term_id])
        thetab = abs(topicb[term_id])
        score += math.pow(abs(math.sqrt(thetaa) - math.sqrt(thetab)), 2)
    return 0.5 * score / total

def get_term_score(terma, termb):
    score = 0
    for term_id in range(len(terma)):
        score += math.pow(terma[term_id] - termb[term_id], 2)
    return score


### write relations to db functions ###



def write_docs(con, cur, total_redacoes):
    #cur.execute('CREATE TABLE docs (id INTEGER PRIMARY KEY, title VARCHAR(100))')
    con.commit()
    id_autoincrement = int(open("lastdoc_in","r").read())
    for i in range(int(total_redacoes)):
    
        red_nome = f"red_{i}"
        cur.execute('INSERT INTO docs (id, title) VALUES(%s, %s)', [int(id_autoincrement), red_nome])
        id_autoincrement = id_autoincrement + 1
	
    controle = open("lastdoc_in","w")
    controle.write(str(id_autoincrement))
    controle.close()
    con.commit()

def write_doc_topic(con, cur):
    #cur.execute('CREATE TABLE doc_topic (id INTEGER PRIMARY KEY, doc INTEGER, topic INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX doc_topic_idx1 ON doc_topic(doc)')
    #cur.execute('CREATE INDEX doc_topic_idx2 ON doc_topic(topic)')
    con.commit()

    # for each line in the gamma file
    arquivo = open('redacao_topico_score', 'r').read().split("\n")

    for doc in arquivo:
        doc_no = int(doc.split(" ")[0])
        topic_no = doc.split(" ")[1]
        score = doc.split(" ")[2]
        for i in range(len(doc)):
            #print(doc[i])
            cur.execute('INSERT INTO doc_topic (doc, topic, score) VALUES(%s, %s, %s)', [doc_no, topic_no, score])
        doc_no = doc_no + 1

    con.commit()
        
def write_topic_term(con, cur, beta_file):
    #cur.execute('CREATE TABLE topic_term (id INTEGER PRIMARY KEY, topic INTEGER, term INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX topic_term_idx1 ON topic_term(topic)')
    #cur.execute('CREATE INDEX topic_term_idx2 ON topic_term(term)')
    con.commit()
    
    topic_no = 0
    id_autoincrement = 0
    #topic_term_file = open(filename, 'a')
    
    for topic in open(beta_file, 'r'):
        topic = list(map(float, topic.split()))
        indices = list(range(len(topic))) # note: len(topic) should be the same as len(vocab)
        key_f = lambda x : -topic[x]
        indices.sort(key=key_f)
        for i in range(len(topic)):
            cur.execute('INSERT INTO topic_term (id, topic, term, score) VALUES(%s, %s, %s, %s)', [int(id_autoincrement), topic_no, indices[i], topic[indices[i]]])
            id_autoincrement = id_autoincrement + 1
        topic_no = topic_no + 1

    con.commit()



### main ###

if (__name__ == '__main__'):
    if (len(sys.argv) != 4):

       print ('usage: python redacao_db.py <Nome_Banco> <Senha_Banco> <Quantidade redações>\n')

       sys.exit(1)


    banco = sys.argv[1]
    rootpass = sys.argv[2]
    quantas_redacoes = sys.argv[3]

    # connect to database, which is presumed to not already exist
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password=rootpass,
        database=banco
    )
    #con = sqlite3.connect(filename)
    cur = con.cursor()


    # write the relevant rlations to the database, see individual functions for details


    print ("writing doc_topic to db REDAÇÕES...")
    write_doc_topic(con, cur)
    
    print ("writing doc_term to db REDAÇÕES...")
    #write_doc_term(con, cur, doc_wordcount_file, len(vocab))
    
    write_docs(con, cur, quantas_redacoes)
    
    
    
    
