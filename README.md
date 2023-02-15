# Topic Model Viewer
This is a web application to view and navigate into a LDA model.

Python 3.8.10

PHP 7.4.3


# project.py

python3 project.py

Inform a simple name to your project and your mysql password to create the database.
The script will search into a directory named **corpus**. 
Each file in the **corpus** directory is a document to the LDA.
Each file need to be named as: **doc_0, doc_1, doc_2** and so on...


When the script is done, your project is ready!
A PHP web service will be started at 2000 TCP door. Ensure that this door is free.

# Bibliotecas para instalação:

pip3 install bs4
pip3 install nltk
pip3 install -U scikit-learn
pip3 install -U gensim
pip3 install -U mysql-connector-python
apt install php-mysqli
