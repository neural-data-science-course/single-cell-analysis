import numpy as np


def create_receptive_field(size=(15, 15),
                           mu=(8, 8),
                           sigma=(4, 4),
                           angle=45,
                           frequency=.085,
                           phase=0.):
    """2D Gabor-like receptive field

    Parameters
    ----------
    size: tuple
      (width, height) of the 2D RF
    mu: tuple
      (x, y) center coordinates of the Gaussian envelope
    sigma: tuple
      standard deviation of the Gaussian envelope
    angle: float
      Angle of the grating (in degrees)
    frequency: float
      Spatial grating frequency
    phase: float
      Spatial phase (in degrees)
    """

    xx, yy = np.meshgrid(1. + np.arange(size[0]),
                         1. + np.arange(size[1]))

    # Gaussian envelope
    G = np.exp(- np.power(xx - mu[0], 2) / (2. * sigma[0])
               - np.power(yy - mu[1], 2) / (2. * sigma[1]))

    # spatial modulation
    phi = np.deg2rad(angle)
    xxr = xx * np.cos(phi)
    yyr = yy * np.sin(phi)
    xyr = (xxr + yyr) * 2. * np.pi * 2. * frequency
    S = np.cos(xyr + phase)

    K = G * S
    K /= np.amax(np.abs(K))

    return K


def create_gaussian_stimuli(n_bins, n_dim,
                            std_dev=1.,
                            append_ones=True):
    """Gausssian white noise stimulus matrix

    Parameter
    ---------
    n_bins: int
        Number of time steps
    n_dim: int
        RF dimensionality (= stimulus space dimensionality)
    std_dev: float
        Standard deviation of the Gaussian white noise
    append_ones: bool
        Append a column of ones to the stimulus matrix
    """

    S = std_dev * np.random.randn(n_bins, n_dim)

    if append_ones:
        # append a row with ones for fitting the offset term
        S = np.hstack((S, np.ones((n_bins, 1))))

    return S


def f_identity(x):
    # identity function used in a truly linear model

    return x


def f_threshold_quadratic(x):
    # threshold-quadratic nonlinearity

    y = np.copy(x)
    y[y < 0] = 0

    return y**2


def f_quadratic(x):
    # fully quadratic nonliearity

    return x**2


def generate_data_linear(rf_size=(15, 15),
                         f_nonlin=f_identity,
                         duration=10.,
                         dt=.1,
                         offset=2.,
                         noise_variance=4):
    """create model, stimulus set and and simulate neural response

    The model consists of the two stages:
    1. A 2-dimensional RF that is used to filter 2D Gaussian white noise stimuli
    2. A threshold-linear nonlinearity (as neural firing rates cannot be negative)

    Note: by using a large offset term (r_0) the model can be made linear as the product k x s will be 
    positive. However, for the chosen stimulus class (Gaussian white noise) the linear estimator provides 
    an unbiased estimate even in the presence of a nonlinearity (Bussgang Res. Lab. Elec. (1952), Paninski 
    Network (2003)).

    Parameters
    ----------
    duration: float
        Length of the data sequence in seconds
    f_nonlin: function-like
        The (potentially nonlinear) function that transforms k x s into a neural response (default: identity)
    dt: float
        Bin width (= time resolution) in seconds
    offset: float
        Offset term (see "r_0" in the description above)
    noise_variance: float
        Response noise variance
    """

    assert duration > 0 and dt > 0 and noise_variance >= 0

    # get number of non-overlapping time bins
    n_bins = round(duration / float(dt))

    # Gabor-like receptive field
    K = create_receptive_field(size=rf_size)  # 2D RF -> matrix

    # append entry to "true" RF (ravel() vectorizes the 2D RF matrix into a 1D vector)
    k_with_offset = np.append(K.ravel(), offset)

    # generate Gaussian stimuli
    # dimensionality of "vectorized" RF (= dim. of stimuli); the same as K.shape[0]*K.shape[1]
    n_dim = K.size
    S = create_gaussian_stimuli(n_bins, n_dim,
                                append_ones=True)

    # 1. linear stage
    ks = np.dot(k_with_offset, S.T)

    # 2. nonlinear stage (for a truly linear model: f -> identity function)
    rate = f_nonlin(ks)

    # add Gaussian noise centered around the "true" rate for each bin
    rate = rate + np.sqrt(noise_variance) * np.random.randn(n_bins)

    return K, S, ks, rate


def generate_inhomogeneous_poisson_spikes(lamda, dt):

    n_bins = lamda.shape[0]
    bins = np.arange(n_bins+1)*dt

    # generate Poisson distributed numbers for all bins with the max. intensity (lamda_max)
    lamda_max = np.max(lamda)
    poisson_numbers = np.random.poisson(lamda_max, size=n_bins)

    # throw away numbers depending on the actual intensity ("thinning")
    spike_times = []
    prob = lamda / lamda_max
    for i in range(n_bins):

        # number of spikes to keep in this bin
        n = np.sum(np.random.rand(poisson_numbers[i]) < prob[i])
        n_s = int(round(n * dt))

        # generate random spike times in this bin
        ts = bins[i] + np.random.rand(n_s)*dt

        spike_times.extend(ts)

    return np.asarray(spike_times)


def generate_data_poisson(rf_size=(15, 15),
                          duration=10.,
                          dt=.1,  # delta in equation
                          offset=0.,
                          spike_rate=5.  # average spike rate
                          ):

    assert duration > 0 and dt > 0

    # get number of non-overlapping time bins
    n_bins = round(duration / float(dt))

    # Gabor-like receptive field
    K = create_receptive_field(size=rf_size)  # 2D RF -> matrix

    # generate Gaussian stimuli
    # dimensionality of "vectorized" RF (= dim. of stimuli); the same as K.shape[0]*K.shape[1]
    n_dim = K.size
    S = create_gaussian_stimuli(n_bins, n_dim,
                                # gives a more realistic spike rate (exp() nonlinearity can produce very large values)
                                std_dev=.75,
                                append_ones=True)

    # append entry to "true" RF (ravel() vectorizes the 2D RF matrix)
    k_with_offset = np.append(K.ravel(), offset)

    # 1. linear stage
    ks = np.dot(k_with_offset, S.T)

    # 2. nonlinear stage
    lamda = np.exp(ks)

    # lamda * dt is the number of spikes in the different bins (but keep in mind that the Poisson process
    # is a stochastic process so the actual number will differ for every draw). Thus, the sum of the product
    # across all bins gives the expected number of spikes for the whole draw.
    expected_rate = np.sum(lamda*dt) / duration
    lamda *= (spike_rate / expected_rate)

    # generate spike times using an inhomogeneous Poisson process
    spike_times = generate_inhomogeneous_poisson_spikes(lamda, dt)

    # compute spike counts in the different time bins
    spike_counts = np.histogram(spike_times,
                                bins=np.arange(n_bins+1)*dt)[0]

    print("average spike rate: %0.2f spikes per second" %
          (len(spike_times) / duration))

    return K, S, ks, lamda, spike_times, spike_counts
