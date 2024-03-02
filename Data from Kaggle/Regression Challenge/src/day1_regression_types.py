import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import abline_plot

recipes = pd.read_csv("Regression Challenge/data/epicurious_recipes.csv", engine="pyarrow")

recipes = recipes[recipes.calories < 10000].dropna()

exog = sm.add_constant(recipes.calories, prepend=False)

glm_binom = sm.GLM(recipes.dessert, exog=exog, family=sm.families.Binomial())
res = glm_binom.fit()
res.summary()
res.mu

fig, ax = plt.subplots()

ax.scatter(recipes.calories, recipes.dessert)
line_fit = sm.OLS(recipes.dessert, sm.add_constant(recipes.calories)).fit()
frame = line_fit.get_prediction().summary_frame(alpha=0.05)
abline_plot(model_results=line_fit, ax=ax)

up_fit = sm.OLS(frame.mean_ci_upper, sm.add_constant(recipes.calories)).fit()
abline_plot(model_results=up_fit, ax=ax, color="r", alpha=0.5, linestyle=(0, (1, 2)))

down_fit = sm.OLS(frame.mean_ci_lower, sm.add_constant(recipes.calories)).fit()
abline_plot(model_results=down_fit, ax=ax, color="r", alpha=0.5, linestyle=(0, (1, 2)))

plt.show()
plt.savefig("Regression Challenge/images/linear_regression.png")