from knn_optuna_model import KNNOptunaModel
import pandas as pd

# Eğitim verisini yükle
df = pd.read_excel('tamam_son_2.xlsx')
model = KNNOptunaModel()
model.train(df)
model.save_model('knn_optuna_model.pkl')
print("Model başarıyla yeniden eğitildi ve kaydedildi.")