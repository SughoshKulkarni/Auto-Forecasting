# Auto-Forecasting
This is a web application that takes in an excel file with univariate time series data (Excel file with two columns: Date (Format:YYYY-MM-DD or YYYY-MM) and Values (historical sales, visitors on a website, gold prices, stock prices, etc.) and provides forecasts.<br><br>Auto-Forecasting works on buiding time series forecasting technique called [SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/ "Seasonal ARIMA") which stands for Seasonal Autoregressive Integrated Moving Average. 

<p align="center"><img src="https://lh3.googleusercontent.com/n2R5y3OvxDaQZpOKxwqr9JKMtECAa5eGQkSFO5RH-S2BBi05iuJYKsv8dkVmw39zSCWzqti9q9eHpDyrTpd3bsg8e60Q9CQXUud0m3NKxbmD8OopZMQNUNpRbBfYtU4F3ek_C0IfG9hkPcrGqvtLl_qNvZfPpTLyRXAjh_3PmLrPhV-EcAB7UTrHT7lmF3w-5iVgR0MPcy416ZU_tqTEWxEZod_-yzU8WtmazPQ6MbcFA4UCIC-ISexYFnXJhT359TKyusQL9FokLOKrPcFiPSiuDg1pqpc8Y_pRG8ifGlZ3stBibLrh_KI9Lj3uVWlsq8tA78_s2AtRZEIfbC06jOwI6HauKEPHxDoaOCGOkoUF5CU7jTs27sHE2WjmcSiQFXZq3VQaGovlpVLIl6tzreeZogPoBPKph97KJvxB8OJd5jPN1jGOQ3rZ4XvJ5w-BlIEwV4nr4WdixQS6fAIEH4avtQ744plgOVkY0OS1maVIlY0KCe2mxl33pwmafWJdXoaT8Keza7KUDRmdhC7SDXu9J8XHbjZc0N7k_5Lkthn5fEA2VjYrYcXMWDSmGDF2lShvNsaQeQPoIsejIhk3gZvVW1kmwhvUeaRmZSETUM1vzFNxdjQ8i8rEXcqwAURv-rgsBGlSRuOsYa5d96KqEBwJ4CgAB3-A3nkAzHlVpgRQi5jsazdFWp5tjLTXFWTT3n9YZg=s1005-w1005-h915-no?authuser=1" width="60%" height="70%"></p>

---

## Summary

Auto-Forecasting is a name which I have given to the web application that I have built.
For this project, we used Flask API to create the app and Python for modeling. The SARIMA model in this application can work with univariate time series. I was working on a building a forecasting model and always wanted to make the forecast easy and simple for people to get their forecasts in less number of steps and also ensuring less error. I took inspiration from an article by [Susan Li](https://www.linkedin.com/in/susanli/ "Susan Li") on towardsdatascience.com website and link is [here](https://towardsdatascience.com/@actsusanli "Time Series Analysis and Forecasting with Python").

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

You can check out the website [here](https://autoforecast.herokuapp.com/ "Auto-Forecast") or go to this website [https://autoforecast.herokuapp.com/](https://autoforecast.herokuapp.com/ "Auto-Forecast")

---
