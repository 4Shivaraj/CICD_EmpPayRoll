from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = 'many random bytes'

server = os.getenv('MSSQL_SERVER')
database = os.getenv('DATABASE')  # Use the AdventureWorks database
connection_string = f'DRIVER=SQL Server;SERVER={server};DATABASE={database};Trusted_Connection=yes;'
cnxn = pyodbc.connect(connection_string)
cursor = cnxn.cursor()

@app.route('/')
def Index():
    cursor.execute("SELECT BusinessEntityID, NationalIDNumber, JobTitle, BirthDate, Gender, SalariedFlag FROM HumanResources.Employee")
    data = cursor.fetchall()
    return render_template('index.html', employee=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        BusinessEntityID = request.form['BusinessEntityID']
        NationalIDNumber = request.form['NationalIDNumber']
        JobTitle = request.form['JobTitle']
        BirthDate = request.form['BirthDate']
        SalariedFlag = request.form['SalariedFlag']
        cursor.execute("INSERT INTO HumanResources.Employee (BusinessEntityID, NationalIDNumber, JobTitle, BirthDate, SalariedFlag) VALUES (?, ?, ?, ?, ?)",
                       (BusinessEntityID, NationalIDNumber, JobTitle, BirthDate, SalariedFlag))
        cnxn.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<int:id_data>', methods=['GET'])
def delete(id_data):
    flash("Record Has Been Deleted Successfully")
    cursor.execute("DELETE FROM HumanResources.Employee WHERE BusinessEntityID=?", (id_data,))
    cnxn.commit()
    return redirect(url_for('Index'))

@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        BusinessEntityID = request.form['BusinessEntityID']
        NationalIDNumber = request.form['NationalIDNumber']
        JobTitle = request.form['JobTitle']
        BirthDate = request.form['BirthDate']
        SalariedFlag = request.form['SalariedFlag']
        cursor.execute("""
           UPDATE HumanResources.Employee
           SET NationalIDNumber=?, JobTitle=?, BirthDate=?, SalariedFlag=?
           WHERE BusinessEntityID=?
        """, (NationalIDNumber, JobTitle, BirthDate, SalariedFlag, BusinessEntityID))
        flash("Data Updated Successfully")
        cnxn.commit()
        return redirect(url_for('Index'))

if __name__ == "__main__":
    app.run(debug=True)
