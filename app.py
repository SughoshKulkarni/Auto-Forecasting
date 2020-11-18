import numpy as np
from flask import Flask, request, render_template, flash, redirect, url_for, send_file
import pandas as pd
import warnings
import itertools
warnings.filterwarnings("ignore")
import statsmodels.api as sm
from warnings import filterwarnings
from io import BytesIO
import matplotlib.pyplot as plt
import base64


app = Flask(__name__)
app.secret_key = "VaishSughosh%$1234"

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/about',methods=['GET', 'POST'])
def about():
    return render_template('about.html')

@app.route('/help',methods=['GET', 'POST'])
def helps():
    return render_template('help.html')

@app.route('/privacy',methods=['GET', 'POST'])
def privacy():
    return render_template('privacy.html')

@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    return render_template('feedback.html')

@app.route('/sitemap.xml', methods=['GET', 'POST'])
def sitemap():
    return render_template('sitemap.xml')

@app.errorhandler(500)
def request_internal_server_error(error):
    flash("Please ensure the Excel file has univariate time series data.", "error")
    return redirect(url_for("index"),500)

@app.route('/downloads', methods=['GET', 'POST'])
def downloads():
    path = 'sample/Sample_template_for_AutoForecasting.xlsx'
    return send_file(path, as_attachment=True)

@app.route('/forecast',methods=['GET', 'POST'])
def forecast():
    f = (request.files['file'])
    ci = float(request.form.get("CI",""))
    actual_ci = 100-(ci*100)
    month = int(request.form.get("months",""))
    
    try:
        excel_file = pd.read_excel(f, names=["Date", "Values"], header=0)
    except:
        excel_file = pd.read_csv(f, names=["Date", "Values"], header=0)
        
    try:
        pd.to_datetime(excel_file['Date'], format='%Y%m%d', errors='raise')
        print('date is in correct format correct format')
    except ValueError:
        excel_file['Date'] = pd.to_datetime(excel_file['Date'], errors='coerce')
        
    excel_file.sort_values(by=['Date'], inplace=True, ascending=True)
    
    abc = excel_file['Date'][1] - excel_file['Date'][0]
    abc = abc / np.timedelta64(1, 'D')
    print('The difference between consecutive dates is {}'.format(abc))
    if abc == 1.0 or abc == 0.0 or abc < 20.0:
        print('It is daily data')
        excel_file = excel_file.groupby('Date')['Values'].sum().reset_index()
        excel_file = excel_file.set_index('Date')
        y = excel_file['Values'].resample('MS').mean()
    elif abc == 31.0 or abc == 30.0:
        print('It is monthly data')
        excel_file = excel_file.set_index('Date')
        y = excel_file['Values'].resample('MS').mean()
      
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    
    filterwarnings('ignore')
    model_values = []
    for param in pdq:
        for param_seasonal in seasonal_pdq:
            mod = sm.tsa.statespace.SARIMAX(y,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)
            results = mod.fit()
            model_values.append([param, param_seasonal, results.aic])
            
    model_values_df = pd.DataFrame(model_values, columns = ['pdq','PDQs','AIC'])
    model_values_df[model_values_df['AIC'].idxmin():model_values_df['AIC'].idxmin()+1]
    AIC = round(min(model_values_df['AIC']),2)
    
    pdq_order = model_values_df[model_values_df['AIC'].idxmin():model_values_df['AIC'].idxmin()+1]['pdq'].iloc[0]
    PDQs_order = model_values_df[model_values_df['AIC'].idxmin():model_values_df['AIC'].idxmin()+1]['PDQs'].iloc[0]
    
    mod = sm.tsa.statespace.SARIMAX(y,
                                order=pdq_order,
                                seasonal_order=PDQs_order,
                                enforce_stationarity=False,
                                enforce_invertibility=False)
    results = mod.fit()
    
    fcast = results.get_forecast(month)
    Final_results_df = pd.DataFrame(fcast.conf_int(alpha=ci))
    Final_results_df['Forecasts'] = pd.DataFrame(fcast.predicted_mean)
    column_names = ["lower Values", "Forecasts", "upper Values"]
    Final_results_df= Final_results_df.reindex(columns=column_names)
    Final_results_df = Final_results_df.round(2)
    
    ######Preparation for Plots######
    img = BytesIO()
    img2 = BytesIO()
    pred_uc = results.get_forecast(steps=month)
    pred_ci = pred_uc.conf_int(alpha=ci)
    
    ######First Plot######
    ax = y.plot(label='observed', figsize=(14, 7))
    pred_uc.predicted_mean.plot(ax=ax, label='Forecast', title = 'Observed data and Forecasts')
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='g', alpha=.25)
    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    
    plt.legend()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode('utf8')
    
    ######Second Plot######
    forecasts = results.get_forecast(steps=month).predicted_mean
    ax = forecasts.plot(figsize=(14, 7), label='Forecasts', color='r',marker = '.', markersize = 15, title = 'Forecasts with {}% confidence interval'.format(actual_ci)) 
    ax.fill_between(pred_ci.index,
                    pred_ci.iloc[:, 0],
                    pred_ci.iloc[:, 1], color='g', alpha=.25)
    ax.set_xlabel('Months')
    ax.set_ylabel('Values')
        
    plt.legend()
    plt.savefig(img2, format='png')
    plt.close()
    img2.seek(0)
    plot_url2 = base64.b64encode(img2.getvalue()).decode('utf8')

    flash("The model details are: pdq order = {}, PDQs order = {} and AIC = {}".format(pdq_order,PDQs_order,AIC), "info")
    return render_template('output.html',  tables=[Final_results_df.to_html(classes='data')], titles=Final_results_df.columns.values, plot_url=plot_url, plot_url2=plot_url2)     # ,  final_list_plot=final_list_plot, legend=legend, datelist=date_list, Forecastlist=Forecast_list,

if __name__ == "__main__":
    app.run(debug=True)
