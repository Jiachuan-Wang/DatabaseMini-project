Database Mini-project

Quick Start:
Run the Python code.
Type the date in user interface, in the form of Year-Month-Day, which should be greater than or equal to 2020-01-22 and less than or equal to today's date.
Then the user interface outputs the country with the largest number of confirmed cases till that day and the number of cases. An HTML file reflecting the COVID-19 situation of 8 key countries on that day will be generated in the same directory of Python code, containing a world map in the form of a heat map.

Introduction
The COVID-19 epidemic is closely related to everyone's life. Faced with the massive amount of data generated by various media every second, it is challenging for people to form a comprehensive understanding of it with human brains. Structured query language (SQL), however, can precisely meet this demand under the function of data definition. This mini-project focuses on the realization of two following functions: checking the country with the largest number of cumulative confirmed cases as of the specified date and visualizing the number of cases in some key countries, by using SQL, direct operation user interface, and heat map to realize information interaction and knowledge production.

Software Design
The software adopts a direct operation user interface and is made based on the pygame and pyecharts packages of Python programming language. Users can run the software via different applications, such as command prompt, then open a simple initial interface, which provides a line of prompts and a button that is designed to be clicked to enter the date specified by the user. Type in a regulated date (in the form of Year-Month-Day) and press Enter, then the interface will return the country with the largest number of cumulative confirmed cases till that day and the corresponding number. Besides, the software will generate an HTML file containing a world map, intuitively showing COVID-19 situation of the day in some key countries (China, US, United Kingdom, Italy, France, Germany, Spain, and Iran).

Database Design
The database files used in this project are countries-aggregated_csv.csv and key-countries-pivoted_csv.csv, downloaded from https://datahub.io/core/covid-19. According to the data features of these databases, table ONECOUNTRYCONFIRMED and KEYCOUNTRYCONFIRMED were created.
The tables in this project are satisfied amidst the first normal form (1NF), and the query efficiency is relatively high. The date entered by the user is used as the foreign key and a constraint, to participate in data querying in tables.

Acknowledgment
Thanks to Dr. Wanlu Liu for teaching SQL and the code about pycop2 and pygame. Thanks to some classmates in BMI1901, ZJE institute for their help.
