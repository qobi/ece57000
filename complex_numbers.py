from math import sqrt

def make_complex_number(real, imaginary):
    return (real, imaginary)

def complex_number_real(complex_number):
    (real, imaginary) = complex_number
    return real

def complex_number_imaginary(complex_number):
    (real, imaginary) = complex_number
    return imaginary

def is_complex_number(thing):
    return type(thing)==tuple

def lift_real_to_complex(real):
    return make_complex_number(real, 0)

def complex_plus(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return make_complex_number(complex_number_real(x)+
                                       complex_number_real(y),
                                       complex_number_imaginary(x)+
                                       complex_number_imaginary(y))
        else:
            return complex_plus(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return complex_plus(lift_real_to_complex(x), y)
        else:
            return x+y

def complex_minus(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return make_complex_number(complex_number_real(x)-
                                       complex_number_real(y),
                                       complex_number_imaginary(x)-
                                       complex_number_imaginary(y))
        else:
            return complex_minus(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return complex_minus(lift_real_to_complex(x), y)
        else:
            return x-y

def complex_times(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return make_complex_number(
                complex_number_real(x)*complex_number_real(y)-
                complex_number_imaginary(x)*complex_number_imaginary(y),
                complex_number_real(x)*complex_number_imaginary(y)+
                complex_number_imaginary(x)*complex_number_real(y))
        else:
            return complex_times(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return complex_times(lift_real_to_complex(x), y)
        else:
            return x*y

def complex_divide(x, y):
    if is_complex_number(x):
        if is_complex_number(y):
            return make_complex_number(
                (complex_number_real(x)*complex_number_real(y)+
                 complex_number_imaginary(x)*complex_number_imaginary(y))/
                (complex_number_real(y)*complex_number_real(y)+
                 complex_number_imaginary(y)*complex_number_imaginary(y)),
                (complex_number_imaginary(x)*complex_number_real(y)-
                 complex_number_real(x)*complex_number_imaginary(y))/
                (complex_number_real(y)*complex_number_real(y)+
                 complex_number_imaginary(y)*complex_number_imaginary(y)))
        else:
            return complex_divide(x, lift_real_to_complex(y))
    else:
        if is_complex_number(y):
            return complex_divide(lift_real_to_complex(x), y)
        else:
            return x/y

def complex_sqrt(x):
    if is_complex_number(x):
        r = sqrt(complex_number_real(x)*complex_number_real(x)+
                 complex_number_imaginary(x)*complex_number_imaginary(x))
        if complex_number_imaginary(x)<0:
            return make_complex_number(
                sqrt((complex_number_real(x)+r)/2),
                -sqrt((r-complex_number_real(x))/2))
        else:
            return make_complex_number(
                sqrt((complex_number_real(x)+r)/2),
                sqrt((r-complex_number_real(x))/2))
    elif x>=0:
        return sqrt(x)
    else:
        return make_complex_number(0, sqrt(-x))

def quadratic(a, b, c, x):
    return complex_plus(complex_times(a, complex_times(x, x)),
                        complex_plus(complex_times(b, x), c))

def quadratic_roots(a, b, c):
    return (complex_divide(
        complex_plus(
            complex_minus(0, b),
            complex_sqrt(complex_minus(complex_times(b, b),
                                       complex_times(4, complex_times(a, c))))),
        complex_times(2, a)),
            complex_divide(
                complex_minus(
                    complex_minus(0, b),
                    complex_sqrt(
                        complex_minus(complex_times(b, b),
                                      complex_times(4, complex_times(a, c))))),
                complex_times(2, a)))
