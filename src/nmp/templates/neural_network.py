"""P4 - Feedforward Backprop NN."""

import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix

iris = load_iris()
X = iris.data
y = iris.target

y = (y != 0).astype(int).reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

def sigmoid(x):
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def sigmoid_derivative(x):
    return x * (1 - x)

np.random.seed(42)

input_size = X_train.shape[1]
hidden_size = 8
output_size = 1

w1 = np.random.randn(input_size, hidden_size) * 0.1
b1 = np.zeros((1, hidden_size))
w2 = np.random.randn(hidden_size, output_size) * 0.1
b2 = np.zeros((1, output_size))

learning_rate = 0.01
epochs = 5000

n = X_train.shape[0]

for epoch in range(epochs):
    z1 = np.dot(X_train, w1) + b1
    a1 = sigmoid(z1)
    z2 = np.dot(a1, w2) + b2
    a2 = sigmoid(z2)

    epsilon = 1e-8

    loss = -np.mean(
        y_train * np.log(a2 + epsilon) + (1 - y_train) * np.log(1 - a2)
    )

    dz2 = a2 - y_train

    dw2 = np.dot(a1.T, dz2) / n
    db2 = np.sum(dz2, axis=0, keepdims=True) / n

    da1 = np.dot(dz2, w2.T)
    dz1 = da1 * sigmoid_derivative(a1)

    dw1 = np.dot(X_train.T, dz1) / n
    db1 = np.sum(dz1, axis=0, keepdims=True) / n

    w2 -= learning_rate * dw2
    b2 -= learning_rate * db2

    w1 -= learning_rate * dw1
    b1 -= learning_rate * db1

    if epoch % 500 == 0:
        print(f"Epoch {epoch + 1}, Loss: {loss:.4f}")

z1_test = np.dot(X_test, w1) + b1
a1_test = sigmoid(z1_test)

z2_test = np.dot(a1_test, w2) + b2
a2_test = sigmoid(z2_test)

y_pred = (a2_test >= 0.5).astype(int)

accuracy = accuracy_score(y_test, y_pred)
cm = confusion_matrix(y_test, y_pred)

print(f"\nFinal Train Loss: {loss:.4f}")
print("Test Accuracy:", accuracy * 100, "%")
print("Confusion Matrix:")
print(cm)
