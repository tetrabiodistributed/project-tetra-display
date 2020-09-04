import numpy as np


def filter_rms_error(filter_class,
                     to_filter_data_lambda,
                     desired_filter_data_lambda,
                     dt=0.01,
                     start_time=0,
                     end_time=10,
                     skip_initial=0):
    t = np.arange(start_time, end_time, dt)
    test_filter = filter_class(dt)
    to_filter_data = to_filter_data_lambda(t)
    filtered_data = np.array([])
    desired_filtered_data = desired_filter_data_lambda(t)
    error = np.array([])
    for i in range(len(to_filter_data)):
        test_filter.append(to_filter_data[i])
        filtered_data = np.append(filtered_data,
                                  test_filter.get_datum())
        error = np.append(error,
                          desired_filtered_data[i] - filtered_data[i])
    return np.sqrt(np.mean(error[skip_initial:]**2))
