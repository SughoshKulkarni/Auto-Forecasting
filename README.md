# Auto-Forecasting
This is a web application that takes in an excel file with univariate time series data (Excel file with two columns: Date (Format:YYYY-MM-DD or YYYY-MM) and Values (historical sales, visitors on a website, gold prices, stock prices, etc.) and provides forecasts.<br><br>Auto-Forecasting works on buiding time series forecasting technique called [SARIMA](https://machinelearningmastery.com/sarima-for-time-series-forecasting-in-python/ "Seasonal ARIMA") which stands for Seasonal Autoregressive Integrated Moving Average. 

<p align="center"><img src="https://lh3.googleusercontent.com/0ylOGXFt210NJbu5dqVcvvyRyridbfjfLXVyPeKWDD6Z_b-jPlu197hMLNAcUeUptfAECKwdyDo04O1lJUnHMComYM7URxrTwXC3awPxcdz1v-8voELCc8_J9GyJ_ZJk64eRKKbbycEgjb1bCQghq0-FiWSmCFfqZiO6g7htBPAaWFzduvrQJ0aMBYwnJ0DA6_vqNd-GtrogtM-5Irj3KnK1QeHxDhVJtAmB_Ybt4zcNyjKQMSRZRW6mxRZLPG73eNUEspIzhNBsDmljhLYeWR1tgBbDJe4u63sDerK4bm7QtN-SdHJCtXAzsODjP9zZKqBEjFRUmnxXuWrW24vgooyG6V1M9eRKot5N73FZwksgutR1WO8-wWykQMvR-J135S_1sFEhgGmvQkdARE0wT6-hVY8sZUkuKIbWhuHi6vYx5eUL3Xz1dCz9I9VMPBuXfCNZjtKKP2R1OGhroz-0sxrp1mG6mXC5IQPzrTOPv5kvZnoULDs-qP7aiEB8skKqz_fB8Vss2KBLZTF4KIWhr1mWI9fmL8w-kDzl0dHUi5dRN6zmw5Zk7yDXeWHoMo9ltwyl-wlBaUcUF3xpFCpNNDd6Y_BttQwIRymTsmNPcOHRzazgGYqN0ORQMIvT83rUuSU-QQyGQKd3HKNwj6v5gO9C_IzJveBXf5Eg4L1izSoRDlsejI2T_YT2tQuY=w1090-h927-no?authuser=1" width="80%" height="90%"></p>

**Summary**:
Auto-Forecasting is a name which I have given to the web application that I have built.
For this project, we used Flask API to create the app and Python for modeling. The SARIMA model in this application can work with univariate time series. I was working on a building a forecasting model and always wanted to make the forecast easy and simple for people to get their forecasts in less number of steps and also ensuring less error. I took inspiration from an article by [Susan Li](https://www.linkedin.com/in/susanli/ "Susan Li") on towardsdatascience.com website and link is [here](https://towardsdatascience.com/@actsusanli "Time Series Analysis and Forecasting with Python").


**Functionality**:
The web app has an interface with three steps:
* Step 1:	Choose an excel file with your data. Preferably the file should have two columns: Date and Values(historical sales, visitors on a website, gold prices, stock prices, etc.)
* Step 2:	Choose the confidence interval that you like. The options provided are 99% CI, 95% CI, and 90% CI.
* Step 3:	Choose the forecast length of your wish. The options provided range from 1 month to 12 months. (The forecasting model only provides monthly forecasting regardless of date format on input file as of now).

By clicking on forecast button, the the model reads the excel file and converts the date into YYYY-MM-DD format if not in that format already. If the data is in daily format, it will sum by grouping the values from the same month and takes an average of the month. The new data is run through a series of SARIMA models. The model with best [AIC](https://en.wikipedia.org/wiki/Akaike_information_criterion "Akaike information criterion") is chosen and will fit that model to the data, and generate the forecasts with the confidence intervals and display in a table format.

**Languages and Technologies used**:
* Python
* Flask API
* HTML
* Heroku

You can check out the website [here](https://autoforecast.herokuapp.com/ "Auto-Forecast") or go to this website [https://autoforecast.herokuapp.com/](https://autoforecast.herokuapp.com/ "Auto-Forecast")
