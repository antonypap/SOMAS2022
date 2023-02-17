import os
import json
import matplotlib.pyplot as plt

OUTPUT_FILE_LOCATION = "./output/output.json"
RUN_COMMAND = "go run ./pkg/infra "
NUM_ITERATIONS = 1


def fixed_dict_to_plot_both(d1: dict, d2: dict):
    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Fixed Sanction Length (Turns)"
    ylabel = "Average Level Reached (Turns)"
    filename = "fixedBoth"

    names1, counts1 = zip(*d1.items())
    names2, counts2 = zip(*d2.items())
    plt.figure()
    plt.plot(names1, counts1, "-o")
    plt.plot(names2, counts2, "-o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f"./figures/{filename}.pdf")


def fixed_dict_to_plot(data: dict, is_persistent: bool):

    # title = "Level Reached Against Fixed Sanction Length"
    xlabel = "Fixed Sanction Length (Turns)"
    ylabel = "Average Level Reached (Turns)"
    filename = "fixedNonPersist"
    if is_persistent:
        filename = "fixedPersist"

    names, counts = zip(*data.items())
    plt.figure()
    plt.plot(names, counts, "-o")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(f"./figures/{filename}.pdf")


def parseJSON(data):
    level_data = data["Levels"]
    return len(level_data)


def fixedLength(is_persistent: bool = False):
    durations = [0, 5, 10, 15, 20, 25, 30]
    duration_comp = {}
    for duration in durations:
        avg_level_reached = 0
        for _ in range(NUM_ITERATIONS):
            full_run_command = RUN_COMMAND + \
                f"-fSanc={duration} -verbose=false"
            if is_persistent:
                full_run_command += " -pSanc=true"

            os.system(full_run_command)

            with open(OUTPUT_FILE_LOCATION) as OUTPUT_JSON:
                DATA = json.load(OUTPUT_JSON)
                lvl = parseJSON(DATA)
                avg_level_reached += lvl
        avg_level_reached /= NUM_ITERATIONS
        duration_comp[duration] = avg_level_reached

    for duration, score in duration_comp.items():
        print(f"duration:{duration}, score:{score}")

    fixed_dict_to_plot(duration_comp, is_persistent)

    return duration_comp


def dynamic():
    return


def graduated():
    return


if __name__ == "__main__":
    fixedPer = fixedLength(is_persistent=True)
    fixedNotPer = fixedLength(is_persistent=False)
    fixed_dict_to_plot_both(fixedPer, fixedNotPer)
    # dynamic()
    # graduated()
