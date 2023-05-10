import cProfile, pstats
from functions import *

profile = os.path.join(DATA_FOLDER, "profile")

# Helps me to identify what was slowing down my code
cProfile.run("load_save_data(PATH_TO_GOOGLE_PLAY_STORE)", profile)
cProfile.run("from analysis import *", sort="cumulative")

p = pstats.Stats(profile)
p.sort_stats(pstats.SortKey.CUMULATIVE).print_stats()
