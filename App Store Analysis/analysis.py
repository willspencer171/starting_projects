#! python3
# A python program that analyses and presents data from a dataset
# comprising apps from the App Store and Google Play Store
# Wanted to make an App object but because the two files have two different formats,
# can't use a single App object, and using two would defeat the point
import re
from datetime import datetime
import os
from collections import namedtuple
import inspect
import dill
import time
import threading
from queue import Queue
from functions import *

global finished
finished = False

PATH_TO_APP_STORE = "App Store Analysis\\AppleStore.dill"
PATH_TO_GOOGLE_PLAY_STORE = "App Store Analysis\\googleplaystore.dill"
RE_FLOAT = re.compile(r"[0-9.]+$")
RE_M = re.compile(r"[0-9.]+M$")
RE_K = re.compile(r"[0-9.]+k$")

# stole this online: https://stackoverflow.com/questions/18425225/getting-the-name-of-a-variable-as-a-string
# uses the inspect module to have a look at the local variable of the previous previous frame (in this case, call)
# and check to see what the name of the variable passed to the function is called
def retrieve_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var]

def custom_thread(target_1: tuple, target_2: tuple):
    progress_thread = threading.Thread(target=target_1[0], args=target_1[1])
    progress_thread.start()

    gen_thread = threading.Thread(target=target_2[0], args=target_2[1])
    gen_thread.start()

    gen_thread.join()
    globals()["finished"] = True
    # Retrieve dataset from queue
    progress_thread.join()
    globals()["finished"] = False

# For threading, this will indicate that the process is still continuing
def show_progress(string):
    print(string, end='\r')
    dot = 0
    space = " " * (len(string) + 4) + "\033[A"
    while not finished:
        print(space)
        print(string + "." * ((dot % 3)+1), end="\r")
        time.sleep(0.3)
        dot += 1
    print(space, end="\n")

# Essentially cleans the data
def app_value_clean(value: str, output: list, iteration=None,
                    re_float=RE_FLOAT, re_m=RE_M, re_k=RE_K):
    
    def isfloat(val):
        return re_float.match(val)
    
    if isinstance(value, int):
        pass
    # If only digits, convert to int (There are no phone numbers)
    elif value.isdigit():
        # this is where the size is held in the apple db
        if iteration == 2:
            value = round(float(value) / 1000000, 2)
        else:
            value = int(value)
    # if digits and period "." (only one since there are version numbers with multiple "."),
    # convert to float
    elif isfloat(value) and value.count(".") <= 1 and value != "":
        value = float(value)
    
    # There are some instances where the number of installs is *multiple of 10*+
    # We can't use this number to do any maths with so convert to int
    elif value.startswith('"') and re.search('[0-1]\+"$', value):
        value = int("".join([letter for letter in value[1:-2] if letter != ","]))
    
    elif re_m.match(value) and isfloat(value[:-1]):
        value = float(value[:-1])
    
    elif re_k.match(value) and isfloat(value[:-1]):
        value = float(value[:-1]) / 1000

    # If it's a date, convert to date
    elif value.startswith('"') and value.endswith('"'):
        try:
            value = datetime.strptime(value, '"%B %d, %Y"').date()
        except ValueError:
            pass

    # finally, update the dictionary
    output += [value]

# Useful when displaying a date, and keeping format consistent
def convert_date_to_string(date: datetime):
    return datetime.strftime(date, "%d/%m/%Y")

# Will open the data and process it into a format I can manipulate
def open_data(file, headers=True):
    # open the file with utf-8 encoding
    with open(file, "r", encoding="utf-8") as f:
        
        # If declared headers, use them as keys
        if headers:
            _headers = re.split(",", f.readline())
            _headers = [item.replace(" ", "_").lower() for item in _headers]
            if _headers[-1].endswith("\n"):
                _headers[-1] = _headers[-1][:-1]
            
            
        read_file = f.readlines()
    

    # I'm not very good at regex, so I got ChatGPT to write this expression for me,
    # it works for both Apple and Google datasets which is nice.
    # Here's the breakdown:
    # , - Matches a comma character.
    # (?=- Positive lookahead assertion. This is a zero-width assertion that matches a comma only if it is followed by the pattern that follows the=sign.
    # (?: - Non-capturing group. This group is used for grouping multiple expressions together without capturing the matched text.
    # (?: [ ^ "]*"){2} - Matches any number of characters that are not double-quotes, followed by a double-quote character, and repeats this pattern twice.
    # ) * - Matches the previous group zero or more times.
    # [ ^"] * - Matches any number of characters that are not double-quotes.
    # $ - Matches the end of the string.
    read_file = [re.split(r',(?=(?:(?:[^"]*"){2})*[^"]*$)', item.strip()) 
                    for item in read_file 
                    # exclude any with Asian (CJK) characters
                    if not re.findall("[\u31c0-\u9fff]", "".join(item))
                    and "Varies with device" not in item
                    ]
    """ don't need anymore since ?: indicates non-capturing groups 
    for i in range(len(read_file)):
        read_file[i] = [j for j in read_file[i] if j != ","] """
    """ also no longer needed as item.strip() removes whitespace including \\n 
        if _app[-1].endswith("\n"):
            _app[-1] = _app[-1][:-1] """

    output = {}
    duplicate = set()
    dup_count = 0

    # Cycle through apps in file, adding each to the dictionary using headers as keys
    # Each value must be checked and converted to int, float, or date
    for app_index, _app in enumerate(read_file):
        if _app[0] in duplicate:
            dup_count += 1
            continue

        vals = []
        if headers:
            if "id" not in _headers:
                _headers += ["id"]
                _new_id = True
            if "_new_id" in locals():
                _app += [app_index]
            App = namedtuple("App", _headers)
            
        else:
            # if no headers, the key is just the index of the column
            # could refactor this into the OutputDict.app_update_check function but it would lose
            # readability I think
            App = namedtuple("App", range(len(_app[0])))
        
        for index, value in enumerate(_app):
            app_value_clean(value, vals, index)
            
        # Add to dict
        current_app = App(*vals)
        output.update({current_app.id: current_app})
        duplicate.add(_app[0])
        
    print(f"Removed {dup_count} duplicate rows from {os.path.basename(file)}")
            
    return output



# This code drives the above function ONLY if it can't be retrieved from a dill file
def load_save_data(path):
    csv_file = path[:-4] + "csv"
    # I HAVE THEM SAVED thanks to dill :) better than pickle in that it'll save namedtuples to a .dill file :)
    # Did try using gzip to speed up serialisation but while it saved on space, it actually slowed the retrieval
    if os.path.exists(path):

        # Prime for threading
        def open_file(path, queue: Queue):
            with open(path, "rb") as file:
                output = dill.load(file)
                queue.put(output)

        output_queue = Queue()
        custom_thread((show_progress, (f"Fetching {path}",)), (open_file, (path, output_queue)))
        output = output_queue.get()
        
        print(f"File loaded: {len(output)} items with {len(output[list(output.keys())[0]])} traits each\n")

    else:
        print("No .dill found, generating data")
        
        output_queue = Queue()
        def gen_output(file, queue: Queue):
            output = open_data(file)
            queue.put(output)

        custom_thread((show_progress, ("Generating",)), 
                      (gen_output, (csv_file, output_queue)))
        
        # Retrieve dataset from queue
        output = output_queue.get() 
        del output_queue

        def dump_output(path, output):
            with open(path, "wb") as dump:
                # Highest protocol is fastest and smallest file size
                dill.dump(output, dump, protocol=dill.HIGHEST_PROTOCOL)
        
        custom_thread((show_progress, ("Serialising",)), 
                      (dump_output, (path, output)))

        print(path, "Serialised using dill protocol", dill.HIGHEST_PROTOCOL, "\n")
    
    return output

google_play = load_save_data(PATH_TO_GOOGLE_PLAY_STORE)
app_store = load_save_data(PATH_TO_APP_STORE)

# Took a while to load it all in in a nice format but we have it all ready now.
# Let's get into analysis

# Makes it easy to retrieve the information we can see in the apps, depending on store
def display_fields(apps: dict):
    print(f"fields accessible through {retrieve_name(apps)[0]}:")
    for item in list(apps.values())[0]._fields:
        print(item)


def freq_table(dataset: dict, attr: str):
    table = {}
    total = len(dataset)

    for item in dataset.values():
        value = getattr(item, attr.lower())
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    return {key: round((value/total)*100, 5) for key, value in table.items()}

def display_freq_table(dataset: dict, attr="", reverse=True, is_freq_table=False):
    
    if is_freq_table:
        table = dataset
    else:
        table = freq_table(dataset, attr)
        
    sorted_table = sorted(table.items(), key=lambda x: x[1], reverse=reverse)
    for key, value in sorted_table:
        print(key, value, sep=": ")

display_fields(app_store)
print()
apple_genres = freq_table(app_store, "prime_genre")
display_freq_table(apple_genres, is_freq_table=True)
