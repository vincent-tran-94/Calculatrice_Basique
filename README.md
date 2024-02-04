# Calculatrice_Basique avec l'intégration d'un Chatbot sur Flask 

Dans ce projet, j'ai mis en place une application web sur une calculatrice basique avec un chatbot en utilisant Flask et du JavaScript. <br>
L'objectif de ce site est de calculer les différents opérations par une expression mathématique d'une calculatrice et puis
de stocker dans les différents bases de données sur les opérations et les comptes qui ont été créés.
Le chatbot va nous indiquer comment marche la fonctionnalité de la calculatrice.

Ce projet va me permettre de comprendre les différents fonctionnnalités de base du backend pour la première création du site web avec de l'Intelligence Artificielle.

## Installation for setup:
This repo currently contains the starter files.

Clone repo and create a virtual environment
```
$ git clone https://github.com/vincent-tran-94/Calculatrice_Basique.git
$ python3 -m venv venv
$ . venv/bin/activate
```
Install dependencies
```
$ (venv) pip install -r requirements.txt 
```
Install nltk package
```
$ (venv) python
>>> import nltk
>>> nltk.download('punkt')
```
Modify `intents.json` with different intents and responses for your Chatbot

Run
```
$ (venv) python train.py
```
This will dump data.pth file. And then run the following command to test it in the console.

You need to install postgresql to configure your setup connexion
https://www.postgresql.org/download/

Then you need to configure your database name, your user and your password in script create_postgre.py 

Run to create two tables (users and operations) in database 
```
$ (venv) python create_postgre.py
```
Run your app Flask 
```
$ (venv) python main.py
```
Now for deployment follow my tutorial to implement `main.py`
After implement `main.py` connect your first site in http://localhost:5000/login  <br>
and go to register to create the first account in page register: http://localhost:5000/register <br>

