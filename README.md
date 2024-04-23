# Electoral Bonds data analysis website

Welcome to the Electoral Analysis Website! This web application provides insights and analysis tools for electoral data.

## Table of Contents
1. Installation
2. Screenshots
3. Usage
4. Contributing

## Installation
1. Create a database named 'bonds' in SQL.
2. You are provided with two CSV files, 'individual.csv' and 'political_party.csv,' which contain the money paid by individuals or companies and political parties who encashed the money. Upload these files as tables in 'bonds' database.
3. Create a user in SQL using the command below.
CREATE USER 'testing'@'%' IDENTIFIED BY 'password'; 
GRANT ALL PRIVILEGES ON *.* TO 'testing'@'%' WITH GRANT OPTION;
4. Open terminal, and install flask and flask-mysqldb by following command.
pip install Flask Flask-MySQLdb
5. Open the main.py file, on the first line of code write your MYSQL password as string.
6. Run the main.py file, website will be live on localhost.
7. Visit the link which appears in the terminal to open the website.

## Screenshot
![Screenshot 2024-04-23 114522](https://github.com/samarth2015/electoral_bonds_website/assets/143396640/4df05d30-d67c-4406-bd77-5caf871f187a)
Home page of the website.

---

![Screenshot 2024-04-23 114600](https://github.com/samarth2015/electoral_bonds_website/assets/143396640/b23fa413-7784-47b8-9942-1e4fdde407d0)
Database shown after searching for bond number.

---

![Screenshot 2024-04-23 114721](https://github.com/samarth2015/electoral_bonds_website/assets/143396640/48eccc79-7d4d-4e69-823c-16e3f0f602b3)
Table showing the total number of bonds and total value of bonds per year.

---

![Screenshot 2024-04-23 114737](https://github.com/samarth2015/electoral_bonds_website/assets/143396640/cc0b42a5-ffae-4631-879a-c51a406b1336)
Bar chart of the total value of bonds per year.

---

![Screenshot 2024-04-23 114857](https://github.com/samarth2015/electoral_bonds_website/assets/143396640/61e0a0d9-9f9c-43c9-8b5a-47ead410385e)
Pie chart showing the donors to a political party.

## Usage
1. The first search bar is to search for a particular bond number.
   a. If you leave the next filter empty, the website will show you the total data.
   b. If you add a particular filter, you get only the data you want.
2. In second dropdown, you can find the data of a particular individual or a company.
   a. This data include the number of bonds and total money given each year.
   b. A bar chart showing the total amount for comparision.
   c. The bar char also have a download button to save the chart as .png locally.
3. In third dropdown, you can find the data of the particular political party.
   a. This data include the number of bonds and total money encashed each year.
   b. A bar chart showing the total amount for comparision.
   c. The bar char also have a download button to save the chart as .png locally.
4. In the fourth part, you will first select the political party and then choose the individual to get the data about how much money that individual donated to the party. You can choose not to select the individual, and then you will get all the data. Also, there is a pie chart showing the comparison of money.
5. In the fifth part, firstly you will select the individual or political party and then select the political party to get the data about how much money that political party encashed from the individual. You can choose not to select the political party, and then you will get the whole data. Also, there is a pie chart showing the comparison of money.
6. Here is a button for 'Get Pie' that shows the pie chart of the total money the political parties took in the total data provided.
7. Each result page has a robust search bar, from which you can search for all the matches in the results obtained from the above searches.
8. Also there is a 'Go to home' button to navigate smoothly through the website.

## Contributing
Contributions are welcome! If you'd like to contribute to the Electoral Analysis Website, please follow these steps:

1. Fork the repository
2. Create a new branch (git checkout -b feature/your-feature)
3. Make your changes
4. Commit your changes (git commit -am 'Add some feature')
5. Push to the branch (git push origin feature/your-feature)
6. Create a pull request
   (add actual values in place of your-feature, etc.)

## Author
[Samarth Sonawane](https://github.com/samarth2015)

