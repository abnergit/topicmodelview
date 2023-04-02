import requests
from bs4 import BeautifulSoup
import os
import sys
import concurrent.futures
from queue import Queue
import urllib.parse

visited_pages = Queue()
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
        os.system("pkill -f wiki_scraping_corpus.py")
        return
    artigo = url.split("/wiki/")[1]
    
    if artigo[0].isnumeric:
        #Para evitar artigos que tratem de datas. São um pouco confusos
        return
    
    if url in visited_pages.queue:
        sys.exit(0)

    visited_pages.put(url)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    contents = soup.find_all(class_="mw-parser-output")
    text = ""
    for content in contents:
        for table in content.find_all("table"):
            table.decompose()
        text += content.get_text()
    text = text.split("Referências\n")[0]
    #Essa linha acima irá ignorar as referências e bibliografias, pois trazem muitas palavras repetidas que atrapalham a modelagem
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
            futures = [executor.submit(extract_text_from_wiki, "https://pt.wikipedia.org" + link) for link in links[:50]]

# Começa a extração de texto a partir da página principal da Wikipedia
extract_text_from_wiki(link_principal)

