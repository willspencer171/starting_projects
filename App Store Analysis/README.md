# App Store Analysis

## An investigation into data cleaning and analysis, following [Data Quest](https://app.dataquest.io/c/112/m/350/guided-project%3A-profitable-app-profiles-for-the-app-store-and-google-play-markets/)'s guided project

While loosely following the guided project, I've been finding ways to streamline and optimise the analysis of a large dataset ([Google Play](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv) and the [App Store](https://dq-content.s3.amazonaws.com/350/AppleStore.csv) - these links both download the data in .csv format)

Methods of increasing processing speeds of the large datasets include threading, and pickling (using the dill module) in order to bypass the need to reprocess data that has already been processed

### UPDATE: 10/05/23

Thanks to a bit of advice, I used the cprofile module to figure out where in my code I was being slowed down. Processing around 18000 lines of a CSV file turns out to be less intensive than I thought, and it was the dill module that was slowing things down the most

I thought I needed to use dill purely for the fact that I was using namedtuples that were created inside a function on runtime and couldn't be recreated without re-running the code. This was correct, but it was completely unnecessary. The performance distinction between a namedtuple and dictionary is nominal, if not favourable toward dictionaries.

Accessing data from a dictionary is easy. Easier than using a namedtuple's _fields property. And a dictionary has near constant average time complexity for CRUD operations. A no-brainer really.

Implementing this change, I was able to use pickle instead of dill, and have now sped up the program 6-fold (from ~12 seconds to ~2 seconds when processing a csv file). Needless to say, I don't need to overcomplicate things just to look impressive.

Also, threading was never used to speed things up, I just have it to do a fancy lil "Generating..." or "Serialising..." feature. Kind of moot now that the program is so much faster now
