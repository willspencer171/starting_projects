import pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from scipy.stats import boxcox
from mlxtend.preprocessing import minmax_scaling
from sklearn.linear_model import LinearRegression

"""Preparing a dataset for Regression analysis"""

bicycle_data = pd.read_csv('data/nyc-east-river-bicycle-counts.csv',
                           engine="pyarrow",
                           index_col=0)

# Convert all dtypes for consistency
bicycle_data = bicycle_data.convert_dtypes()

# Handle missing vals
print(f"Total missing vals: {bicycle_data.isnull().sum().sum()}")
# There are none actually, oh well

regression_types = ["Linear", "Logistic", "Poisson"]
print(f"""Our regression type choices:
\t{"\n\t".join(regression_types)}
""")

# Because we know our data types for Brooklyn Bridge through 
# to Total are integers, we can use Poisson regression
# Jumping in at the deep end damn.

# The temperature values and date values are continuous and would require
# linear regression

# let's plot total against date:
# regression requires date to be a number rather than a datetime
# object. We can convert them as below:
bicycle_data["Date_num"] = bicycle_data.Date.dt.day_of_year

# Normalise with Box-Cox method
bicycle_data["Date_num"] = boxcox(bicycle_data["Date_num"])[0].squeeze()

fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# So this uses the sklearn package to perform linear regression
# It's probably best in future to use the statsmodels library for this
X = bicycle_data[["Date_num"]]
y = bicycle_data["Total"]

model = LinearRegression()
model.fit(X, y)
preds = model.predict(X)

ax[0].scatter(x=bicycle_data['Date'], y=bicycle_data['Total'])
ax[0].plot(bicycle_data["Date"], preds, label="regression", color="red")

ax[0].set_title('Date vs Total (using sklearn)')

# Since our data is count data, it's more fitting to use
# Poisson regression which is not a model supported by sklearn

import statsmodels.api as sm

X = bicycle_data[['Date_num']]
X = sm.add_constant(X)

poisson_mod = sm.GLM(y, X, family=sm.families.Poisson()).fit()
print(poisson_mod.summary())

preds = poisson_mod.predict(X)
ci = poisson_mod.bse
print(ci)

ax[1].scatter(x=bicycle_data["Date"], y=bicycle_data["Total"])
#ax[1].plot(bicycle_data["Date"], preds, label='Poisson Prediction', color='red')
ax[1].fill_between(bicycle_data["Date"], preds+ci.iloc[0], preds-ci.iloc[0], color='skyblue')

ax[1].set_title('Date vs Total (Poisson Regression)')

plt.savefig('images/Linear and Poisson Regression.png')
