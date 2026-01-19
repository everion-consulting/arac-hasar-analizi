import os
import sys

def show_error_and_wait(msg):
    print("\n[HATA] {}".format(msg))
    input("\nPencereyi kapatmak için Enter'a basın...")
    sys.exit(1)

try:
    import uvicorn
    import fastapi
    import pandas
    import pydantic
    import joblib
    import sklearn
    import numpy
    import optuna
except ModuleNotFoundError as e:
    show_error_and_wait(f"Gerekli Python paketi eksik: {e}\nÇözüm: 'pip install -r requirements.txt' komutunu çalıştırın ve tekrar exe oluşturun.")

try:
    if getattr(sys, 'frozen', False):
        backend_path = os.path.join(sys._MEIPASS, "backend")
        os.chdir(backend_path)
        sys.path.insert(0, backend_path)
    else:
        backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
        os.chdir(backend_path)
        sys.path.insert(0, backend_path)

    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=False)
except Exception as e:
    show_error_and_wait(str(e))