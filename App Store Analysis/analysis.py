#! python3
# A python program that analyses and presents data from a dataset
# comprising apps from the App Store and Google Play Store
from functions import *


google_play = load_save_data(PATH_TO_GOOGLE_PLAY_STORE)
app_store = load_save_data(PATH_TO_APP_STORE)

# Took a while to load it all in in a nice format but we have it all ready now.
# Let's get into analysis
display_fields(google_play)
print()
google_genres = freq_table(google_play, "category")
display_freq_table(google_genres, is_freq_table=True, reverse=False)


def average(store: dict, field, number_field):
    # Unique items, no repeats
    fields = set([str(item[field]).title()
                 for item in store.values()])

    for _field in fields:
        # find average number of numerical field
        subset = {key: value for key, value in store.items() if str(
            value[field]).title() == _field}
        total = sum([value[number_field]
                    for value in subset.values()])
        avg = round(total / (len(subset) or 1), 2)
        print(_field, avg, sep=" : ")


average(google_play, "category", "price")
