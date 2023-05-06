#! python3
# A python program that analyses and presents data from a dataset
# comprising apps from the App Store and Google Play Store
from functions import *

google_play = load_save_data(PATH_TO_GOOGLE_PLAY_STORE)
app_store = load_save_data(PATH_TO_APP_STORE)

# Took a while to load it all in in a nice format but we have it all ready now.
# Let's get into analysis
display_fields(app_store)
print()
apple_genres = freq_table(app_store, "prime_genre")
display_freq_table(apple_genres, is_freq_table=True)
