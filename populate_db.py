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

def write_doc_doc(con, cur, gamma_file):
    #cur.execute('CREATE TABLE doc_doc (id INTEGER PRIMARY KEY, doc_a INTEGER, doc_b INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX doc_doc_idx1 ON doc_doc(doc_a)')
    #cur.execute('CREATE INDEX doc_doc_idx2 ON doc_doc(doc_b)')
    con.commit()

    # for each line in the gamma file
    read_file = open(gamma_file, 'r')
    docs = []
    for doc in read_file:
        docs.append(list(map(float,doc.split())))
    read_file.close()
    for i in range(len(docs)):
        for j in range(len(docs[i])):
            #print(docs[i][j])
            docs[i][j] = math.pow(abs(docs[i][j]), 2)
    
    tamanho_docs = len(docs)
    print (tamanho_docs)
    id_autoincrement=0
    for a in range(len(docs)):
        if a % 1000 == 0:
            print ("doc " + str(a))
        doc_by_doc = {}
        for b in range(a, len(docs)):
            score = get_doc_score(docs[a], docs[b])
            if score == 0:
                continue
            elif len(doc_by_doc) < 100:
                doc_by_doc[score] = (a, b)
            else:
                max_score = max(doc_by_doc.keys())
                if max_score > score:
                    del doc_by_doc[max_score]
                    doc_by_doc[score] = (a, b)
        
        for doc in doc_by_doc:
            execution_string = 'INSERT INTO doc_doc (id, doc_a, doc_b, score) VALUES(%s, %s, %s, %s)'
            cur.execute(execution_string, [int(id_autoincrement), str(doc_by_doc[doc][0]), str(doc_by_doc[doc][1]), str(doc)])
            id_autoincrement = id_autoincrement + 1

    con.commit()

def write_doc_topic(con, cur, gamma_file):
    #cur.execute('CREATE TABLE doc_topic (id INTEGER PRIMARY KEY, doc INTEGER, topic INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX doc_topic_idx1 ON doc_topic(doc)')
    #cur.execute('CREATE INDEX doc_topic_idx2 ON doc_topic(topic)')
    con.commit()

    # for each line in the gamma file
    doc_no = 0
    id_autoincrement = 0
    for doc in open(gamma_file, 'r'):
        #doc = [float, doc.split()]
        doc = list(map(float, doc.split()))
        for i in range(len(doc)):
            #print(doc[i])
            cur.execute('INSERT INTO doc_topic (doc, topic, score) VALUES(%s, %s, %s)', [doc_no, i, doc[i]])
            id_autoincrement = id_autoincrement + 1
        doc_no = doc_no + 1

    con.commit()
        

def write_topics(con, cur, beta_file, vocab):
    #cur.execute('CREATE TABLE topics (id INTEGER PRIMARY KEY, title VARCHAR(100))')
    con.commit()

    # for each line in the beta file
    indices = range(len(vocab))
    #topics_file = open(filename, 'a')
    id_autoincrement = 0
    for topic in open(beta_file, 'r'):
        topic = list(map(float, topic.split()))
        indices = list(range(len(topic)))
        key_f = lambda x : -topic[x]
        indices.sort(key=key_f)
        #print(f"{vocab[indices[0]]} + ', ' + {vocab[indices[1]]} + ', ' + {vocab[indices[2]]}")
        #break
        cur.execute('INSERT INTO topics (id, title) VALUES(%s, %s)', [int(id_autoincrement),"{" + vocab[indices[0]] + ', ' + vocab[indices[1]] + ', ' + vocab[indices[2]] + '}'])
        id_autoincrement = id_autoincrement + 1
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


def write_topic_topic(con, cur, beta_file):
    #cur.execute('CREATE TABLE topic_topic (id INTEGER PRIMARY KEY, topic_a INTEGER, topic_b INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX topic_topic_idx1 ON topic_topic(topic_a)')
    #cur.execute('CREATE INDEX topic_topic_idx2 ON topic_topic(topic_b)')
    con.commit()
    # for each line in the beta file
    read_file = open(beta_file, 'r')
    topics = []
    topic_no = 0
    id_autoincrement = 0
    for topic in read_file:
        #topics = topics + list(map(float, topic.split()))
        topics.append(list(map(float, topic.split())))
        topic_no = topic_no +1
    
    topica_count = 0
    topic_by_topic = []
    for topica in topics:
        #topic_sim = r
        topicb_count = 0
        for topicb in topics:
            #if topic_by_topic.count((topicb_count, topica_count)) != 0:
            #    topicb_count +=1
            #    continue
            score = get_topic_score(topica, topicb)
            if (score == 0):
                topicb_count += 1
                continue
            cur.execute('INSERT INTO topic_topic (id, topic_a, topic_b, score) VALUES(%s, %s, %s, %s)', [int(id_autoincrement),topica_count, topicb_count, score])
            os.system(f"echo INSERT INTO topic_topic \(id, topic_a, topic_b, score\) VALUES \({id_autoincrement}, {topica_count}, {topicb_count}, {score}\) >> topicos_topicos")
            id_autoincrement = id_autoincrement + 1
            
            topic_by_topic.append((topica_count, topicb_count))
            topicb_count = topicb_count + 1
        topica_count = topica_count + 1

    con.commit()



def write_term_term(con, cur, beta_file, no_vocab):
    v = {}
    
    #cur.execute('CREATE TABLE term_term (id INTEGER PRIMARY KEY, term_a INTEGER, term_b INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX term_term_idx1 ON term_term(term_a)')
    #cur.execute('CREATE INDEX term_term_idx2 ON term_term(term_b)')
    con.commit()
    id_autoincrement = 0
    for i in range(no_vocab):
	    v[i] = []

    for topic in open(beta_file, 'r'):
        topic = list(map(float, topic.split()))
        for i in range(no_vocab):
            v[i].append(math.sqrt(math.exp(topic[i])))
    
    for terma in range(no_vocab):
        if terma % 1 == 0:
            print ("term " + str(terma))
        term_by_term = {}
        for termb in range(terma, len(vocab)):
            score = get_term_score(v[terma], v[termb])
            if score == 0:
                continue
            elif len(term_by_term) < 100:
                term_by_term[score] = (terma, termb)
            else:
                max_score = max(term_by_term.keys())
                if max_score > score:
                    del term_by_term[max_score]
                    term_by_term[score] = (terma, termb)
        
        for term in term_by_term:
            execution_string = 'INSERT INTO term_term (id, term_a, term_b, score) VALUES(%s, %s, %s, %s)'
            cur.execute(execution_string, [int(id_autoincrement), term_by_term[term][0], term_by_term[term][1], term])
            id_autoincrement = id_autoincrement + 1

    con.commit()
    
def write_doc_term(con, cur, wordcount_file, no_words):
    #cur.execute('CREATE TABLE doc_term (id INTEGER PRIMARY KEY, doc INTEGER, term INTEGER, score FLOAT)')
    #cur.execute('CREATE INDEX doc_term_idx1 ON doc_term(doc)')
    #cur.execute('CREATE INDEX doc_term_idx2 ON doc_term(term)')
    con.commit()
    
    doc_no = 0
    for doc in open(wordcount_file, 'r'):
        doc = doc.split()[1:]
        terms = {}
        for term in doc:
            terms[int(term.split(':')[0])] = int(term.split(':')[1])

        for i in range(no_words):
            score = 0
            if i in terms:
                score = terms[i]
                execution_string = 'INSERT INTO doc_term (doc, term, score) VALUES(%s, %s, %s)'
                cur.execute(execution_string, [doc_no, i, score])


        doc_no += 1
    
    con.commit()

def write_terms(con, cur, terms_file):
    #cur.execute('CREATE TABLE terms (id INTEGER PRIMARY KEY, title VARCHAR(100))')
    con.commit()
    id_autoincrement = 0
    for line in open(terms_file, 'r'):
        try:
            cur.execute('INSERT INTO terms (id, title) VALUES(%s, %s)', [str(id_autoincrement), line.strip()])
        except:
            print(f"Nao adicionada ao BANCO: {line}")
	id_autoincrement = id_autoincrement + 1
    con.commit()

def write_docs(con, cur, docs_file):
    #cur.execute('CREATE TABLE docs (id INTEGER PRIMARY KEY, title VARCHAR(100))')
    con.commit()
    id_autoincrement = 0
    for line in open(docs_file, 'r'):
        cur.execute('INSERT INTO docs (id, title) VALUES(%s, %s)', [int(id_autoincrement), line.strip()])
        id_autoincrement = id_autoincrement + 1
	
    controle = open("lastdoc_in","w")
    controle.write(str(id_autoincrement))
    controle.close()
    con.commit()


### main ###

if (__name__ == '__main__'):
    if (len(sys.argv) != 8):
       #print 'usage: python generate_csvs.py <db-filename> <doc-wordcount-file> <beta-file> <gamma-file> <vocab-file> <doc-file>\n'
       print ('usage: python generate_csvs.py <doc-wordcount-file> <beta-file> <gamma-file> <vocab-file> <doc-file>\n')

       sys.exit(1)

    #filename = sys.argv[1]
    doc_wordcount_file = sys.argv[1]
    beta_file = sys.argv[2]
    gamma_file = sys.argv[3]
    vocab_file = sys.argv[4]
    doc_file = sys.argv[5]
    banco = sys.argv[6]
    rootpass = sys.argv[7]

    # connect to database, which is presumed to not already exist
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password=rootpass,
        database=banco
    )
    #con = sqlite3.connect(filename)
    cur = con.cursor()

    # pre-process vocab, since several of the below functions need it in this format
    vocab = open(vocab_file, 'r').read()
    vocab = vocab.split("\n")
    #vocab = [lambda x: x.strip(), vocab]

    # write the relevant rlations to the database, see individual functions for details
    print ("writing terms to db...")
    write_terms(con, cur, vocab_file)
    
    print ("writing docs to db...")
    write_docs(con, cur, doc_file)
    
    print ("writing doc_doc to db...")
    write_doc_doc(con, cur, gamma_file)

    print ("writing doc_topic to db...")
    write_doc_topic(con, cur, gamma_file)

    print ("writing topics to db...")
    write_topics(con, cur, beta_file, vocab)

    print ("writing topic_term to db...")
    write_topic_term(con, cur, beta_file)

    print ("writing topic_topic to db...")
    write_topic_topic(con, cur, beta_file)
    
    print ("writing term_term to db...")
    ####write_term_term(con, cur, beta_file, len(vocab))
    
    print ("writing doc_term to db...")
    write_doc_term(con, cur, doc_wordcount_file, len(vocab))
