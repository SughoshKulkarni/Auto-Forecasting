import numpy as np
from flask import Flask, request, render_template, flash
import pandas as pd
import warnings
import itertools
warnings.filterwarnings("ignore")
import statsmodels.api as sm
from warnings import filterwarnings


app = Flask(__name__)
app.secret_key = "VaishSughosh%$1234"

@app.route('/',methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/forecast',methods=['GET', 'POST'])
def forecast():
    f = (request.files['file'])
    ci = float(request.form.get("CI",""))
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
    
    flash("The model details are:pdq order = {}, PDQs order = {} and AIC = {}".format(pdq_order,PDQs_order,AIC), "info")
    return render_template('index.html',  tables=[Final_results_df.to_html(classes='data')], titles=Final_results_df.columns.values)

if __name__ == "__main__":
    app.run(debug=True)