from math import exp

def make_tape(primal, factors, tapes, fanout, cotangent):
    return [primal, factors, tapes, fanout, cotangent]

def tape_primal(tape):
    [primal, factors, tapes, fanout, cotangent] = tape
    return primal

def tape_factors(tape):
    [primal, factors, tapes, fanout, cotangent] = tape
    return factors

def tape_tapes(tape):
    [primal, factors, tapes, fanout, cotangent] = tape
    return tapes

def tape_fanout(tape):
    [primal, factors, tapes, fanout, cotangent] = tape
    return fanout

def tape_cotangent(tape):
    [primal, factors, tapes, fanout, cotangent] = tape
    return cotangent

def set_tape_fanout(tape, fanout):
    tape[3] = fanout

def increment_tape_fanout(tape):
    set_tape_fanout(tape, tape_fanout(tape)+1)

def decrement_tape_fanout(tape):
    set_tape_fanout(tape, tape_fanout(tape)-1)

def set_tape_cotangent(tape, cotangent):
    tape[4] = cotangent

def is_tape(thing):
    return type(thing)==list

def lift_primal_to_tape(primal):
    return make_tape(primal, [], [], 0, 0)

def ad_plus(x, y):
    if is_tape(x):
        if is_tape(y):
            increment_tape_fanout(x)
            increment_tape_fanout(y)
            return make_tape(ad_plus(tape_primal(x), tape_primal(y)),
                             [1, 1],
                             [x, y],
                             0,
                             0)
        else:
            return ad_plus(x, lift_primal_to_tape(y))
    else:
        if is_tape(y):
            return ad_plus(lift_primal_to_tape(x), y)
        else:
            return x+y

def ad_minus(x, y):
    if is_tape(x):
        if is_tape(y):
            increment_tape_fanout(x)
            increment_tape_fanout(y)
            return make_tape(ad_minus(tape_primal(x), tape_primal(y)),
                             [1, -1],
                             [x, y],
                             0,
                             0)
        else:
            return ad_minus(x, lift_primal_to_tape(y))
    else:
        if is_tape(y):
            return ad_minus(lift_primal_to_tape(x), y)
        else:
            return x-y

def ad_times(x, y):
    if is_tape(x):
        if is_tape(y):
            increment_tape_fanout(x)
            increment_tape_fanout(y)
            return make_tape(ad_times(tape_primal(x), tape_primal(y)),
                             [tape_primal(y), tape_primal(x)],
                             [x, y],
                             0,
                             0)
        else:
            return ad_times(x, lift_primal_to_tape(y))
    else:
        if is_tape(y):
            return ad_times(lift_primal_to_tape(x), y)
        else:
            return x*y

def ad_divide(x, y):
    if is_tape(x):
        if is_tape(y):
            increment_tape_fanout(x)
            increment_tape_fanout(y)
            return make_tape(ad_divide(tape_primal(x), tape_primal(y)),
                             [ad_divide(tape_primal(y),
                                        ad_times(tape_primal(y),
                                                 tape_primal(y))),
                              ad_divide(ad_minus(0, tape_primal(x)),
                                        ad_times(tape_primal(y),
                                                 tape_primal(y)))],
                             [x, y],
                             0,
                             0)
        else:
            return ad_divide(x, lift_primal_to_tape(y))
    else:
        if is_tape(y):
            return ad_divide(lift_primal_to_tape(x), y)
        else:
            return x/y

def ad_sqr(x):
    return ad_times(x, x)

def ad_exp(x):
    if is_tape(x):
        increment_tape_fanout(x)
        return make_tape(exp(tape_primal(x)),
                         [exp(tape_primal(x))],
                         [x],
                         0,
                         0)
    else:
        return exp(x)

def ad_gt(x, y):
    if is_tape(x):
        if is_tape(y):
            return ad_gt(tape_primal(x), tape_primal(y))
        else:
            return ad_gt(x, lift_primal_to_tape(y))
    else:
        if is_tape(y):
            return ad_gt(lift_primal_to_tape(x), y)
        else:
            return x>y

def ad_max(x, y):
    if ad_gt(x, y):
        return x
    else:
        return y

def reverse_sweep(cotangent, tape):
    set_tape_cotangent(tape, tape_cotangent(tape)+cotangent)
    decrement_tape_fanout(tape)
    if tape_fanout(tape)==0:
        cotangent = tape_cotangent(tape)
        for factor, tape in zip(tape_factors(tape), tape_tapes(tape)):
            reverse_sweep(cotangent*factor, tape)

def derivative(f):
    def inner(x):
        input = lift_primal_to_tape(x)
        output = f(input)
        increment_tape_fanout(output)
        reverse_sweep(1, output)
        return tape_cotangent(input)
    return inner

def f1(x):
    return ad_times(x, x)

def f2(x):
    return ad_times(x, ad_times(x, x))

def f3(x):
    return ad_plus(ad_times(2, ad_times(x, ad_times(x, x))),
                   ad_times(4, ad_times(x, x)))

def gradient(f):
    def inner(xs):
        inputs = [lift_primal_to_tape(x) for x in xs]
        output = f(inputs)
        increment_tape_fanout(output)
        reverse_sweep(1, output)
        return [tape_cotangent(input) for input in inputs]
    return inner

def f4(x):
    return ad_plus(ad_times(x[0], x[0]),
                   ad_times(x[1], ad_times(x[1], x[1])))
