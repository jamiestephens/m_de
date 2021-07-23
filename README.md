## Foreign Exchange Futures Dashboard

Accessing foreign exchange data that's easy to understand and consolidated in one place is a difficult task. This dashboard aims to simplify foreign exchange futures trading by providing graphs and tables with up to date information. The pipeline for this project starts with accessing this raw data from Investing.com via Selenium (web scraping) or yfinance, a Python library that pulls commonly needed data from Yahoo Finance. This data is then organized with dynamically named SQL tables, and placed into a singular SQL database using SqlAlchemy. To economize the space used within the database, minute-based foreign exchange data was discarded as it was not needed for longer-term analysis. The data is later pulled as needed and displayed using various HTML components within Dash, allowing for the manipulation of graph views to further understand the data trends. Callbacks were heavily utilized for this project in order to maximize user functionality. 


### Design
The dashboard was designed to first provide the user with an overview of the most recent activity seen by the most actively traded currencies (such as the Great British Pound, Euro, and Japanese Yen). The user is able to alter the data used by a heat map to the last 24 hrs worth of activity, to the last three days' worth, and to the last weeks' worth. Further down the page, the user can access a line graph showing a singular currency and its value over time as it compares to the USD and see its value change over a large time frame than the heatmap above. Futures contracts for each of the currencies listed is also available and appears in the grid to the right of the line graph. A final bar graph shows the difference in opening values for each of the futures being actively traded.


### Data
Approximately 104,000 datapoints were collected and used for this project. The bulk of the data came from the foreign exchange rate updates collected both on a minute and hour basis for separate graphs. Futures data (expiration dates, opening values, highs, and lows) was also collected, but this comprised a much smaller proportion of the total dataset.


### Algorithms
Very little was done for this project that was computationally intense. Percentage-based changes in foreign currency value were calculated for a map shown on the dashboard, but outside of that calculation the data was presented as is. The majority of the code had to do with either importing data via Selenium or formatting and updating the Dash dashboard. 

### Tools
* SQLAlchemy: data storage and retrieval
* Selenium: web scraping
* YFinance: provided some of the data used in the dashboard
* Plotly: data visualization
* Dash: dashboard creation and maintenance


### Communication
A brief Powerpoint with pipeline visuals was created for this project, as well as a dashboard that could be downloaded and demoed online. 

![image](https://user-images.githubusercontent.com/71529189/126757134-e968e970-0dfb-4c7c-87e1-b51f79224da7.png)
![image](https://user-images.githubusercontent.com/71529189/126757191-2b2b77bf-7c23-490d-a41a-a3eed90e6441.png)
