import pandas as pd
pd.set_option('display.max_rows', 10)

### Creating, Reading and Writing Data
def creating_reading():
    def creating():
        """
        Creating
        --------

        A Pandas DataFrame is essentially a 2D table comprised of columns and rows
        and can be created using a key: value pair where the key is a columnn name
        and the value is a list of values
        """

        print("This DataFrame shows apples and bananas yields over the course of two years:\n")
        df = pd.DataFrame({"Apples": [31, 43],
                        "Bananas": [24, 31],})
        
        print(df)

        print("\nThe index optional parameter labels the rows, ideally with unique identifiers\n")

        df.index = ["Year 1", "Year 2"]

        print(df)

        print("""\na Series is all the values from a single column. In the first example,
    the Series of values under 'Apples' is [31, 43]
            
    These are created in a similar way to DataFrames but the data is a list
    rather than a dictionary""")
        
        s = pd.Series([1,2,3,4,5])

        print(s)

        print("""
    Again, the index names can be changed using a list
    """)

        s.index = ["Mon", "Tues", "Weds", "Thurs", "Fri"]  

        print(s)

    def reading():
        """
        Reading
        -------
        
        Reading in to a Pandas DataFrame is simple, just get the path of a csv file (or
        loads of other file types like Excel and JSON), and pass it in to pd.read_<filetype>()
        """

        print("""We'll use a dataset from Kaggle about wine reviews
    """)

        wine_reviews = pd.read_csv("Kaggle/data/winemag-data-130k-v2.csv", index_col=0)

        print(wine_reviews)

        print("\nand that's huge! big big big dataset! We don't need to see it all at one time\nso let's use df.head() to show the first 5")

        print(wine_reviews.head())

        print(f"We can see the shape of this DataFrame is {wine_reviews.shape} using `df.shape`\nwhich mean it has nearly 130 thousand records with 13 columns")

        print("\nFinally we need to be able to save a DataFrame to a file, and this is done\nusing `df.to_<filetype>(path)`\n")

    print(creating.__doc__)
    creating()
    print(reading.__doc__)
    reading()

### Indexing, Selecting and Assigning Data
wine_reviews = pd.read_csv("Kaggle/data/winemag-data-130k-v2.csv", index_col=0)
def index_select_assign():
    def access():
        """
        Access
        ------
        
        We need to be able to access the relevant data points in our dataset
        and this becomes apparent immediately. We can do this in Pandas
        using the native accessors like in dictionaries and objects
        """

        print("Here, I am accessing the country column using `df.country`\n")

        print(wine_reviews.country)

        print("\nAnd here with `df['country']`\n")

        print(wine_reviews["country"])

        print("\nAnd from this we can access anything in the Series like in a\nlist using [] notation:\n")

        print("wine_reviews[\"country\"][0] = " + wine_reviews["country"][0])

    def indexing():
        """
        Indexing
        --------
        
        Indexing is Selection via the row or column number rather than its name.
        This is done with the df.iloc property (not a method)
        """

        print("Using the same data as before, we can use `df.iloc` to get to our datapoints\niloc works on an index-first access scheme, which is different to usual")

        print(f"wine_reviews.iloc[0] returns the first row:\n{wine_reviews.iloc[0]}\n")
        print(f"While wine_reviews.iloc[:, 0] returns the first column:\n{wine_reviews.iloc[:, 0]}")

        print("\nKnowing this, we can pass slices and lists in as arguments to the iloc property:\n")

        print(f"For example, wine_reviews.iloc[[0, 10], :4] returns\n{wine_reviews.iloc[[0, 10], :4]}\n")

        print("\nWe can also index using labels with the df.loc property.\nThis works in a similar way but with a small caveat: the indexing is *inclusive*")
        print("By this I mean that if I were to do df.iloc[0:100] it would give me 0 to 99 (100 entries)\nbut with loc[0:100], it would give the 0 to 100!")
        print("This is helpful in the circumstance that you intend to slice your columns alphabetically\nIf your indexes are ['Apples', ..., 'Potatoes'] it could be difficult to\n index up to Potatoes' in a slice")
        print("Which would look more like df.loc[:, 'Apples':'Potatoet'] (since t comes after s) - not terribly convenient!")

    def conditional():
        """
        Conditional Selection
        ---------------------
        
        We can select the data we want based on conditions as well!
        This can be done very simply by using Boolean operations on both
        DataFrames and Series, but it can also be done using some masking functions
        """

        print("Let's check our wines to see if they were made in Italy or not using\n`df['country'] == 'Italy`:\n")

        print(wine_reviews["country"] == "Italy")

        print("This give us a Boolean Series that can be used to filter our data.\nWe can do this in combination with loc and iloc:\n")

        print(f"wine_reviews.loc[wine_reviews['country'] == 'Italy'] returns:\n{wine_reviews.loc[wine_reviews['country'] == 'Italy']}\nwhich is a DataFrame in its own right that can be accessed and manipulated too")

        print("\nWe can use any Boolean operation to mask our data, as complex as you like using normal Boolean operations\n")

        print("There are also functions that are provided for us that help with this filtering, including `.isin()`\nwhich can be passed a list to return a Boolean Series as before")

    print(access.__doc__)
    access()
    print(indexing.__doc__)
    indexing()
    print(conditional.__doc__)
    conditional()

### Summary Functions and Maps
def summaries_maps():
    def summaries():
        """
        Summary Functions
        -----
        Not an official term, but summary functions give you an overview of a specific DataFrame or Series
        Some of these will give you results based on the data in your df or Series such as mean and sum"""

        print("Pandas comes built in with a method that describes the data you have - `describe()`\nIt's a type-aware method whose output changes depending on the datatype")

        print(f"Country description:\n {wine_reviews.country.describe()}")
        print(f"Points description:\n {wine_reviews.points.describe()}")

        print("\nHere are some summative methods as well:\n")

        print(f"Points mean(): {wine_reviews.points.mean():.2f}")
        print(f"Points sum(): {wine_reviews.points.sum()}")
        print(f"Country value_counts(): {wine_reviews.country.value_counts()}")
        print(f"Country unique(): {wine_reviews.country.unique()}")

    def mapping():
        """
    Mapping
    ---
    Mapping is the act of creating new data based on a given dataset by applying a given function
    to the data in the set
    There are two mapping functions to know, one for Series objects and one for DataFrames
    namely `map` and `apply` respectively"""

    print("So, knowing this, let's map a Series object to another!")

    mean = wine_reviews.points.mean()

    def mapping_func(point):
        return point - mean
    
    print("""Let's use this function to map each point:
    
    def mapping_func(point):
        return point - mean
""")
    print(f"wine_reviews.points.map(mapping_func) returns:\n{wine_reviews.points.map(mapping_func)}")

    print(f"And we can do the same thing with a DataFrame, but\nwe get to choose which axis doesn't get modified")

    def applying_func(row):
        row.points -= mean
        return row
    
    print(f"""Like last time, we'll use a similar function to modify the points:
    
    def applying_func(row):
        row.points -= mean
        return row

wine_reviews.apply(applying_func, axis='columns') returns:
{wine_reviews.apply(applying_func, axis='columns')}""")
    
    print("\n" + " DEAR GOD that takes a while ".center(64, "#"))

    print("\nAnd since it takes so long, there are some workarounds using the built-in arithmetic operators\nlike + - < >. Pandas can tell what we mean based on context")
    print("So the above map method could just be rewritten as\nwine_reviews.points - mean\nand pandas would have known")

    print(summaries.__doc__)
    summaries()
    print(mapping.__doc__)
    mapping()

### Grouping and Sorting
def grouping_sorting():

    def groupwise_analysis():
        """
        Groupwise Analysis
        -

        Grouping our data allows us to look at fields as if they were categories
        We can use this to perform operations on values in these groups
        """

        print("Not really an easy one to describe without saying 'Grouping is grouping doy'\nbut anyway, we can analyse groups using the summary functions as before")

        print(f"\nFor example, wine_reviews.groupby('points').points.count() yields\n{wine_reviews.groupby('points').points.count()}")

        print("\nWhich actually happens to be the same as wine_reviews.points.value_counts()\nwhich is just a shortcut to the groupby method")

        print("\nSince the groupby() method returns a DataFrame-like object, we can manipulate it\nusing the apply() method!")

        print(f"""
    wine_reviews.groupby('winery').apply(lambda df: df.title.iloc[0])\nwill give us the first wine title in each winery:
    {wine_reviews.groupby('winery').apply(lambda df: df.title.iloc[0])}
    """)
        
        print("Another powerful aspect of grouping is aggregating. This allows us\nto pass multiple functions to apply to a Series or DataFrame:\n")

        print(f"""wine_reviews.groupby('country').price.agg([len, min, max]) will produce a DataFrame aggregating
    the price of each group with those three functions:
    {wine_reviews.groupby("country").price.agg([len, "min", "max"])}
    """)
        
        print("Next, we need to know about MultiIndexing, which is done\nby passing a list of columns\nto the groupby() method, resulting in a DataFrame\nwith multiple levels of indices")

        print("Let's say we group our data by country and province, we can do that with\nwine_reviews.groupby(['country', 'province']) and\nthen use different functions on it:")

        multi_index = wine_reviews.groupby(["country", "province"]).price.agg([len])

        print(f"\n{multi_index}\n")

        print("There are loads of use cases for MultiIndex DataFrames detailed here:\nhttps://pandas.pydata.org/pandas-docs/stable/advanced.html \nbut I won't go into it. A useful method is to turn it\nback into a regular indexed df using .reset_index()")

    def sorting():
        """
    Sorting
    -
    This is nice and simple, you can sort your DataFrame quite easily 
    using the .sort_values() method or .sort_index() method.
    These will arrange your data in either ascending or descending order
    based on a key (or more)"""

    multi_index = wine_reviews.groupby(["country", "province"]).price.agg([len])

    print("\nLet's sort our old MultiIndexed DataFrame by country using .sort_values():\n")

    print(f"multi_index.reset_index().sort_values(by='country') yields\n{multi_index.reset_index().sort_values(by='country')}\n")

    print("And we can also sort by multiple columns by passing a list, in order of sorting (passing 'country' and 'len'):\n")

    print(f"{multi_index.reset_index().sort_values(by=["country", "len"])}")

    print(groupwise_analysis.__doc__)
    groupwise_analysis()
    print(sorting.__doc__)
    sorting()

creating_reading()
index_select_assign()
summaries_maps()
grouping_sorting()
