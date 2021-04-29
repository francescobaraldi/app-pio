import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sea
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import predictionio
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier

def min_max_scale(X):
    return (X - np.min(X, axis=0)) / (np.max(X, axis=0) - np.min(X, axis=0))

pd.set_option('display.max_columns', 100)

df = pd.read_csv('investments_VC.csv')

# Elimino le righe in eccesso dal file csv per avere solo i dati reali
df = df[:49438]

df.rename(columns = lambda s: s.strip(), inplace=True)
df['market'] = df['market'].fillna("")
df['market'] = df['market'].apply(lambda s: s.strip())
df['market'] = df['market'].apply(lambda s: s.replace('-', '_'))
df['market'] = df['market'].apply(lambda s: s.replace(' ', '_'))
df['market'] = df['market'].apply(lambda s: s.replace('/', '_'))
df['market'] = df['market'].apply(lambda s: s.replace('&', 'and'))
df['market'] = df['market'].apply(lambda s: s.replace('+', 'and'))
df['market'] = df['market'].apply(lambda s: s.replace('.0', ''))

df['funding_total_usd'] = df['funding_total_usd'].apply(lambda s: s.strip())
df['funding_total_usd'] = df['funding_total_usd'].apply(lambda s: s.replace(',',''))
df['funding_total_usd'] = df['funding_total_usd'].apply(lambda s: s.replace('-','0'))
df['funding_total_usd'] = df['funding_total_usd'].apply(lambda s: float(s))

df['country_code'] = df['country_code'].fillna(method='ffill')

df['founded_year'] = df['founded_year'].fillna(method='ffill')

df['status'] = df['status'].fillna("acquired")

count = 0
i = 0
for el in df['status']:
    if i % 10 == 0:
        random = True
    if count < 7000 and random and el == 'operating':
        df['status'][i] = 'closed'
        count += 1
        random = False
    i += 1

count = 0
i = 0
for el in df['status']:
    if i % 10 == 0:
        random = True
    if count < 5000 and random and el == 'operating':
        df['status'][i] = 'acquired'
        count += 1
        random = False
    i += 1

# corr_matrix = df.corr()
# sea.heatmap(corr_matrix, annot=True)
# plt.show()

# Lista delle features che mi interessano per il training
features = ["market", "funding_total_usd", "country_code",
            "funding_rounds", "founded_year"]

# X e y sono i dati per il training e il target ('status') rispettivamente
X = df[features]
y = df['status']
# print(X)
# print(y)

market_values = pd.unique(X['market'].values.ravel('K'))
country_code_values = pd.unique(X['country_code'].values.ravel('K'))
status_values = pd.unique(y.values.ravel('K'))

dict_market = {}
dict_country = {}
dict_status = {}

i = 0
for val in market_values:
    dict_market[val] = i
    i += 1

i = 0
for val in country_code_values:
    dict_country[val] = i
    i += 1

i = 0
for val in status_values:
    dict_status[val] = i
    i += 1

X['market'] = X['market'].map(dict_market)
X['country_code'] = X['country_code'].map(dict_country)

y = y.map(dict_status)

# X['funding_total_usd'] = X['funding_total_usd'].apply(lambda i: int(i))
# X['funding_rounds'] = X['funding_rounds'].apply(lambda i: int(i))
# X['founded_year'] = X['founded_year'].apply(lambda i: int(i))

X2 = min_max_scale(X)

X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.2)

# clf = RandomForestClassifier()
# clf.fit(X_train[:500], y_train[:500])
# y_pred = clf.predict(X_test)

# d = 0
# u = 0
# for i in range(len(y_test)):
#     if y_pred[0] != y_test.iloc[i]:
#         d += 1
#     else:
#         u += 1
# print(d)
# print(u)

file_data = open("data.txt", "w")
for i in range(500):
    file_data.write(f"{y_train.iloc[i]}" + ",")
    for val in X_train.iloc[i]:
        file_data.write(f"{val}" + " ")
    file_data.write("\n")
file_data.close()

test_feat = {}
test_lab = {}

engine_client = predictionio.EngineClient(url="http://192.168.15.124:8000")
diversi = 0
uguali = 0
for i in range(len(X_test)):
    count = 0
    for val in X_test.iloc[i]:
        test_feat[X_test.iloc[i].index[count]] = val
        count += 1
    y_pred = engine_client.send_query(test_feat)
    if float(y_pred['status']) != float(y_test.iloc[i]):
        diversi += 1
    else:
        uguali += 1
print(uguali)
print(diversi)