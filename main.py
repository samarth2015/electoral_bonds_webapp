Password = ""
from flask import Flask, render_template, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'efHJHD7SK7834#d$hjd(*&^%$#'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = Password
app.config['MYSQL_DB'] = 'bonds'

mysql = MySQL(app)


INDIVIDUAL_COLUMNS = ['Sr No.', 'Reference No (URN)', 'Journal Date', 'Date of Purchase', 'Date of Expiry', 'Name of the Purchaser', 'Prefix', 'Bond Number', 'Denominations', 'Issue Branch Code', 'Issue Teller', 'Status']

POLITICAL_PARTY_COLUMNS = ['Sr No.','Date of Encashment','Name of the Political Party','Account no. of Political Party','Prefix','Bond Number','Denominations','Pay Branch Code','Pay Teller']

MERGED_COLUMNS = INDIVIDUAL_COLUMNS + POLITICAL_PARTY_COLUMNS[1:4] + POLITICAL_PARTY_COLUMNS[6:]

@app.route('/', methods = ["POST", "GET"])
def main_page():
    if "unique_individual" in session:
        unique_individual = session['unique_individual']
        unique_party = session['unique_party']
        party_purchaser = session['party_purchaser']
        return render_template("index.html", name_of_purchaser = unique_individual, name_of_political_party = unique_party, pairs = party_purchaser, bond_filter = MERGED_COLUMNS)
    else:
        cursor = mysql.connection.cursor()
        cursor.execute("select distinct(`Name of the Purchaser`) from individual")
        unique_individual = cursor.fetchall()
        cursor.execute("select distinct(`Name of the Political Party`) from political_party")
        unique_party = cursor.fetchall()
        cursor.execute("select `Name of the Political Party`, `Name of the Purchaser` from individual inner join political_party on individual.`Bond Number` = political_party.`Bond Number` and substring(`Journal Date`, 8, 4) = substring(`Date of Encashment`, 8, 4)")
        party_purchaser = cursor.fetchall()
        # print(data3)
        party_purchaser = tuple(set(party_purchaser))
        # print(data3)
        cursor.close()
        session['unique_individual'] = unique_individual
        session['unique_party'] = unique_party
        session['party_purchaser'] = party_purchaser
        # print(data)
        return render_template("index.html", name_of_purchaser = unique_individual, name_of_political_party = unique_party, pairs = party_purchaser, bond_filter = MERGED_COLUMNS)



@app.route('/search_by_bond_number', methods = ["POST", "GET"])
def search_by_bond_number():
    if request.method == 'POST':
        bond_number = request.form['bond_number']
        type = request.form['type']
        cursor = mysql.connection.cursor()
        if type == 'default':
            cursor.execute("select * from individual where `Bond Number` = %s", (bond_number,))
            data = list(cursor.fetchall())
            cursor.execute("select * from political_party where `Bond Number` = %s", (bond_number,))
            if len(data) == 0:
                print("Not Found !!!")
                return main_page()
            data2 = list(cursor.fetchall()) 
            # print(data2)
            for i in range(len(data)):
                data[i] = data[i] + data2[i][1:4] + data2[i][6:]
                # print(len(data[i]))
            cursor.close()
            return render_template("bond_details.html", table_rows = data, table_header = MERGED_COLUMNS, show_chart = False)
        else:
            if type == "Prefix" or type == "Bond Number" or type == "Denominations":
                type = "individual" + ".`" + type + "`"
            else:
                type = "`" + type + "`"
            query = "select " + str(type) + " from individual inner join political_party on individual.`Bond Number` = political_party.`Bond Number` and substring(`Journal Date`, 8, 4) = substring(`Date of Encashment`, 8, 4)"
            cursor.execute(query + " where individual.`Bond Number` = %s", (bond_number,))
            data = list(cursor.fetchall())
            cursor.close()
            return render_template("bond_details.html", table_rows = data, table_header = [type], show_chart = False)

    else:
        return main_page()

    
@app.route('/go_to_home', methods = ["POST", "GET"])
def go_to_home():
    return main_page()


@app.route('/search_by_individual_per_year', methods = ["POST", "GET"])
def search_by_individual_per_year():
    if request.method == 'POST':
        individual = request.form.get('individual')
        # year = request.form.get('year')
        if individual == 'default':
            return main_page()

        # print(year, individual)
        cursor = mysql.connection.cursor()
        cursor.execute("select * from individual where `Name of the Purchaser` = %s", (individual,))
        data = list(cursor.fetchall())
        # print(data)
        y_axis = []
        bonds_per_year = []
        for i in range(2019, 2025):
            cursor.execute("select Denominations from individual where `Name of the Purchaser` = %s and `Journal Date` like %s and `Status` = 'Paid'", (individual, '%' + str(i)))
            data2 = list(cursor.fetchall())
            data2 = [int(i[0].replace(',', '')) for i in data2]
            bonds_per_year.append(len(data2))
            y_axis.append(sum(data2)/100000)
        # print(y_axis)
        cursor.close()
        # for i in range(len(data)):

        return render_template("bond_details.html", table_rows = data, table_header = INDIVIDUAL_COLUMNS, show_chart = True, x_axis = ['2019', '2020', '2021', '2022', '2023', '2024'], y_axis = y_axis, bonds_per_year = bonds_per_year)
    
@app.route('/search_by_political_party_per_year', methods = ["POST", "GET"])
def search_by_political_party_per_year():
    if request.method == "POST":
        political_party = request.form.get('political_party')
        if political_party == 'default':
            return main_page()
        cursor = mysql.connection.cursor()
        cursor.execute("select * from political_party where `Name of the Political Party` = %s", (political_party,))
        data = list(cursor.fetchall())
        y_axis = []
        bonds_per_year = []
        for i in range(2019, 2025):
            cursor.execute("select Denominations from political_party where `Name of the Political Party` = %s and `Date of Encashment` like %s", (political_party, '%' + str(i)))
            data2 = list(cursor.fetchall())
            data2 = [int(i[0].replace(',', '')) for i in data2]
            y_axis.append(sum(data2)/100000)
            bonds_per_year.append(len(data2))
        # print(y_axis)
        cursor.close()
        return render_template("bond_details.html", table_rows = data, table_header = POLITICAL_PARTY_COLUMNS, show_chart = True, x_axis = ['2019', '2020', '2021', '2022', '2023', '2024'], y_axis = y_axis, bonds_per_year = bonds_per_year) 
    
@app.route('/search_by_political_party_individual', methods = ["POST", "GET"])
def search_by_political_party_individual():
    if request.method == "POST":
        political_party = request.form.get('political_party')
        individual = request.form.get('individual')
        if (political_party == 'default' and individual == 'default') or political_party == 'default':
            return main_page()
        elif individual == 'default':
            cursor = mysql.connection.cursor()
            cursor.execute('select `Name of the Purchaser`, individual.Denominations from individual inner join political_party on individual.`Bond Number` = political_party.`Bond Number` and substring(`Journal Date`, 8, 4) = substring(`Date of Encashment`, 8, 4) where `Name of the Political Party` = %s and `Status` = "Paid"', (political_party,))
            data_political = cursor.fetchall()
            result = {}
            for key, value in data_political:
                if key in result:
                    result[key] += round(int(value.replace(',', ''))/100000, 2)
                else:
                    result[key] = round(int(value.replace(',', ''))/100000, 2)
            cursor.close()
            
            return render_template("bond_details.html", table_rows = tuple(result.items()), table_header = ['Name of the Purchaser', 'Total Amount in Lakhs'], show_chart_pie = True, show_chart = False, x_pie = tuple(result.keys()), y_pie = tuple(result.values()))
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('select individual.Denominations from individual inner join political_party on individual.`Bond Number` = political_party.`Bond Number` and substring(`Journal Date`, 8, 4) = substring(`Date of Encashment`, 8, 4) where `Name of the Purchaser` = %s and `Name of the Political Party` = %s and `Status` = "Paid"', (individual, political_party))
            data_political = cursor.fetchall()
            total = round(sum([int(i[0].replace(',', '')) for i in data_political])/100000, 2)
            # print(total)
            cursor.close()
            return render_template("bond_details.html", table_rows = [[individual, total]], table_header = ['Name of the Purchaser', 'Total Amount in Lakhs'], show_chart = False, show_chart_pie = False)
        
@app.route('/search_by_individual_political_party', methods = ["POST", "GET"])
def search_by_individual_political_party():
    if request.method == "POST":
        individual = request.form.get('individual')
        political_party = request.form.get('political_party')
        if (political_party == 'default' and individual == 'default') or individual == 'default':
            return main_page()
        elif political_party == 'default':
            cursor = mysql.connection.cursor()
            cursor.execute('select `Name of the Political Party`, political_party.Denominations from individual inner join political_party on individual.`Bond Number` = political_party.`Bond Number` and substring(`Journal Date`, 8, 4) = substring(`Date of Encashment`, 8, 4) where `Name of the Purchaser` = %s', (individual,))
            data_political = cursor.fetchall()
            result = {}
            for key, value in data_political:
                if key in result:
                    result[key] += round(int(value.replace(',', ''))/100000, 2)
                else:
                    result[key] = round(int(value.replace(',', ''))/100000, 2)
            cursor.close()
            
            return render_template("bond_details.html", table_rows = tuple(result.items()), table_header = ['Name of the Political Party', 'Total Amount in Lakhs'], show_chart = False, show_chart_pie = True, x_pie = tuple(result.keys()), y_pie = tuple(result.values()))
        else:
            cursor = mysql.connection.cursor()
            cursor.execute('select political_party.Denominations from individual inner join political_party on individual.`Bond Number` = political_party.`Bond Number` and substring(`Journal Date`, 8, 4) = substring(`Date of Encashment`, 8, 4) where `Name of the Purchaser` = %s and `Name of the Political Party` = %s', (individual, political_party))
            data_political = cursor.fetchall()
            total = round(sum([int(i[0].replace(',', '')) for i in data_political])/100000, 2)
            # print(total)
            cursor.close()
            return render_template("bond_details.html", table_rows = [[political_party, total]], table_header = ['Name of the Political Party', 'Total Amount in Lakhs'], show_chart = False, show_chart_pie = False)

@app.route('/get_pie', methods = ["POST", "GET"])
def get_pie():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        cursor.execute("select `Name of the Political Party`, Denominations from political_party")
        data = cursor.fetchall()
        result = {}
        for key, value in data:
            if key in result:
                result[key] += round(int(value.replace(',', ''))/100000, 2)
            else:
                result[key] = round(int(value.replace(',', ''))/100000, 2)
        cursor.close()
        return render_template("pie.html", x_axis = list(result.keys()), y_axis = list(result.values()))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port="80", debug = True)
    # app.run(debug = True) 
