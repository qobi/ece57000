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

def dual_plus(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(dual_plus(dual_number_primal(x),
                                              dual_number_primal(y)),
                                    dual_plus(dual_number_tangent(x),
                                              dual_number_tangent(y)))
        else:
            return dual_plus(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return dual_plus(lift_primal_to_dual(x), y)
        else:
            return x+y

def dual_minus(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(dual_minus(dual_number_primal(x),
                                               dual_number_primal(y)),
                                    dual_minus(dual_number_tangent(x),
                                               dual_number_tangent(y)))
        else:
            return dual_minus(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return dual_minus(lift_primal_to_dual(x), y)
        else:
            return x-y

def dual_times(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(
                dual_times(dual_number_primal(x), dual_number_primal(y)),
                dual_plus(dual_times(dual_number_primal(x),
                                     dual_number_tangent(y)),
                          dual_times(dual_number_tangent(x),
                                     dual_number_primal(y))))
        else:
            return dual_times(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return dual_times(lift_primal_to_dual(x), y)
        else:
            return x*y

def dual_divide(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return make_dual_number(
                dual_divide(dual_number_primal(x), dual_number_primal(y)),
                dual_divide(
                    dual_minus(dual_times(dual_number_primal(y),
                                          dual_number_tangent(x)),
                               dual_times(dual_number_primal(x),
                                          dual_number_tangent(y))),
                    dual_times(dual_number_primal(y), dual_number_primal(y))))
        else:
            return dual_divide(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return dual_divide(lift_primal_to_dual(x), y)
        else:
            return x/y

def dual_sqr(x):
    return dual_times(x, x)

def dual_exp(x):
    if is_dual_number(x):
        return make_dual_number(
            exp(dual_number_primal(x)),
            dual_times(dual_number_tangent(x), exp(dual_number_primal(x))))
    else:
        return exp(x)

def dual_gt(x, y):
    if is_dual_number(x):
        if is_dual_number(y):
            return dual_gt(dual_number_primal(x), dual_number_primal(y))
        else:
            return dual_gt(x, lift_primal_to_dual(y))
    else:
        if is_dual_number(y):
            return dual_gt(lift_primal_to_dual(x), y)
        else:
            return x>y

def dual_max(x, y):
    if dual_gt(x, y):
        return x
    else:
        return y

def derivative(f):
    def inner(x):
        return dual_number_tangent(f(make_dual_number(x, 1)))
    return inner

def f1(x):
    return dual_times(x, x)

def f2(x):
    return dual_times(x, dual_times(x, x))

def f3(x):
    return dual_plus(dual_times(2, dual_times(x, dual_times(x, x))),
                     dual_times(4, dual_times(x, x)))

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
    return dual_plus(dual_times(x[0], x[0]),
                     dual_times(x[1], dual_times(x[1], x[1])))

def gradient(f):
    def inner(x):
        return [partial_derivative(f, i)(x) for i in range(0, len(x))]
    return inner
