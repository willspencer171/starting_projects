# Data Cleaning

> Whenever you have data, there is every chance that it will need cleaning and standardising before usage. There are a few things we need to know and think about before we can actually use a raw dataset.

I cover 5 important data cleaning problems here:

- Handling Missing Values [↓](#handling-missing-values)
- Scaling and Normalisation [↓](#scaling-and-normalisation)
- Parsing Dates [↓](#parsing-dates)
- Character Encoding [↓](#character-encoding)
- Inconsistent Data Entry [↓](#inconsistent-data-entry)

This readme occasionally references the [python file](data_cleaning.py) of the same name in this repository.

## Handling Missing Values

The first and probably foremost problem to look at is what happens if we have missing data. We can have missing data in our set for a number of reasons - primarily the data doesn't exist (like a postcode suffix ???) or it just wasn't entered.

We can use `pandas` to do pretty much all of this which is nice! Let's load in an example from [Kaggle](https://www.kaggle.com/code/alexisbcook/handling-missing-values/data):

```python
import pandas as pd
import numpy as np

nfl_data = pd.read_csv('Kaggle/data/NFL Play by Play 2009-2016 (v3).csv')
```

Great! This will be our dataset now

We can see how many missing values (represented with np.nan) there are in our data, and as a percentage:

```python
# Counts for each column
missing_values_count = nfl_data.isnull().sum()

# As a percentage
total = np.product(nfl_data.shape) # nifty, will give you the total number of data points
percent_missing = missing_values_count.sum() / total * 100
```

```shell
>>> percent_missing
>>> 24.87214126835169
```

So, what can we do with this information? We can try to fill missing values, or drop them

### Dealing with missing values

When faced with a lot of missing data, we need to look at why it might be missing. 

Sometimes we just don't want to deal with missing values or we don't have a good reason as to why they're missing. In this instance, we just drop missing values using `dropna()`:

```python
nfl_data.dropna() # drops all rows with any missing data
nfl_data.dropna(axis=1) # drops all columns with missing values
```

Sometimes the data just doesn't exist (like in the `PenalizedTeam` column, where there just aren't any penalties), or missing (maybe something wasn't recorded). We use the `fillna()` method to deal with this:

```python
nfl_data.bfill() # fills data with the data that follows it in the next row, if it can
# Good for data that follows a logical order
nfl_data.fillna(0) # fills all remaining missing data with a 0
```

This data filling option is called imputation, and there are a whole bunch of other useful tricks to fill missing values. `scikit-learn` has a `SimpleImputer` class that will fill values using the average of the row or column:

```python
from sklearn.impute import SimpleImputer

imputer = SimpleImputer()

# This will apply an average to each column to get missing values
nfl_data = pd.DataFrame(imputer.fit_transform(nfl_data))
```

In machine learning models, imputation with a slight extension to say whether a value was imputed or not performs better than just imputation as well.

## Scaling and Normalisation

Scaling and Normalisation are two different processes but seem similar at first:

- *Scaling* is about changing the *range* of your data
- *Normalisation* is about changing the *shape* or *distribution* of your data

This is an interesting one with uses outside what I had thought about.

### Scaling

So basically, scaling allows you to transform your data to fit within a given range. In doing so, you're ensuring that changes in data points of different series are equivalent - a change of '1' in one measurement is related to a change of '1' in another. For example, the US dollar and the Japanese Yen are not the same unit, but can be scaled to be equivalent through a relationship (roughly 1 USD to 100 Yen). Sophisticated scaling algorithms like Suuport Vector Machine ([SVMs](https://en.wikipedia.org/wiki/Support_vector_machine)) and k-Nearest Neighbours ([KNN](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm)) relate the differences between scales to match our intuitions.

So this works great for units of similar measurements (USD and JPY are both currencies), but how can we do the same for unrelated scales like height and weight? These two are not equivable but we can still use these algorithms to scale them to the same range.

Let's look at an example with made up numbers:

```python
from mlxtend.preprocessing import minmax_scaling
original_data = np.random.exponential(1000)

scaled_data = minmax_scaling(original_data, columns=[0]) # columns is a list of column names, or indexes
```

<p align="center">
    <img width="95%" src="images/Data Scaling.png" alt="Original vs Scaled Data">
</p>

See how the scale at the bottom is now 0 - 1 rather than 0 - 8 ish

### Normalisation

Normalisation is a more radical transformation of your data. Its main purpose is to distribute your data points to look like the normal bell curve (AKA Gaussian curve). This is typically used for when you're using machine learning techniques that assume a normal distribution of your data. (If your technique has Gaussian anywhere in the name, it probably needs normalised data)

So, let's have a quick look at what it'll do to your data using the [Box-Cox](https://en.wikipedia.org/wiki/Power_transform#Box–Cox_transformation) transformation:

```python
from scipy import stats

original_data = np.random.exponential(size=1000)
normalised_data = stats.boxcox(original_data)
```

<p align="center">
    <img width="95%" src="images/Data Normalisation.png" alt="Original vs Normalised Data">
</p>

I practice a bit of normalisation and scaling in the python file associated with this readme. Kaggle says to practice with respect to preparing for a regression analysis, so I'll be talking a bit about regression types there.

### Regression Analysis

<details><summary>Click here to see about this</summary>

Regression is something I've gone over more during my degree using R. I now want to get a proper good read into it since I only understood it at surface level before.

Regression is a measurement of the strength and direction of the relationship between the response (y, dependent or output) and explanatory (x, independent or input) variables - lots of names for each! There is typically one of each but it's possible to use regression to measure the effects of multiple explanatory variables (and other stats tests to go with for uni- bi- and multivariate datasets). Regression allows you to create a predictive model for novel data.

The Kaggle challenge is written using R, but I'm going to try and replicate using Python

#### What types of Regression are there?

There are 3 main types of regression analysis and choosing one depends on what type of data you have:

- Continuous data - linear regression
  - Uses the Gaussian family of regression functions
- Categorical data - logistic regression
  - Uses the binomial family of regression functions
- Count data - Poisson regression
  - Uses the Poisson family of regression functions

So, I've gone a little crazy and created some figures based on the total counts of bikes. At first, I thought I'd just plot date against count. You can plot a datetime object against count on a scatter graph, but you can't do linear regression on a datetime object. This needed to be converted to a number like so:

```python
bicycle_data["Date_num"] = bicycle_data.Date.dt.day_of_year
```

This way, we have numbers that we can use in regression, and that can be mapped back to the datetimes on the plot.

At first, I thought I'd do a linear regression to see if it could actually work. It does, but the thing about linear regression is that it assumes your count data is normally distributed (which we do fit it to be) and is continuous (which it isn't). This doesn't make a whole world of difference in the end but could cause issues down the line if I'm not aware of the difference.

The problem I had with using `sklearn` was not that it wouldn't do the linear regression (it did it fine using the LinearRegression model), but that it doesn't return confidence intervals for error margins (since `sklearn` is not a statistics package, but is a machine learning package).

The solution to this is to use a statistical package like `statsmodels`. This does return confidence intervals (shown in blue below) which can be filled. In the image below, I used a Poisson regression method (using the generalised linear model - GLM) which also produced a curve in the predictions. This could mean that either I didn't prep my data properly, or the data would be better represented using a non-linear model such as a generalised additive model (GAM) which is provided in the `pygam` package (not going over that here)

<p align="center">
  <img width=90% alt="Linear regression vs Poisson regression" src='images/Linear and Poisson Regression.png'>
</p>

I did try going into other models that are suited for time series like EST, but this got out of scope very quickly.

</details>

## Parsing Dates

I'm moving on from Scaling and Normalisation, but it was very interesting to look into, if only briefly.

Here, I'm looking at how to parse dates from object dtypes using the `pandas.to_datetime()` method.

Let's say we have a load of dates in our data, which often happens when measuring things over a period of time. In data entry, unless you're using something that can specify the format of a cell (like in Excel), you're entering strings, which are just objects in `numpy` terms. These are parsed using `pd.to_datetime()`:

```python
df.parsed_dates = pd.to_datetime(df.dates, format="%m/%d/%y")
```

The format specified above tells the method that the string we're passing looks like a date with the format mm/dd/yy. The formats for this are specified using the [strftime directive](https://strftime.org).

But what if your date entry is weird and wacky? There is a solution, and that is to let `pandas` guess using the `infer_datetime_format=True` term. This doesn't always do the job correctly if you're too creative with formatting, and is typically slower, but is effective if you're not sure about the format.

From here, we can select attributes of the datetime object through `<datetime_series>.dt.<attribute>`. For example, to select the day of a date object - `df.parsed_dates.dt.day` - or the month number - `df.parsed_dates.dt.month`.

In the tutorial exercise, I was given a dataset of volcanoes and their lastt eruption dates. The Last Known Eruption columns was full of string data stating either 'Unknown', '\<year\> CE' or '\<year\> BCE'. In order to clean this up for processing like actual numbers (not dates objects since it's just a year), I needed to drop rows that contained 'Unknown' (analogous to na, really), and convert BCE-containing dates to negative numbers and CE dates to positive integers.

I created a little function that returns the integer value of the year, with the sign dependent on the presence of BCE or CE:

```python
CE_dict = {"CE": 1,
          "BCE": -1}
def strip_ce(year):
    year, sign = year.split(" ")
    year = int(year) * CE_dict[sign]
    return year
```

## Character Encoding

## Inconsistent Data Entry
