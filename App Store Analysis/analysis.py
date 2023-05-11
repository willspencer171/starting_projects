#! python3
# A python program that analyses and presents data from a dataset
# comprising apps from the App Store and Google Play Store
from functions import *
from matplotlib import pyplot

google_play = load_save_data(PATH_TO_GOOGLE_PLAY_STORE)
app_store = load_save_data(PATH_TO_APP_STORE)

# Took a while to load it all in in a nice format but we have it all ready now.
# Let's get into analysis
display_fields(app_store)
print()
google_genres = freq_table(google_play, "category")
#display_freq_table(google_genres, is_freq_table=True, reverse=False)

avg_rating_for_no_of_installs = average(google_play, "installs", "rating")
avg_rating_for_category = average(google_play, "category", "rating")

pyplot.bar(avg_rating_for_no_of_installs[0], avg_rating_for_no_of_installs[1], color = "red")
pyplot.show()
pyplot.bar(avg_rating_for_category[0], avg_rating_for_category[1], color = "red")
pyplot.show()
