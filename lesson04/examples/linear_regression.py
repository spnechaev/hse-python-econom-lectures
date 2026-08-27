"""Fit a tiny real scikit-learn model and make one prediction."""

from sklearn.linear_model import LinearRegression


weeks = [[1], [2], [3], [4], [5]]
sales = [10, 12, 15, 17, 20]

model = LinearRegression()
model.fit(weeks, sales)

prediction = model.predict([[6]])[0]
print(f"week 6: {prediction:.1f}")
