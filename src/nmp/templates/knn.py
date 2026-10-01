"""P8 - K-Nearest Neighbors."""

from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix, classification_report, ConfusionMatrixDisplay
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

X, y = make_moons(n_samples=300, noise=0.3, random_state=42)
df = pd.DataFrame(X, columns=["Feature 1", "Feature 2"])
df['Target'] = y
plt.figure(figsize=(8,6))
sns.scatterplot(data=df, x = "Feature 1", y = "Feature 2", hue = "Target", palette = "Set1")
plt.title("2D Classification Data (make_moons)")
plt.grid(True)
plt.show()

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)

print(f'KNN Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%')
print('Cross-val scores:', cross_val_score(knn, X, y, cv=5))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))
print('Classification Report:')
print(classification_report(y_test, y_pred))
