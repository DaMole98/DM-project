import json
import matplotlib.pyplot as plt
import numpy as np

DEBUG = True
def write_performance(name_function, dataset, time):
    if DEBUG:
        print("write_performance function called")
        print(f"name_function = {name_function}")
        print(f"dataset = {dataset}")
        print(f"time = {time}")
    # open a json file in append mode
    with open(f"performance.json", 'a') as file:
        # write the data
        json.dump({"function": name_function, "dataset": dataset, "time": time}, file)
        # write a new line
        file.write("\n")

def plotter():
    """
    This function plots the performance of the algorithms
    """
    # read the json file
    with open(f"performance.json", 'r') as file:
        data = json.load(file)

    # divide the data in 3 lists
    name_function = [d["function"] for d in data]

    # replace the name of dataset frome size_dataset to size
    find_best_1 = [d for d in data if d["function"] == "find_best_1"]
    plot_performance_find_best_1(find_best_1)

    perfectRt = [d for d in data if d["function"] == "perfectRoutesFinder"]
    plot_performance_perfectRt(perfectRt)

    generate_new_std_1 = [d for d in data if d["function"] == "generate_new_std_1"]
    plot_performance_generate_new_std_1(generate_new_std_1)



def plot_performance_find_best_1(data):
    if DEBUG:
        print("plot_performance_find_best_1 function called")

    # Keep only the data regarding the find_best_1 function
    data = [d for d in data if d["function"] == "find_best_1"]

    # Sort the data in this order: small, small1, small2, medium, medium1
    data_sorted = [data[0], data[2], data[3], data[4], data[1]]

    # Extract the time and the dataset
    time = [round(d["time"], 4) for d in data_sorted]
    dataset = [d["dataset"] for d in data_sorted]

    # Plot the data in a bar chart
    plt.bar(dataset, time, color='orange')  # Adjust color for clarity
    plt.xlabel("Dataset")
    plt.ylabel("Time (s)")
    plt.title("Performance of FindBestRoutes")
    plt.xticks(fontsize=8)  # Rotate x-axis labels for better visibility

    # Save the plot before displaying it
    plt.savefig("performance_find_best_1.png")

    plt.clf()

    # Convert time values to log base 2
    log_time = np.log2(time)

    # Plot the data in a bar chart with log scale on the y-axis (base 2)
    plt.bar(dataset, log_time, color='orange')  # Adjust color for clarity
    plt.xlabel("Dataset")
    plt.ylabel("Log2(Time) (s)")
    plt.title("Performance of FindBestRoutes log2 scale")
    plt.xticks(fontsize=8)  # Rotate x-axis labels for better visibility

    # set the yticks every 0.5
    plt.yticks(np.arange(min(log_time), max(log_time)+0.5, 0.5))

    # Save the plot before displaying it
    plt.savefig("performance_find_best_1_log2.png")

    plt.clf()

def plot_performance_perfectRt(data):
    # Keep only the data regarding the perfectRoute function
    data = [d for d in data if d["function"] == "perfectRoutesFinder"]

    # Sort the data in this order: small, small1, small2, medium, medium1
    data_sorted = [data[0], data[2], data[3], data[4], data[1]]

    # Extract the time and the dataset
    time = [round(d["time"], 4) for d in data_sorted]
    dataset = [d["dataset"] for d in data_sorted]

    # Plot the data in a bar chart
    plt.bar(dataset, time, color='blue')
    plt.xlabel("Dataset")
    plt.ylabel("Time (s)")
    plt.title("Performance of perfectRoutesFinder")
    plt.xticks(fontsize=8)  # Rotate x-axis labels for better visibility

    # Save the plot before displaying it
    plt.savefig("performance_perfectfind.png")

    plt.clf()

    # Convert time values to log base 2
    log_time = np.log2(time)

    print(log_time)

    # Plot the data in a bar chart with log scale on the y-axis (base 2)
    plt.bar(dataset, log_time, color='blue')
    plt.xlabel("Dataset")
    plt.ylabel("Log2(Time) (s)")
    plt.title("Performance of perfectRoutesFinder log2 scale")
    plt.xticks(fontsize=8)  # Rotate x-axis labels for better visibility

    # set the yticks every 0.5
    plt.yticks(np.arange(min(log_time), max(log_time)+0.5, 0.5))

    # Save the plot before displaying it
    plt.savefig("performance_perfectfind_log2.png")

    plt.clf()
def plot_performance_generate_new_std_1(data):
    if DEBUG:
        print("plot_performance_generate_new_std_1 function called")


    # Keep only the data regarding the generate_new_std_1 function
    data = [d for d in data if d["function"] == "generate_new_std_1"]

    # Sort the data in this order: small, small1, small2, medium, medium1
    data_sorted = [data[0], data[2], data[3], data[4], data[1]]

    # Extract the time and the dataset
    time = [round(d["time"], 4) for d in data_sorted]
    dataset = [d["dataset"] for d in data_sorted]

    # Plot the data in a bar chart
    plt.bar(dataset, time, color='green')  # Adjust color for clarity
    plt.xlabel("Dataset")
    plt.ylabel("Time (s)")
    plt.title("Performance of GenerateNewSTD")
    plt.xticks(fontsize=8)  # Rotate x-axis labels for better visibility

    # Save the plot before displaying it
    plt.savefig("performance_generate_new_std_1.png")

    plt.clf()

    # Convert time values to log base 2
    log_time = np.log2(time)

    # Plot the data in a bar chart with log scale on the y-axis (base 2)
    plt.bar(dataset, log_time, color='green')  # Adjust color for clarity
    plt.xlabel("Dataset")
    plt.ylabel("Log2(Time) (s)")
    plt.title("Performance of GenerateNewSTD log2 scale")
    plt.xticks(fontsize=8)  # Rotate x-axis labels for better visibility


    # set the yticks every 0.5
    plt.yticks(np.arange(min(log_time), max(log_time)+0.5, 0.5))

    # Save the plot before displaying it
    plt.savefig("performance_generate_new_std_1_log2.png")

    plt.clf()
plotter()