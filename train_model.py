import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import pickle

# Cargar los datos de entrenamiento
data = pd.read_csv("training_data.csv")

# Vectorizar el texto
vectorizer = TfidfVectorizer(max_features=5000)  # Convertir texto en vectores numéricos
X = vectorizer.fit_transform(data["texto"])
y = data["categoria"]

# Dividir los datos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Entrenar el modelo de clasificación
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluar el modelo
y_pred = model.predict(X_test)
print("Reporte de Clasificación:")
print(classification_report(y_test, y_pred))

# Guardar el modelo entrenado y el vectorizador
with open("models/model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

with open("models/vectorizer.pkl", "wb") as vec_file:
    pickle.dump(vectorizer, vec_file)

print("Modelo y vectorizador guardados en la carpeta 'models'.")
