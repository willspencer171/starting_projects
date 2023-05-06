# App Store Analysis
## An investigation into data cleaning and analysis, following [Data Quest](https://app.dataquest.io/c/112/m/350/guided-project%3A-profitable-app-profiles-for-the-app-store-and-google-play-markets/)'s guided project

While loosely following the guided project, I've been finding ways to streamline and optimise the analysis of a large dataset ([Google Play](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv) and the [App Store](https://dq-content.s3.amazonaws.com/350/AppleStore.csv) - these links both download the data in .csv format)

Methods of increasing processing speeds of the large datasets include threading, and pickling (using the dill module) in order to bypass the need to reprocess data that has already been processed