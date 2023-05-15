# Book Store Sales

## A simple analysis of example books about the R scripting language

Written in Python, this dataset for beginners in R is simple and easy to understand. This is another example of simple data analysis from [Data Quest](app.dataquest.io/c/88/m/498/guided-project%3A-creating-an-efficient-data-analysis-workflow/) that uses a small dataset of book sales of 5 books in 4 different US states.

Using [pandas](https://pandas.pydata.org) to read a comma-separated values file, I subset and manipulate the data to show relationships between the four attributes of each book - name, state, review, and price - as well as identifying the quality of the data entries by counting missing entries.

I have also started learning how to use the [matplotlib](https://matplotlib.org) data visualisation library to illustrate these relationships graphically - this was good fun since I have experience with R's ggplot library, which has a very different feel to plotting than does Python. It's also worth pointing out that the project outlined by Data Quest is designed for user's of R.

>### Why is this any good?
>
>- Practice with matplotlib and pandas
>- Data cleaning
>   - Different imputation methods implemented and visualised:
>     - Modal imputation
>     - Hot-deck imputation
>     - Random imputation
>- Data visualisation
