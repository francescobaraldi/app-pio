import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sea
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import predictionio
from DB import Database

#############################################
# PARTE PER CLASSIFICATION #
#############################################

pd.set_option('display.max_columns', 100)

df = pd.read_csv('investments_VC.csv')

# Elimino le righe in eccesso dal file csv per avere solo i dati reali
df = df[:49438]

df.rename(columns = lambda s: s.strip(), inplace=True)

# Converto le date in datetime
format_date = ['founded_at','first_funding_at','last_funding_at']
for i in format_date:
  df[i] = pd.to_datetime(df[i], format = '%Y-%m-%d', errors = 'coerce')


# Elimino le righe che hanno dei valori nulli per alcune features
df = df.drop(df[((df['founded_month'].isna()) | (df['founded_year'].isna()) |
            (df['market'].isna()) | (df['country_code'].isna()) | (df['funding_total_usd'].isna()) |
            (df['age_first_funding'].isna()))].index)

df = df.drop(['permalink', 'homepage_url', 'state_code', 'region', 'city',
              'funding_total_usd', 'category_list'], axis = 1)

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


# Escludo le aziende vecchie
df = df[(df['founded_year'] >= 1995.0 )]

df['market'] = df['market'].apply(lambda s: s.strip())

# X e y sono i dati per il training e il target ('status') rispettivamente
features = ["name", "market", "total_investment", "funding_rounds", "founded_at", "first_funding_at", "last_funding_at"]
X = df[features]

X['name'] = X['name'].fillna("Sconosciuto")
X['first_funding_at'] = X['first_funding_at'].fillna(X.loc[37313][6])

db = Database()

for i in range(1, len(X)):
    params = []
    for j in range(len(X.iloc[i])):
        if(j==2 or j==3):
            params.append(X.iloc[i][j].item())
        elif(j==4 or j==5 or j==6):
            params.append(X.iloc[i][j].date())
        else:
            params.append(X.iloc[i][j])
    db.insert_company(*params)




#############################################
# PARTE PER RECOEMMENDATION #
#############################################

db.cursor.execute("SELECT name FROM companies")
companies = db.cursor.fetchall()
users = ["francesco", "francesco_baraldi", "filippo", "gloria"]

count = 0
for i in range(6, len(companies)):
    if i % 11 == 0 and count <= 100:
        db.insert_interested("gloria", companies[i][0])
        count += 1

francesco = db.read_interested('*', "username", "francesco")
francesco_baraldi = db.read_interested('*', "username", "francesco_baraldi")
filippo = db.read_interested('*', "username", "filippo")
gloria = db.read_interested('*', "username", "gloria")

file_data = open("data_rec.txt", "w")
data = [francesco, francesco_baraldi, filippo, gloria]
for d in data:
    for i in range(len(d)):
        file_data.write(d[i][0] + "::" + d[i][1] + "::" + "interested\n")
file_data.close()