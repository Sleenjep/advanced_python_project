import lightgbm as lgb
import pandas as pd

class RecommendationModel:
    def __init__(self, model_path: str):
        self.clf_model = lgb.Booster(model_file=model_path)

    def predict(self, features: pd.DataFrame, top_k: int = 10):
        preds = self.clf_model.predict(features)
        return preds