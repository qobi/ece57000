from numpy import sum, array, zeros
from numpy.random import random, choice

def check(w, a, b, c):
    L = len(w)
    I = max([len(w[l]) for l in range(0, L)])
    J = len(b)
    K = c.shape[1]
    if len(a.shape)!=2 or a.shape[0]!=J or a.shape[1]!=J:
        raise RuntimeError("a has wrong shape")
    if len(b.shape)!=1:
        raise RuntimeError("b has wrong shape")
    if len(c.shape)!=2 or c.shape[0]!=J:
        raise RuntimeError("c has wrong shape")
    for wl in w:
        for wli in wl:
            if not type(wli)==int or wli<0 or wli>=K:
                raise RuntimeError("w has bad word")
    return I, J, K, L

def calculate_alpha(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    alpha = zeros([L, I, J])
    for l in range(0, L):
        for j in range(0, J):
            alpha[l, 0, j] = b[j]*c[j, w[l][0]]
        for i in range(1, len(w[l])):
            for j in range(0, J):
                for j_prime in range(0, J):
                    alpha[l, i, j] += alpha[l, i-1, j_prime]*a[j_prime, j]
                alpha[l, i, j] *= c[j, w[l][i]]
    return alpha

def calculate_beta(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    beta = zeros([L, I, J])
    for l in range(0, L):
        for j in range(0, J):
            beta[l, len(w[l])-1, j] = 1
        for i in range(len(w[l])-2, -1, -1):
            for j in range(0, J):
                for j_prime in range(0, J):
                    beta[l, i, j] += (a[j, j_prime]*
                                      c[j_prime, w[l][i+1]]*
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

def calculate_gamma(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    alpha = calculate_alpha(w, a, b, c)
    beta = calculate_beta(w, a, b, c)
    gamma = zeros([L, I, J])
    for l in range(0, L):
        for i in range(0, len(w[l])):
            for j in range(0, J):
                gamma[l, i, j] = alpha[l, i, j]*beta[l, i, j]
            gamma[l, i, :] /= sum(gamma[l, i, :])
    return gamma

def train(w, gamma):
    J = gamma.shape[2]
    K = 0
    L = len(w)
    for wl in w:
        for wli in wl:
            if not type(wli)==int:
                raise RuntimeError("w has bad word")
            K = max(K, wli+1)
    a = zeros([J, J])
    b = zeros([J])
    c = zeros([J, K])
    for j in range(0, J):
        for j_prime in range(0, J):
            for l in range(0, L):
                for i in range(0, len(w[l])-1):
                    a[j, j_prime] += gamma[l, i, j]*gamma[l, i+1, j_prime]
        a[j, :] /= sum(a[j, :])
        for l in range(0, L):
            b[j] += gamma[l, 0, j]
        for k in range(0, K):
            for l in range(0, L):
                for i in range(0, len(w[l])):
                    if w[l][i]==k:
                        c[j, k] += gamma[l, i, j]
        c[j, :] /= sum(c[j, :])
    b /= sum(b)
    return a, b, c

def likelihood(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    alpha = calculate_alpha(w, a, b, c)
    p = 1
    for l in range(0, L):
        pl = 0
        for j in range(0, J):
            pl += alpha[l, len(w[l])-1, j]
        p *= pl
    return p

def alternate_likelihood(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    beta = calculate_beta(w, a, b, c)
    p = 1
    for l in range(0, L):
        pl = 0
        for j in range(0, J):
            pl += b[j]*c[j, w[l][0]]*beta[l, 0, j]
        p *= pl
    return p

def sample(a, b, c, I):
    J = len(b)
    K = c.shape[1]
    j = choice(range(0, J), 1, p=b)[0]
    w = []
    for i in range(1, I+1):
        w.append(int(choice(range(0, K), 1, p=c[j, :])[0]))
        j = choice(range(0, J), 1, p=a[j, :])[0]
    return w

def samples(a, b, c, I, L):
    return [sample(a, b, c, I) for l in range(0, L)]

def model():
    a = array([[0.5, 0.5], [0, 1]])
    b = array([1, 0])
    c = array([[1, 0], [0, 1]])
    return a, b, c

def baum_welch_initial(w, J):
    gamma = random_gamma(w, J)
    a, b, c = train(w, gamma)
    return a, b, c

def baum_welch_step(w, a, b, c):
    gamma = calculate_gamma(w, a, b, c)
    a, b, c = train(w, gamma)
    return a, b, c

def baum_welch(w, J):
    a, b, c = baum_welch_initial(w, J)
    p = likelihood(w, a, b, c)
    print p
    while True:
        a, b, c = baum_welch_step(w, a, b, c)
        new_p = likelihood(w, a, b, c)
        print new_p
        if new_p<=p:
            return a, b, c
        p = new_p
