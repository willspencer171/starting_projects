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

Characters are encoded in computing. There are several different codecs (methods for encoding and decoding character data) such as ASCII, UTF-8, UTF-16, Unicode etc. If you try decoding bytes that were encoded using a different codec, you'd end up with what's called *mojibake* (literally character transformation in Japanese). This can look like this: æ–‡å—åŒ–ã?? or like ����������.

In Python, the standard text encoding is UTF-8. You can encode and decode to and from byte data using the `encode()` and `decode()` methods, respectively. If we try to decode using the wrong codec, however, we end up with errors since different character codecs have different ranges of characters. For example, ASCII only has 128 characters in its set. If you encode a Python string including a "€", and decode it using `bytes.decode("ascii")`, you'll throw an error since ASCII doesn't know how to translate the UTF-8 representation of a Euro back into a Euro character (or any, since € isn't in ASCII, thanks America).

A similar issue happens if you try to encode the string using a codec that doesn't have the character included. Using the € example again, if we encode using ASCII `byte_data = "€".encode("ascii", errors="replace")` and decode it using ASCII `byte_data.decode("ascii")` we'll get the unknown character �.

When reading in files with encoding issues, we run into problems. By default, Python will try to read files in using the UTF-8 encoding. However, if your data contains something that isn't UTF-8 encoded, it'll throw an error. One way around this is to try to read the data in with different codecs, using trial and error. This can take a while and isn't fun cos it throws a lot of errors.

Another way around it, more efficient, is to use the `charset_normalizer` module:

```python
import charset_normalizer

with open("path/to/file", "rb") as binarydata:
    # take the first 10000 bytes and guess the codec
    result = charset_normalizer.detect(binarydata.read(10000))

print(result)

>>> {'encoding': 'Windows-1252', 'language': 'English', 'confidence': 0.76}
```

This just tells us that we're 76% confident that the codec used in this file is "Windows-1252", and is written in English. At the end of the day, this module does just guess, so you can adjust the `.read()` range to make the guess better.

This is all from the tutorial, but it does go on to say about the `ftfy` module that is really useful for garbled Unicode codecs (UTF-x). Sometimes, the decoding can go wrong and you end up with actual Unicode-decoded strings like 'âœ” No problems'. This is weird, but is Unicode-correct. However, Unicode is apparently really good at letting *mojibake* tell us where it's gone wrong. As such, using the `ftfy.fix_text()` method will return this how it was supposed to look:

```python
print(ftfy.fix_text('âœ” No problems'))

>>> '✔ No problems'
```

There's a whole load of functionality that this one method can unscramble which is amazing, just have a look [here](https://ftfy.readthedocs.io/en/latest) for the documentation. `ftfy` developer Robyn Speer seems quite angry with people who use encoding guessers like `charset_normalizer` since that's what often causes issues in the first place. The majority of the Internet has been using UTF-8 since 2008 and there shouldn't be much reason to assume that a random string of bytes you found on the Internet is not in fact UTF-8. If it isn't, then that's when you might consider using a guesser.

## Inconsistent Data Entry

Fuzzy. Wuzzy.

This is a nice and simple one really. We all know how much it sucks when you're doing your data entry by hand, and you have to type Actual Things™ out. You're only human, you're prone to error. Maybe you've written "Democratic Republic of Congo" so many times you got bored and wrote "DRC" a few times, or "Democratic Reppublic of Congo". This is inconsistent data entry and can skew your data.

Now, we can go through all our data manually and change every instance of "DRC" to "Democratic Republic of Congo" OR, now hear me out, we can automate it!

In some cases, maybe you've got a space at the start or end of your data, or some other erroneous character. For this, you can simply perform the string operation on your columns like:

```python
dataframe['Erroneous Column'].str.strip()
dataframe['Erroneous Column'].str.strip(char="/")
```

or if you've got a few entries where the case changes throughout, you can set your data to be lowercase or title case:

```python
dataframe['Inconsistent Column'].str.lower()
dataframe['Inconsistent Column'].str.title()
```

Now, let's go back to our issue with the Democratic Republic of Congo. This doesn't fall into either category - it's just a misspelling of Republic! No amount of string methods will save you from this! But what we can do is use a package called `fuzzywuzzy`, which will perform an analysis on your string and find out how similar other entries in your data Series are. Then, you can use this package to amend your erroneous data to match the entry you actually want it to be:

```python
import fuzzywuzzy
from fuzzywuzzy import process

countries = dataframe['Countries'].unique()

# Find matches closest to the target string
matches = process.extract("democratic republic of congo", countries, 
                            limit=4, 
                            scorer=fuzzywuzzy.fuzz.token_sort_ratio)

>>> matches
[('democratic republic of congo': 100),
('democratic reppublic of congo': 78),
('democrtic rep of congo': 46),
('republic of ireland': 40)]
```

Let's create a little function that we can use to replace everything over a certain threshold:

```python
def replace_matches_in_column(df, column, target_string, threshold = 45):
  strings = df[column].unique()

  matches = process.extract(target_string, strings,
                            limit=threshold,
                            scorer=fuzzywuzzy.fuzz.token_sort_ratio)
  
  close_matches = [match[0] for match in matches 
                  if match[1] >= threshold]

  target_rows = df[column].isin(close_matches)

  df.loc[target_rows, column] = string_to_match
```

Now, this does replace all our closely incorrect instances of 'Democratic Republic of Congo', but it does leave out the issue of 'DRC'. This can't really be sorted since it is just too semantically distant from 'Democratic Republic of Congo' and needs to be done by hand really.
