import pandas as pd
from os import path
import matplotlib.pyplot as plt
import numpy as np

# Turns out I don't even need 46 of these cos 
# there's only 4 states in the data :')
US_STATE_NAME_CONVERT = {value: key for key, value in {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}.items()}

REVIEW_TO_NUM = {np.nan: 0,
                 'Poor': 1,
                 'Fair': 2,
                 'Good': 3,
                 'Great': 4,
                 'Excellent': 5}

REVIEW_TO_NUM_REVERSE = {value: key for key, value in REVIEW_TO_NUM.items()}

data_file = path.join(path.dirname(__file__), path.join("Data", "book_reviews.csv"))

dataset = pd.read_csv(data_file)

# Added imputation function so the user can opt to either drop NA values,
# or modally impute them. I could match imputation to a method
def data_cleaning(dataset=dataset, imputation=False):
    _return = dataset.copy()
    IMPUTATION_METHODS = ["mode", "hotdeck", "random", "none"]
    if imputation:
        try:
            assert imputation in IMPUTATION_METHODS
        except AssertionError:
            raise KeyError(f"Valid Imputation methods are: {IMPUTATION_METHODS}")
    
    match imputation:
        case "mode":
            _return["review"] = _return["review"].fillna(_return["review"].mode().iloc[0])
            _return["state"] = _return["state"].fillna(_return["state"].mode().iloc[0])
        
        case "hotdeck":
            def hot_deck_impute(col):
                # Find the indices of missing values
                missing = col.isnull()

                # Find the indices of non-missing values
                non_missing = ~missing

                # Get the non-missing values
                values = col[non_missing]

                # For each missing value, find the nearest non-missing value
                for i in missing[missing].index:
                    j = np.abs(non_missing-i).argmin()
                    col[i] = values[j]

                return col
            
            _return = _return.apply(hot_deck_impute)

        case "random":
            _return = _return.apply(lambda x: x.fillna(np.random.choice(x.dropna())))

        case False:
            # otherwise, drop NAs
            _return = _return.dropna(how="any")
        
        case _:
            pass

    # This dict comprehension converts state postal codes to their full names
    # based on the constant map in line 5. This provides consistency when counting
    # found online at https://gist.github.com/rogerallen/1583593
    _return["state"] = {x: US_STATE_NAME_CONVERT[y] if len(y) == 2 else y
                        for x, y in _return["state"].items()}

    _return["review"] = {key: REVIEW_TO_NUM[value]
                        for key, value in _return["review"].items()}
    
    return _return

dataset = data_cleaning(imputation="none")
dataset_mode = data_cleaning(imputation="mode")
dataset_hotdeck = data_cleaning(imputation="hotdeck")
dataset_random = data_cleaning(imputation="random")
dataset_dropna = data_cleaning(imputation=False)

data_list = [(dataset, "The raw dataset with nothing changed"),
             (dataset_mode, "Imputed by filling NA with modal value"), 
             (dataset_hotdeck, "Imputed by filling NA with nearest non-missing value (hot-deck)"),
             (dataset_random, "Imputed by filling NA with random value"),
             (dataset_dropna, "Dropped NA values")]

dataset.query("state == 'FL' and price > 19.99")

# with this, we can see that dropping NA values is different from imputing them
# We can also  visualise the difference between imputation methods
for data in data_list:
    # count NA values in raw dataset
    if "The raw dataset" in data[1]:
        blanks_by_state = data[0].groupby("state")["review"].apply(
                                lambda x: pd.Series([REVIEW_TO_NUM_REVERSE[item] for item in x]).isna().sum())
        blank_revs_by_book = data[0].groupby("book")["review"].apply(
                                lambda x: pd.Series([REVIEW_TO_NUM_REVERSE[item] for item in x]).isna().sum())
        
        fig, axs = plt.subplots(2,1)
        
        print(data[0]["review"])

        axs[0].bar(blanks_by_state.index, blanks_by_state.values)
        axs[0].set_title("Number of blank reviews by state", color="r")

        axs[1].bar(blank_revs_by_book.index, blank_revs_by_book.values)
        axs[1].set_title("Number of blank reviews by book", color="r")

        root = plt.get_current_fig_manager().window
        root.state('zoomed')

        plt.suptitle("Number of omitted reviews by state or book", weight="bold")

        plt.show()
        continue

    # Apply .mode() to each review series from the groups (FL, TX, NY, CA)
    modal_review_by_state = data[0].groupby("state")["review"].apply(lambda x: x.mode()[0])

    # same for review by state but with mean
    mean_review_by_state = data[0].groupby("state")["review"].mean()

    # find sum of book prices - total value sold
    total_sales_by_book = data[0].groupby("book")["price"].sum()

    # get the number of items for each state
    state_counts = data[0]["state"].value_counts()

    # This mosaic is exactly what I needed, beautiful, succinct and tidy
    # Also works as a nested list if you wanted proper names
    mosaic = '''
ABC
DDD
'''
    fig, axs = plt.subplot_mosaic(mosaic)

    # Putting bar and pie charts onto a mosaic figure
    axs["A"].bar(modal_review_by_state.index, modal_review_by_state.values)
    axs["A"].set_yticks(list(range(0, 6)))
    axs["A"].set_yticklabels([""] + list(REVIEW_TO_NUM.keys())[1:])
    axs["A"].set_title("Modal review grouped by state", color="r")

    axs["B"].bar(mean_review_by_state.index, mean_review_by_state.values)
    axs["B"].set_yticks(list(range(0, 6)))
    axs["B"].set_yticklabels([""] + list(REVIEW_TO_NUM.keys())[1:])
    axs["B"].set_title("Mean review grouped by state", color="r")

    axs["C"].pie(state_counts, labels=state_counts.index)
    axs["C"].set_title("Number of books by state", color="r")

    axs["D"].bar(total_sales_by_book.index, total_sales_by_book.values)
    axs["D"].set_yticklabels([f"${item}" for item in range(0, 20001, round(20000/8))])
    axs["D"].tick_params(axis="both", labelrotation=15)
    axs["D"].set_title("Total sales of each book", color="r")

    fig.suptitle(data[1], y=1, weight="bold", size="16", stretch="expanded")
    
    root = plt.get_current_fig_manager().window
    root.state('zoomed')
   
    plt.show()
