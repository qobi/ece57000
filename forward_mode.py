# A simple minimal implementation of forward-mode automatic differentiation
# (AD).
# This does not handle nesting.

# Beda, L.M., Korolev, L.N., Sukkikh, N.V., and Frolov, T.S., Programs for
# Automatic Differentiation for the Machine BESM, Institute for Precise
# Mechanics and Computation Techniques, Academy of Science, Moscow, USSR,
# 1959.

# Wengert, R.E., A simple automatic derivative evaluation program,
# CACM, 7(8):463-4, 1964.

# Siskind, J.M. and Pearlmutter, B.A., Nesting Forward-Mode AD in a
# Functional Framework, HOSC, 21(4):361-76, 2008.

# A real implementation would use reverse-mode AD. We use forward mode just
# for pedagogical purposes so that we can derive everything easily from
# first principles.

from math import exp

def make_dual_number(primal, tangent):
    return (primal, tangent)

def dual_number_primal(dual_number):
    (primal, tangent) = dual_number
    return primal

def dual_number_tangent(dual_number):
    (primal, tangent) = dual_number
    return tangent

def is_dual_number(thing):
    return type(thing)==tuple

def lift_primal_to_dual(primal):
    return make_dual_number(primal, 0)

def ad_plus(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(ad_plus(dual_number_primal(x),
                                            dual_number_primal(y)),
                                    ad_plus(dual_number_tangent(x),
                                            dual_number_tangent(y)))
        else:
            return ad_plus(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return ad_plus(lift_primal_to_dual(x), y)
        else:
            return x+y

def ad_minus(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(ad_minus(dual_number_primal(x),
                                             dual_number_primal(y)),
                                    ad_minus(dual_number_tangent(x),
                                             dual_number_tangent(y)))
        else:
            return ad_minus(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return ad_minus(lift_primal_to_dual(x), y)
        else:
            return x-y

def ad_times(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(
                ad_times(dual_number_primal(x), dual_number_primal(y)),
                ad_plus(ad_times(dual_number_primal(x),
                                 dual_number_tangent(y)),
                        ad_times(dual_number_tangent(x),
                                 dual_number_primal(y))))
        else:
            return ad_times(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return ad_times(lift_primal_to_dual(x), y)
        else:
            return x*y

def ad_divide(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(
                ad_divide(dual_number_primal(x), dual_number_primal(y)),
                ad_divide(
                    ad_minus(ad_times(dual_number_primal(y),
                                      dual_number_tangent(x)),
                             ad_times(dual_number_primal(x),
                                      dual_number_tangent(y))),
                    ad_times(dual_number_primal(y), dual_number_primal(y))))
        else:
            return ad_divide(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return ad_divide(lift_primal_to_dual(x), y)
        else:
            return x/y

def ad_sqr(x):
    return ad_times(x, x)

def ad_exp(x):
    if is_dual_number(x):
        return make_dual_number(
            exp(dual_number_primal(x)),
            ad_times(dual_number_tangent(x), exp(dual_number_primal(x))))
    else:
        return exp(x)

def ad_gt(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return ad_gt(dual_number_primal(x), dual_number_primal(y))
        else:
            return ad_gt(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return ad_gt(lift_primal_to_dual(x), y)
        else:
            return x>y

def ad_max(x, y):
    if ad_gt(x, y):
        return x
    else:
        return y

def derivative(f):
    def inner(x):
        return dual_number_tangent(f(make_dual_number(x, 1)))
    return inner

def f1(x):
    return ad_times(x, x)

def f2(x):
    return ad_times(x, ad_times(x, x))

def f3(x):
    return ad_plus(ad_times(2, ad_times(x, ad_times(x, x))),
                   ad_times(4, ad_times(x, x)))

def replace_ith(x, i, xi):
    result = []
    for j in range(0, len(x)):
        if j==i:
            result.append(xi)
        else:
            result.append(x[j])
    return result

def partial_derivative(f, i):
    def outer(x):
        def inner(xi):
            return f(replace_ith(x, i, xi))
        return derivative(inner)(x[i])
    return outer

def f4(x):
    return ad_plus(ad_times(x[0], x[0]),
                   ad_times(x[1], ad_times(x[1], x[1])))

def gradient(f):
    def inner(x):
        return [partial_derivative(f, i)(x) for i in range(0, len(x))]
    return inner
