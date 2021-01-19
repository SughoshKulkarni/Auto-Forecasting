# Auto-Forecasting
This is a web application that takes in an excel file with univariate time series data (Excel file with two columns: Date (Format:YYYY-MM-DD or YYYY-MM) and Values (historical sales, visitors on a website, gold prices, stock prices, etc.) and provides forecasts.<br><br>Auto-Forecasting works on buiding time series forecasting technique called [SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/ "Seasonal ARIMA") which stands for Seasonal Autoregressive Integrated Moving Average. 

<p align="center"><img src="https://lh3.googleusercontent.com/3UvjGxJJajX36J9cQXjtNRD-4AvVfAd36tu8VBkBYgjj7N_NFfgnFDfJHP_Mrsc3YvNE-nuM8i-9AOePV3xqSYLfLTa-qnkvGn9LY8Ru3z3j8f_81kSX9f3YbFaMy9VCfvdlaDHgbg=w2400" width="60%" height="70%"></p>

---

## Summary

For this project, I used Flask API to create the app and Python for modeling. The SARIMA model in this application can work with univariate time series. I was working on a building a forecasting model and always wanted to make the forecast easy and simple for people to get their forecasts in less number of steps and also ensuring less error. I took inspiration from [Amazon Forecast](https://aws.amazon.com/forecast/ "Amazon Forecast") and an article by [Susan Li](https://www.linkedin.com/in/susanli/ "Susan Li") on towardsdatascience.com website and link for that article is [here](https://towardsdatascience.com/an-end-to-end-project-on-time-series-analysis-and-forecasting-with-python-4835e6bf050b "Time Series Analysis and Forecasting with Python").

## Functionality
The web app has an interface with three steps:
* Step 1:	Choose an excel file with your data (format allowed: .xls or .xlsx). Preferably the file should have two columns: Date and Values(historical sales, visitors on a website, gold prices, stock prices, etc.)
* Step 2:	Choose the confidence interval that you like. The options provided are 99% CI, 95% CI, and 90% CI.
* Step 3:	Choose the forecast length of your wish. The options provided range from 1 month to 12 months. (The forecasting model only provides monthly forecasting regardless of date format on input file as of now).

By clicking on forecast button, the the model reads the excel file and converts the date into YYYY-MM-DD format if not in that format already. If the data is in daily format, it will sum by grouping the values from the same month and takes an average of the month. The new data is run through a series of SARIMA models. The model with best [AIC](https://en.wikipedia.org/wiki/Akaike_information_criterion "Akaike information criterion") is chosen and will fit that model to the data, and generate the forecasts with the confidence intervals and display in a table format.
<br>
The model works better if the data is monthly data or daily data and a total of atleast 4-6 years of historical data.

## Languages and Technologies used
* Python
* Flask API
* HTML
* Heroku

You can check out the website [here](https://autoforecast.herokuapp.com/ "Auto-Forecasting") or go to this website [https://autoforecast.herokuapp.com/](https://autoforecast.herokuapp.com/ "Auto-Forecasting")

---
