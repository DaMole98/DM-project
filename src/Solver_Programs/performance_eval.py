import json

DEBUG = True
def write_performance(name_function, dataset, time):
    if DEBUG:
        print("write_performance function called")
        print(f"name_function = {name_function}")
        print(f"dataset = {dataset}")
        print(f"time = {time}")
    # open a json file in append mode
    with open(f"./performance.json", 'a') as file:
        # write the data
        json.dump({"function": name_function, "dataset": dataset, "time": time}, file)
        # write a new line
        file.write("\n")