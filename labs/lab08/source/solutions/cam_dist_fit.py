# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

# Fill the lists with the data you measured
X = [62, 73, 88, 118, 185, 253, 450]  # Size [px]
Y = [1800, 1600, 1300, 900, 600, 400, 200]  # Distance [mm]


def blob_size_to_distance(blob_size, a, b):
    """
    TASK: The cost function which parameters we are looking for, replace with correct function
    """

    dist = a / blob_size - b

    return dist


def main():
    # The curve fitting happens here
    optimized_parameters, pcov = opt.curve_fit(
        blob_size_to_distance,
        X,
        Y,
        bounds=([-np.inf, -np.inf], [np.inf, np.inf])
    )

    print(optimized_parameters)
    a = optimized_parameters[0]
    b = optimized_parameters[1]

    print("Optimized parameters:")
    print("  a = " + str(a))
    print("  b = " + str(b))

    # Calculate points with the optimized parameters
    x_data_fit = np.linspace(min(X), max(X), 100)
    y_data_fit = blob_size_to_distance(x_data_fit, *optimized_parameters)

    # Plot the data
    plt.plot(X, Y, ".", label="measured data")
    plt.plot(x_data_fit, y_data_fit, label="fitted data")

    # Show the graph
    plt.legend()
    plt.xlabel("Blob size (px)")
    plt.ylabel("Distance (mm)")
    plt.show()


if __name__ == "__main__":
    main()
