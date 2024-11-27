from flask import Flask, render_template, redirect, request, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'abi'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pharmacy'
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')

# Route to view all medicines
@app.route('/medicines')
def medicines():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM medicine")
    medicines_info = cur.fetchall()
    cur.close()
    return render_template('medicines.html', medicines=medicines_info)

# Route to search for a specific medicine by ID
@app.route('/search_medicine', methods=['POST', 'GET'])
def search_medicine():
    search_results = []
    search_term = ''
    if request.method == "POST":
        search_term = request.form['med_id']
        cur = mysql.connection.cursor()
        query = "SELECT * FROM medicine WHERE med_id LIKE %s"
        cur.execute(query, ('%' + search_term + '%',))
        search_results = cur.fetchmany(size=1)
        cur.close()
        return render_template('medicines.html', medicines=search_results)

# Route to insert a new medicine
@app.route('/insert_medicine', methods=['POST'])
def insert_medicine():
    if request.method == "POST":
        med_id = request.form['med_id']
        med_name = request.form['med_name']
        description = request.form['description']
        quantity = request.form['quantity']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO medicine (med_id, med_name, description, quantity) VALUES (%s, %s, %s, %s)", (med_id, med_name, description, quantity))
        mysql.connection.commit()
        return redirect(url_for('medicines'))

# Route to delete a medicine by ID
@app.route('/delete_medicine/<string:med_id>', methods=['GET'])
def delete_medicine(med_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM medicine WHERE med_id = %s", (med_id,))
    mysql.connection.commit()
    return redirect(url_for('medicines'))

# Route to update an existing medicine
@app.route('/update_medicine', methods=['POST', 'GET'])
def update_medicine():
    if request.method == 'POST':
        med_id = request.form['med_id']
        med_name = request.form['med_name']
        description = request.form['description']
        quantity = request.form['quantity']
        
        cur = mysql.connection.cursor()
        cur.execute("UPDATE medicine SET med_name = %s, description = %s, quantity = %s WHERE med_id = %s", (med_name, description, quantity, med_id))
        mysql.connection.commit()
        return redirect(url_for('medicines'))

if __name__ == "__main__":
    app.run(debug=True)
