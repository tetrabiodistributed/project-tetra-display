import numpy as np
import matplotlib.pyplot as plt


def filter_rms_error(filter_object,
                     to_filter_data_lambda,
                     desired_filter_data_lambda,
                     dt=0.01,
                     start_time=0.0,
                     end_time=10.0,
                     skip_initial=0,
                     use_pressure_error=False,
                     abs_tol=2.0,
                     rel_tol=0.02,
                     generate_plot=False):
    """Calculates root-mean-square (RMS) error between data calculated
    by a filter and a reference function that nominally should yield
    equal data.

    Parameters
    ----------
    filter_object : object
        An object representing the filter being tested.  It must have
        the following functions defined.
            filter_object(dt: float)
            filter_object.append(datum: float)
            filter_object.get_datum() -> float
    to_filter_data_lambda : lambda
        A function representing the data being fed to the filter.  It
        should be of the form
            to_filter_lambda(time: np.array) -> np.array
    desired_filter_data_lambda : lambda
        A function representing output that the filter_object output
        should be nominally equal to.  It should be of the form
            desired_filter_data_lambda(time: np.array) -> np.array
    start_time=0.0 : float
    end_time=10.0 : float
    dt=0.01 : float
        Represents a time interval in seconds of [start_time, end_time)
        with steps of dt between.  Calculated as
        np.arange(start_time, end_time, dt).
    skip_initial=0 : int
        Ignores the first skip_inital data points when calculating
        error.  This is useful when a filter has an initial transient
        before it starts returning useful data.
    use_pressure_error=False : bool
        Instead of calculating direct RMS error, this function will
        calculate a normalized error based on given tolerances.  This is
        useful for ventilators trying to calculate pressure meeting
        ISO 80601-2-80:2018 201.12.4.101.1.  Default values for the
        tolerances are based on this standard.
    abs_tol=2.0 : float
        The design absolute tolerance when calculating pressure error,
        i.e. +/- abs_tol.  Only used if use_pressure_error == True.
    rel_tol=0.02 : float
        The design relative tolerance when calculating pressure error,
        i.e. +/- rel_tol * desired_filter_data(t).
    generate_plot=False : bool
        If True, then a plot of the filter data and
        desired_filter_data_lambda with respect to time will be
        generated.  Note that this should be false in non-interactive
        contexts.

    Returns
    -------
    error : float
        If use_pressure_error is False,
            This returns the RMS error between the filter output and
            the output of desired_filter_data_lambda.
        If use_pressure_error is True,
            This returns a normalized error between the filter output
            and the output of desired_filter_data_lambda.  If error < 1,
            then the typical error is within the design tolerance.  When
            testing, you can add a safety factor to the error by
            asserting that the error must be less than 1/safety_factor.
    """
    t = np.arange(start_time, end_time, dt)
    test_filter = filter_object(dt)
    to_filter_data = to_filter_data_lambda(t)
    filtered_data = np.array([])
    desired_filtered_data = desired_filter_data_lambda(t)
    for i in range(len(to_filter_data)):
        test_filter.append(to_filter_data[i])
        filtered_data = np.append(filtered_data,
                                  test_filter.get_datum())

    if generate_plot:
        figure, axis = plt.subplots()
        axis.plot(t, to_filter_data, label="To Filter Data")
        axis.plot(t, filtered_data, label="Filtered Data")
        axis.plot(t, desired_filtered_data, label="Desired Filtered Data")
        axis.legend()
        plt.show()

    if not use_pressure_error:
        return _root_mean_square(
            (filtered_data - desired_filtered_data)[skip_initial:])
    else:
        return _pressure_error(filtered_data[skip_initial:],
                               desired_filtered_data[skip_initial:])


def _root_mean_square(np_array):
    return np.sqrt(np.mean(np.square(np_array)))


def _pressure_error(calculated_pressure,
                    actual_pressure,
                    abs_tol=2.0,
                    rel_tol=0.02):
    return _root_mean_square(
        (calculated_pressure - actual_pressure)
        / (np.full_like(actual_pressure, abs_tol) + rel_tol * actual_pressure)
    )
