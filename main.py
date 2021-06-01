#############################################
# PARTE PER CLASSIFICATION #
#############################################

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sea
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import predictionio

def min_max_scale(X):
    return (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))

pd.set_option('display.max_columns', 100)

df = pd.read_csv('investments_VC.csv')

# Elimino le righe in eccesso dal file csv per avere solo i dati reali
df = df[:49438]

df.rename(columns = lambda s: s.strip(), inplace=True)

# Converto le date in datetime
format_date = ['founded_at','first_funding_at','last_funding_at']
for i in format_date:
  df[i] = pd.to_datetime(df[i], format = '%Y-%m-%d', errors = 'coerce')

# Creo le features per indicare l'età del primo funding e dell'ultimo funding
df['age_first_funding'] = (df['first_funding_at'] - df['founded_at']) / pd.Timedelta(days=365)
df['age_last_funding'] = (df['last_funding_at'] - df['founded_at']) / pd.Timedelta(days=365)

# Elimino le righe che hanno dei valori nulli per alcune features
df = df.drop(df[((df['founded_month'].isna()) | (df['founded_year'].isna()) |
            (df['market'].isna()) | (df['country_code'].isna()) | (df['funding_total_usd'].isna()) |
            (df['age_first_funding'].isna()))].index)

df = df.drop(['permalink', 'homepage_url', 'state_code', 'region', 'city', 'founded_at', 'first_funding_at',
              'funding_total_usd', 'last_funding_at', 'category_list'], axis = 1)

df = df.drop_duplicates()

# Tolgo tutte le righe che hanno status operating
df = df[(df['status'] != 'operating')]

df['status'] = df['status'].fillna("operating")

count = 0
i = 0
for el in df['status']:
    if count < 1400 and el == 'acquired':
        df['status'].iloc[i] = 'operating'
        count += 1
    i += 1

count = 0
i = 0
for el in df['status']:
    if count < 700 and el == 'closed':
        df['status'].iloc[i] = 'operating'
        count += 1
    i += 1

status_values = pd.unique(df['status'].values.ravel('K'))
dict_status = {}
i = 0
for val in status_values:
    dict_status[val] = i
    i += 1
df['status'] = df['status'].map(dict_status)

# Features che indica il totale degli investimenti
df['total_investment'] = df['seed'] + df['venture'] +df['equity_crowdfunding'] + df['undisclosed'] + df['convertible_note'] + df['debt_financing'] + df['angel'] + df['grant'] + df['private_equity'] + df['post_ipo_equity'] + df['post_ipo_debt'] + df['secondary_market'] + df['product_crowdfunding']

# Rimuovo gli outlier da total_investment
Q1 = df['total_investment'].quantile(0.25)
Q3 = df['total_investment'].quantile(0.75)
IQR = Q3 - Q1

fund_lower = (Q1 - 1.5 * IQR)
fund_upper = (Q3 + 1.5 * IQR)

df = df[(df['total_investment'] >= fund_lower ) & (df['total_investment'] <= fund_upper)]

# Seleziono solo i primi 20 mercati e gli altri li chiamo "Other"
top20_markets = df['market'].value_counts()[:20].keys().tolist()
df['market'] = df['market'].apply(lambda i: i if i in top20_markets else 'Other')

# Per le aziende che hanno ricevuto fondi prima della nascita metto la age_funding a 0 e non negativa
df.loc[df['age_first_funding'] < 0, 'age_first_funding'] = 0
df.loc[df['age_last_funding'] < 0, 'age_first_funding'] = 0

# Escludo le aziende vecchie
df = df[(df['founded_year'] >= 1995.0 )]

# Tolgo le feature poco correlate
df = df.drop(
    ['post_ipo_equity','post_ipo_debt','round_G','round_H','founded_year','founded_month','founded_quarter'], axis = 1)

# Tolgo le feature in eccesso per semplificare
features = ["name", "market", "status", "total_investment", "funding_rounds", "age_first_funding", "age_last_funding"]
df = df[features]

df['market'] = df['market'].apply(lambda s: s.strip())
market_values = pd.unique(df['market'].values.ravel('K'))
dict_market = {}
i = 0
for val in market_values:
    dict_market[val] = i
    i += 1

df['market'] = df['market'].map(dict_market)

# X e y sono i dati per il training e il target ('status') rispettivamente
features = ["market", "total_investment", "funding_rounds", "age_first_funding", "age_last_funding"]
X = df[features]
y = df['status']

# X2 = min_max_scale(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

n = 10
while n <= 200:
  model = RandomForestClassifier(n_estimators=n)
  model.fit(X_train, y_train)
  print('{} - train score: {:.3f} | test score: {:.3f}'.format(n,model.score(X_train,y_train),model.score(X_test,y_test)))
  n = n+10

model = RandomForestClassifier(n_estimators=10)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
zero = 0
uno = 0
due = 0
for s in y_pred:
    if s == 0.0:
        zero += 1
    elif s == 1.0:
        uno += 1
    else:
        due += 1
print(zero)
print(uno)
print(due)

file_data = open("data.txt", "w")
for i in range(len(X_train)):
    file_data.write(f"{y_train.iloc[i]}" + ",")
    for val in X_train.iloc[i]:
        file_data.write(f"{val}" + " ")
    file_data.write("\n")
file_data.close()

test_feat = {}
test_lab = {}

engine_client = predictionio.EngineClient(url="http://192.168.1.132:8000")
diversi = 0
uguali = 0
for i in range(len(X_test)):
    count = 0
    for val in X_test.iloc[i]:
        test_feat[X_test.iloc[i].index[count]] = val
        print(test_feat)
        count += 1
    y_pred = engine_client.send_query(test_feat)
    print(y_pred)
    if float(y_pred['status']) != float(y_test.iloc[i]):
        diversi += 1
    else:
        uguali += 1
print(uguali)
print(diversi)
print(uguali/(uguali+diversi))

zero = 0
uno = 0
due = 0
for i in range(len(X_test)):
    count = 0
    for val in X_test.iloc[i]:
        test_feat[X_test.iloc[i].index[count]] = val
        count += 1
    y_pred = engine_client.send_query(test_feat)
    print(y_pred)
    if float(y_pred['status']) == 0.0:
        zero += 1
    elif float(y_pred['status']) == 1.0:
        uno += 1
    else:
        due += 1
        
print(zero)
print(uno)
print(due)

#############################################
# PARTE PER RECOMMENDATION #
#############################################

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sea
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import predictionio

file_rec = open("datarec.txt", "w")