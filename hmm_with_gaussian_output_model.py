from numpy.linalg import inv, det
from numpy import pi, sqrt, exp, dot, sum, outer, array, zeros
from numpy.random import random, choice, multivariate_normal

def check(w, a, b, means, variances):
    L = len(w)
    I = max([len(w[l]) for l in range(0, L)])
    J = len(b)
    K = len(w[0][0])
    if len(a.shape)!=2 or a.shape[0]!=J or a.shape[1]!=J:
        raise RuntimeError("a has wrong shape")
    if len(b.shape)!=1:
        raise RuntimeError("b has wrong shape")
    if len(means.shape)!=2 or means.shape[0]!=J or means.shape[1]!=K:
        raise RuntimeError("means has wrong shape")
    for wl in w:
        for wli in wl:
            if len(wli)!=K:
                raise RuntimeError("w has bad word")
    return I, J, K, L

def distance(x, mean, variance):
    return dot((x-mean), dot(inv(variance), (x-mean)))

def gaussian(x, mean, variance):
    coefficient = 1/sqrt((2*pi)**len(x)*det(variance))
    return coefficient*exp(-0.5*distance(x, mean, variance))

def calculate_alpha(w, a, b, means, variances):
    I, J, K, L = check(w, a, b, means, variances)
    alpha = zeros([L, I, J])
    for l in range(0, L):
        for j in range(0, J):
            alpha[l, 0, j] = b[j]*gaussian(w[l][0], means[j], variances[j])
        for i in range(1, len(w[l])):
            for j in range(0, J):
                for j_prime in range(0, J):
                    alpha[l, i, j] += alpha[l, i-1, j_prime]*a[j_prime, j]
                alpha[l, i, j] *= gaussian(w[l][i], means[j], variances[j])
    return alpha

def calculate_beta(w, a, b, means, variances):
    I, J, K, L = check(w, a, b, means, variances)
    beta = zeros([L, I, J])
    for l in range(0, L):
        for j in range(0, J):
            beta[l, len(w[l])-1, j] = 1
        for i in range(len(w[l])-2, -1, -1):
            for j in range(0, J):
                for j_prime in range(0, J):
                    beta[l, i, j] += (
                        a[j, j_prime]*
                        gaussian(w[l][i+1], means[j_prime], variances[j_prime])*
                        beta[l, i+1, j_prime])
    return beta

def random_gamma(w, J):
    L = len(w)
    I = max([len(w[l]) for l in range(0, L)])
    gamma = zeros([L, I, J])
    for l in range(0, L):
        for i in range(0, len(w[l])):
            for j in range(0, J):
                gamma[l, i, j] = random()
            gamma[l, i, :] /= sum(gamma[l, i, :])
    return gamma

def calculate_gamma(w, a, b, means, variances):
    I, J, K, L = check(w, a, b, means, variances)
    alpha = calculate_alpha(w, a, b, means, variances)
    beta = calculate_beta(w, a, b, means, variances)
    gamma = zeros([L, I, J])
    for l in range(0, L):
        for i in range(0, len(w[l])):
            for j in range(0, J):
                gamma[l, i, j] = alpha[l, i, j]*beta[l, i, j]
            gamma[l, i, :] /= sum(gamma[l, i, :])
    return gamma

def train(w, gamma):
    J = gamma.shape[2]
    K = len(w[0][0])
    L = len(w)
    for wl in w:
        for wli in wl:
            if len(wli)!=K:
                raise RuntimeError("w has bad word")
    a = zeros([J, J])
    b = zeros([J])
    means = zeros([J, K])
    variances = zeros([J, K, K])
    for j in range(0, J):
        for j_prime in range(0, J):
            for l in range(0, L):
                for i in range(0, len(w[l])-1):
                    a[j, j_prime] += gamma[l, i, j]*gamma[l, i+1, j_prime]
        a[j, :] /= sum(a[j, :])
        for l in range(0, L):
            b[j] += gamma[l, 0, j]
        for l in range(0, L):
            for i in range(0, len(w[l])):
                means[j, :] += gamma[l, i, j]*w[l][i]
        means[j, :] /= sum(gamma[:, :, j])
        for l in range(0, L):
            for i in range(0, len(w[l])):
                point = w[l][i]-means[j, :]
                variances[j, :] += gamma[l, i, j]*outer(point, point)
        variances[j, :] /= sum(gamma[:, :, j])
    b /= sum(b)
    return a, b, means, variances

def likelihood(w, a, b, means, variances):
    I, J, K, L = check(w, a, b, means, variances)
    alpha = calculate_alpha(w, a, b, means, variances)
    p = 1
    for l in range(0, L):
        pl = 0
        for j in range(0, J):
            pl += alpha[l, len(w[l])-1, j]
        p *= pl
    return p

def alternate_likelihood(w, a, b, means, variances):
    I, J, K, L = check(w, a, b, means, variances)
    beta = calculate_beta(w, a, b, means, variances)
    p = 1
    for l in range(0, L):
        pl = 0
        for j in range(0, J):
            pl += b[j]*gaussian(w[l][0], means[j], variances[j])*beta[l, 0, j]
        p *= pl
    return p

def sample(a, b, means, variances, I):
    J = len(b)
    K = means.shape[1]
    j = choice(range(0, J), 1, p=b)[0]
    w = []
    for i in range(1, I+1):
        w.append(multivariate_normal(means[j], variances[j]))
        j = choice(range(0, J), 1, p=a[j, :])[0]
    return w

def samples(a, b, means, variances, I, L):
    return [sample(a, b, means, variances, I) for l in range(0, L)]

def model():
    a = array([[0.5, 0.5], [0, 1]])
    b = array([1, 0])
    means = array([[0, 0], [1, 1]])
    variances = array([[[1, 0], [0, 1]], [[1, 0], [0, 1]]])
    return a, b, means, variances

def baum_welch_initial(w, J):
    gamma = random_gamma(w, J)
    a, b, means, variances = train(w, gamma)
    return a, b, means, variances

def baum_welch_step(w, a, b, means, variances):
    gamma = calculate_gamma(w, a, b, means, variances)
    a, b, means, variances = train(w, gamma)
    return a, b, means, variances

def baum_welch(w, J):
    a, b, means, variances = baum_welch_initial(w, J)
    p = likelihood(w, a, b, means, variances)
    print p
    while True:
        a, b, means, variances = baum_welch_step(w, a, b, means, variances)
        new_p = likelihood(w, a, b, means, variances)
        print new_p
        if new_p<=p:
            return a, b, means, variances
        p = new_p
