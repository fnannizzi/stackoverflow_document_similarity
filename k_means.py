import sys
import random

def main():
    # argv[1]: a model file containing all data points
    # argv[2]: output file to write k-mean results
    data = read_model_file(sys.argv[1])
    means = run_k_means(data)
    write_output_file(sys.argv[2], means)

def read_model_file(file):
    model = open(file, "r")
    lines = model.readlines()
    model.close()
    data = []
    for line in lines:
        data.append(line)
    return data

def run_k_means(data):
    means = [random() for i in range(10)]
    param = .01

    for value in data:
        closest_k = 0;
        smallest_error = float("INF")
        for k in enumerate(means):
            error = abs(value - k[1])
            if error < smallest_error:
                smallest_error = error
                closest_k = k[0]
            means[closest_k] = means[closest_k] * (1-param) + value*(param)
    return means

def write_output_file(file, means):
    output = open(file, "r")
    for mean in means:
        output.write(str(mean) + "\n")
    output.close()

if __name__ == "__main__":
    main()