import sqlite3

conn = sqlite3.connect('database.db')                           #connecter au base des donnees
c = conn.cursor() 						 #creer un cursor 

c.execute(               				         #creer un tableau
	'''CREATE TABLE IF NOT EXISTS PHONEBOOK
		(  NOM TEXT PRIMARY KEY,  \
		  NUMERO TEXT \
		  )''' 
		)
conn.commit() 



from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/') # affichage de la page principal  
def index():
    return render_template('index.html')

@app.route('/total') # affichage de tout les numeros  
def total():
    return render_template('total.html')

@app.route('/ajout') # page pour ajouter le numero 
def ajout():
    return render_template('ajout.html')

@app.route('/recherche') # page pour le recherche du numero 
def recherche():
    return render_template('recherche.html')

@app.route('/supprimer') # page pour supprimer le numero 
def supprimer():
    return render_template('supprimer.html')

@app.route('/choix') # page pour faire le choix
def choix():
    return render_template('choix.html')

@app.route('/replacer') # page pour replacer le contact
def replacer():
    return render_template('replacer.html')

@app.route('/ajout_fait',methods = ['POST']) #ecriture du numero et le nom dans le fichier 
def ajout_fait():
    result = request.form
    nom = result['nom']
    num = result['numero']
    
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM PHONEBOOK WHERE nom = ?', [nom])
    rows = cur.fetchone()
    con.close()
    if rows is None :
         con = sqlite3.connect("database.db")
         cur = con.cursor()
         cur.execute("INSERT INTO PHONEBOOK (nom,numero) VALUES (?,?)", (nom,num))
         con.commit()
         con.close()
         return render_template("ajout_fait.html",numero = num)
    else:
         return render_template("choix.html",numero = num)
     
@app.route('/choix_fait',methods = ['POST']) #replacer le numero et le nom dans le fichier 
def choix_fait():
    result = request.form
    nom = result['nom']
    num = result['numero']
    
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("REPLACE INTO PHONEBOOK (nom,numero) VALUES (?,?)", (nom,num))
    con.commit()
    con.close()
    return render_template("choix_fait.html",numero = num)
    

@app.route('/res_recherche',methods = ['POST']) # recherche du numero par nom dans le repertoire_web.txt 
def res_recherche():
    result = request.form
    n = result['nom'] 

    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute('SELECT * FROM PHONEBOOK WHERE nom = ?', [n])
    rows = cur.fetchone()
    con.close()
    if rows is None:
         return render_template("fail.html", nom = n )   
    else:
        num = rows[1]
        return render_template("res_recherche.html", nom = n, numero = num )   
       
        
    
@app.route('/res_supprimer',methods = ['POST']) #supprimer le numero et le nom dans la base de donnees 
def res_supprimer():
    result = request.form
    n = result['nom'] 
    
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM PHONEBOOK WHERE nom='"+ n +"'")
    con.commit()
    con.close()
    return render_template("res_suppr.html",nom = n)
    
@app.route('/res_total',methods = ['POST']) #afficher les numeros et les noms dans la base de donnees 
def res_total():        
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM PHONEBOOK")
    total = cur.fetchall()
    total1 = [x[0] for x in total]
    total2 = [x[1] for x in total]
    con.close()
    
    return render_template("res_total.html", total = total, total1 = total1, total2 = total2)
   
    
app.run(debug=True)