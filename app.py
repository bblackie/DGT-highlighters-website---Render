# app.py

from flask import Flask, g, render_template
import sqlite3

DATABASE = 'database.db'

app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv





@app.route("/")
def home():
    # home page - Just the ID, Brand, Name and ImageURL1
    sql_highlighters = """
        SELECT Highlightersnew.HighlighterID, Brandsnew.Name, Highlightersnew.Name, Highlightersnew.ImageURL1 
        FROM Highlightersnew
        JOIN Brandsnew ON Brandsnew.BrandID = Highlightersnew.BrandID;
    """

    # home page - Brand buttons for each highlighter brand
    sql_brands = "SELECT BrandID, Name FROM Brandsnew;"

    results = query_db(sql_highlighters)
    brands = query_db(sql_brands)

    
    return render_template('home.html', results=results, brands=brands)

@app.route("/highlighter/<int:id>")
def highlighter(id):
    #just one highlighter based on the id
    sql = """
             SELECT * FROM Highlightersnew 
             JOIN Brandsnew ON Brandsnew.BrandID=Highlightersnew.BrandID 
             WHERE Highlightersnew.HighlighterID = ?;
          """
    result = query_db(sql,(id,),True) 
    return render_template('highlighter.html', highlighter=result)

@app.route("/brand/<int:brand_id>")
def brand(brand_id):
    #brands buttons on home page - shows all highlighters for that brand
    sql = """
        SELECT Highlightersnew.HighlighterID, Brandsnew.Name, Highlightersnew.Name, Highlightersnew.ImageURL1
        FROM Highlightersnew
        JOIN Brandsnew ON Brandsnew.BrandID = Highlightersnew.BrandID
        WHERE Brandsnew.BrandID = ?;
    """
    results = query_db(sql, (brand_id,))
    return render_template('home.html', results=results)



@app.route('/comparison')
def comparison():
    #comparison page - table of data of all the highlighters in the website
    conn = sqlite3.connect('database.db')
    

    
    resultss = conn.execute(
        "SELECT Highlightersnew.BrandID, Highlightersnew.Cost, Highlightersnew.Description FROM Highlightersnew"
        ).fetchall()

    conn.close()
    return render_template('comparison.html', highlighter=resultss)


if __name__ == "__main__":
    app.run(debug=True)