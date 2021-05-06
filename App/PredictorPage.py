import predictionio
import pandas as pd
import numpy as np
from DBManager.DB import Database

class Predictor:
    def __init__(self, url=None):
        self.db = Database()
        self.engine_client_class = predictionio.EngineClient(url="http://192.168.1.132:8000")
        self.engine_client_rec = predictionio.EngineClient(url="http://192.168.1.132:8001")
        self.event_client = predictionio.EventClient(access_key="6S_JIW0eesru9ea5NsTwO0dIBea-Q8Wp2tBX7Kh8EojF4KRme8JTnqpr5J0M1hTk", url="http://192.168.1.132:7070", threads=5, qsize=500) 

    def predict_company(self, name):
        features = self.db.read_company("*", "name", name)
        X = self.transform_features(features[0])
        result = self.engine_client_class.send_query(X)
        result_dict = {'operating': 0, 'closed': 1, 'acquired': 2}
        result_dict_inverted = {}
        for key in result_dict.keys():
            result_dict_inverted[result_dict[key]] = key
        return result_dict_inverted[result['status']]

    def transform_features(self, features):
        feature_names = ["name", "market", "total_investment", "funding_rounds", "founded_at", "first_funding_at", "last_funding_at"]
        elements = {}
        i = 0
        for f in feature_names:
            elements[f] = features[i]
            i += 1
        X = pd.DataFrame(elements, columns=["name", "market", "total_investment", "funding_rounds", "founded_at", "first_funding_at", "last_funding_at"], index = [0])
        X['age_first_funding'] = (X['first_funding_at'] - X['founded_at']) / pd.Timedelta(days=365)
        X['age_last_funding'] = (X['last_funding_at'] - X['founded_at']) / pd.Timedelta(days=365)
        X['market'] = X['market'].apply(lambda s: s.strip())
        dict_market = {'Other': 0, 'Software': 1, 'Curated Web': 2, 'Analytics': 3, 'E-Commerce': 4, 'Games': 5, 'Semiconductors': 6, 'Clean Technology': 7, 'Finance': 8, 'Mobile': 9, 'Biotechnology': 10, 'Search': 11, 'Advertising': 12, 'Security': 13, 'Health Care': 14, 'Enterprise Software': 15, 'Social Media': 16, 'Messaging': 17, 'Web Hosting': 18, 'Hardware + Software': 19, 'Education': 20}
        X['market'] = X['market'].map(dict_market)
        X = X[["market", "total_investment", "funding_rounds", "age_first_funding", "age_last_funding"]]
        features_dict = {}
        for i in range(len(X)):
            count = 0
            for val in X.iloc[i]:
                features_dict[X.iloc[i].index[count]] = val
                count += 1
        return features_dict

    def predict_consigliati(self, username):
        X = {"user": username, "num":10}
        result = self.engine_client_rec.send_query(X)
        if(len(result['itemScores']) == 0):
            return [{'item': "Nessun elemento consigliato"}]
        return result['itemScores']

    def insert_consigliato(self, username, name):
        self.event_client.create_event(event="interested", entity_type="user", entity_id=username, target_entity_type="company", target_entity_id=name)
    
    def insert_nonconsigliato(self, username, name):
        self.event_client.create_event(event="notinterested", entity_type="user", entity_id=username, target_entity_type="company", target_entity_id=name)