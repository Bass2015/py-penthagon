import math

def ease_out_expo(x):
    return 1 if x == 1 else 1 - 2 **(-10 * x) 

def ease_out_elastic(x):
    c4 = (2 * math.pi) / 3;
    if (x == 0 or x == 1):
        return x
    return pow(2, -10 * x) * math.sin((x * 10 - 0.75) * c4) + 1;

def ease_out_circ(x):
    return (1-pow(x-1, 2))**2