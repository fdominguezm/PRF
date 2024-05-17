import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

def sample_gaussian(sigma):
    # Sample from a Gaussian distribution with standard deviation sigma
    rho = lambda k: np.exp(-k**2/(2*sigma**2))
    S = np.sqrt(2*np.pi)*sigma # good approximation of S according to section 4 in paper
    
    # x and y make up the discrete Gaussian distribution (or almost, due to limited S)
    x = np.arange(-12*sigma, 12*sigma) # large range, taken from paper
    y = rho(x)/S
    cum_y = np.cumsum(y)
    uni = np.random.random()  # draw uniform between 0 and 1
    diff = np.absolute(cum_y - uni)
    i = np.argmin(diff) # index of closest y value to the uniform sample
    x_sample = x[i] # this is now a sample from discrete gaussian
    return x_sample

#  Paper explaining discrete gaussian:
# https://en.wikipedia.org/wiki/Ring_learning_with_errors#cite_note-4
def test_dist():
    sigma = 2 # integer(?) what happens when alpha comes in to play
    samples = np.array([sample_gaussian(sigma) for i in range(10**4)])
    vals, counts = np.unique(samples, return_counts=True)
    # hist, bins = np.histogram(samples, bins=6*sigma, range=(-3*sigma, 3*sigma))
    fig = plt.figure()
    ax = fig.gca()
    ax.bar(vals, counts)
    ax.set_title("Histogram of samples from discrete gaussian")
    ax.set_xlabel("Smaple value")
    ax.set_ylabel("Frequency")

    ax.xaxis.set_major_locator(MaxNLocator(integer=True)) # restrict ticks to integers

    fig.show()
    plt.show()
    
test_dist()