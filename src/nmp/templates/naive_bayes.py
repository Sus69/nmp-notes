"""P7 - Naive Bayes Classifier."""

from sklearn.naive_bayes import GaussianNB
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

iris = load_iris()

X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.3, random_state=0
)

gnb = GaussianNB()
gnb.fit(X_train, y_train)

print(f'Naive Bayes Accuracy: {gnb.score(X_test, y_test) * 100:.2f}%')
