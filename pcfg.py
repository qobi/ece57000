from numpy import sum, array, zeros, concatenate
from numpy.random import random, choice

def check(w, a, b, c):
    L = len(w)
    I = max([len(w[l]) for l in range(0, L)])
    J = len(b)
    K = c.shape[1]
    if len(a.shape)!=3 or a.shape[0]!=J or a.shape[1]!=J or a.shape[2]!=J:
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
    alpha = zeros([L, I, I, J])
    for l in range(0, L):
        for j in range(0, J):
            for i in range(0, len(w[l])):
                alpha[l, i, i, j] = c[j, w[l][i]]
        for d in range(2, len(w[l])+1):
            for i1 in range(0, len(w[l])-d+1):
                i2 = i1+d-1
                for j in range(0, J):
                    for j1 in range(0, J):
                        for j2 in range(0, J):
                            for i in range(i1, i2):
                                alpha[l, i1, i2, j] += (
                                    a[j, j1, j2]*
                                    alpha[l, i1, i, j1]*
                                    alpha[l, i+1, i2, j2])
    return alpha

def calculate_beta(w, a, b, c, alpha):
    I, J, K, L = check(w, a, b, c)
    beta = zeros([L, I, I, J])
    for l in range(0, L):
        for j in range(0, J):
            beta[l, 0, len(w[l])-1, j] = b[j]
        for d in range(len(w[l])-1, 0, -1):
            for i1 in range(0, len(w[l])-d+1):
                i2 = i1+d-1
                for j in range(0, J):
                    for j1 in range(0, J):
                        for j2 in range(0, J):
                            for i in range(0, i1):
                                beta[l, i1, i2, j] += (
                                    a[j1, j2, j]*
                                    alpha[l, i, i1-1, j2]*
                                    beta[l, i, i2, j1])
                            for i in range(i2+1, len(w[l])):
                                beta[l, i1, i2, j] += (
                                    a[j1, j, j2]*
                                    alpha[l, i2+1, i, j2]*
                                    beta[l, i1, i, j1])
    return beta

def random_gamma(w, J):
    L = len(w)
    I = max([len(w[l]) for l in range(0, L)])
    gamma = zeros([L, I, I, J])
    for l in range(0, L):
        for i1 in range(0, len(w[l])):
            for i2 in range(i1, len(w[l])):
                for j in range(0, J):
                    gamma[l, i1, i2, j] = random()
                gamma[l, i1, i2, :] /= sum(gamma[l, i1, i2, :])
    return gamma

def calculate_gamma(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    alpha = calculate_alpha(w, a, b, c)
    beta = calculate_beta(w, a, b, c, alpha)
    gamma = zeros([L, I, I, J])
    for l in range(0, L):
        for i1 in range(0, len(w[l])):
            for i2 in range(i1, len(w[l])):
                for j in range(0, J):
                    gamma[l, i1, i2, j] = alpha[l, i1, i2, j]*beta[l, i1, i2, j]
                if sum(gamma[l, i1, i2, :])!=0:
                    gamma[l, i1, i2, :] /= sum(gamma[l, i1, i2, :])
    return gamma

def train(w, gamma):
    J = gamma.shape[3]
    K = 0
    L = len(w)
    for wl in w:
        for wli in wl:
            if not type(wli)==int:
                raise RuntimeError("w has bad word")
            K = max(K, wli+1)
    a = zeros([J, J, J])
    b = zeros([J])
    c = zeros([J, K])
    for j in range(0, J):
        for j1 in range(0, J):
            for j2 in range(0, J):
                for l in range(0, L):
                    for i1 in range(0, len(w[l])-1):
                        for i3 in range(i1+1, len(w[l])):
                            for i2 in range(i1, i3):
                                a[j, j1, j2] += (
                                    gamma[l, i1, i3, j]*
                                    gamma[l, i1, i2, j1]*
                                    gamma[l, i2+1, i3, j2])
        for l in range(0, L):
            b[j] += gamma[l, 0, len(w[l])-1, j]
        for k in range(0, K):
            for l in range(0, L):
                for i in range(0, len(w[l])):
                    if w[l][i]==k:
                        c[j, k] += gamma[l, i, i, j]
        denominator = sum(c[j, :])+sum(a[j, :, :])
        c[j, :] /= denominator
        a[j, :, :] /= denominator
    b /= sum(b)
    return a, b, c

def likelihood(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    alpha = calculate_alpha(w, a, b, c)
    p = 1
    for l in range(0, L):
        pl = 0
        for j in range(0, J):
            pl += b[j]*alpha[l, 0, len(w[l])-1, j]
        p *= pl
    return p

def alternate_likelihood(w, a, b, c):
    I, J, K, L = check(w, a, b, c)
    beta = calculate_beta(w, a, b, c, calculate_alpha(w, a, b, c))
    p = 1
    i = 0
    for l in range(0, L):
        pl = 0
        for j in range(0, J):
            pl += c[j, w[l][i]]*beta[l, i, i, j]
        p *= pl
    return p

def sample(a, b, c):
    J = len(b)
    K = c.shape[1]
    j = choice(range(0, J), 1, p=b)[0]
    def s(j):
        r = int(choice(range(0, K+J**2),
                       1,
                       p=concatenate((c[j, :], a[j, :, :].flatten())))[0])
        if r<K:
            return [r]
        else:
            return s((r-K)/J)+s((r-K)%J)
    return s(j)

def samples(a, b, c, L):
    return [sample(a, b, c) for l in range(0, L)]

def model1():
    a = array([[[1./3]]])
    b = array([1])
    c = array([[1./3, 1./3]])
    return a, b, c

def model2():
    a = array([[[0, 0], [0, 1]], [[0, 0], [0, 1./3]]])
    b = array([1, 0])
    c = array([[0, 0], [1./3, 1./3]])
    return a, b, c

def model3():
    a = array([[[0, 0, 0, 0], [0, 0, 0, 0.7], [0, 0, 0, 0,], [0, 0, 0, 0]],
               [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0,], [0, 0, 0, 0]],
               [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0,], [0, 0, 0, 0]],
               [[0, 0, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0,], [0, 0, 0, 0]]])
    b = array([1, 0, 0, 0])
    c = array([[0, 0, 0.3], [1, 0, 0], [0, 1, 0], [0, 0, 0]])
    return a, b, c

def baker_lari_young_initial(w, J):
    gamma = random_gamma(w, J)
    a, b, c = train(w, gamma)
    return a, b, c

def baker_lari_young_step(w, a, b, c):
    gamma = calculate_gamma(w, a, b, c)
    a, b, c = train(w, gamma)
    return a, b, c

def baker_lari_young(w, J):
    a, b, c = baker_lari_young_initial(w, J)
    p = likelihood(w, a, b, c)
    print p
    while True:
        a, b, c = baker_lari_young_step(w, a, b, c)
        new_p = likelihood(w, a, b, c)
        print new_p
        if new_p<=p:
            return a, b, c
        p = new_p
