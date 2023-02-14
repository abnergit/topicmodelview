import requests
from bs4 import BeautifulSoup
import os
import sys
import concurrent.futures
from queue import Queue
import urllib.parse

visited_pages = set()
doc_id_queue = Queue()
if len(sys.argv) != 3:
    print("Uso: python script.py <link_wikipedia> <tamanho_corpus>")
    sys.exit(1)
    
link_principal = sys.argv[1]
tamanho_corpus = int(sys.argv[2])
# Cria a pasta "corpus" se ainda não existir
if not os.path.exists("corpus"):
    os.makedirs("corpus")

# Preenche a fila com os ids dos documentos
for i in range(tamanho_corpus):
    doc_id_queue.put(i)

def extract_text_from_wiki(url):
    if doc_id_queue.empty(): #Se a fila estiver vazia, encerra a execução
        print("FIM")
        return

    if url in visited_pages:
        return

    visited_pages.add(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    contents = soup.find_all(class_="mw-parser-output")
    text = ""
    for content in contents:
        for table in content.find_all("table"):
            table.decompose()
        text += content.get_text()
    
    if len(text.encode('utf-8')) > 10240: #Se o tamanho do texto for superior a 10kB
        doc_id = doc_id_queue.get()
        with open(f"corpus/doc_{doc_id}", "w") as f:
            url = urllib.parse.unquote(url)
            text = f"{url}\n\n" + text
            f.write(text)
        
        links = []
        for link in content.find_all("a"):
            href = link.get("href")
            try:
                if href and href.startswith("/wiki/"):
                    links.append(href)
            except:
                print(f"Não foi possível capturar a pagina: {href}")

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(extract_text_from_wiki, "https://pt.wikipedia.org" + link) for link in links[:10]]
            concurrent.futures.wait(futures)

# Começa a extração de texto a partir da página principal da Wikipedia
extract_text_from_wiki(link_principal)
