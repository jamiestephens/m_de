### Minimum Viable Product

My dashboard's main chart, a percentage change-based choropleth map showing the countries that correspond to various currencies, has been completed. The percentage changes correlate to the past 7 days of activity (meaning the difference between the first value seven days ago and the most recent value pulled from Yahoo Finance).
It's been succesfully shown with a Dash front-end, running locally, and it pulls data from a SQL database implemented to store Yahoo Finance data. The SQL database includes minute data from the previous 7 days and hourly data from the past year.

![image](https://user-images.githubusercontent.com/71529189/126466228-c25bd549-39af-47f7-9757-da0feffc7c97.png)

Next steps will be to implement time duration changes that the user can control, as well as a simple line graph that shows absolute value changes in the currency using the hourly data.
