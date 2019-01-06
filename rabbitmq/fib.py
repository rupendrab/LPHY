from collections import defaultdict

def memoize(f):
    remembered = defaultdict(lambda: -1)
    def call_if_not_evaluated(n):
        calculated = remembered[n]
        if calculated != -1:
            return calculated
        else:
            val = f(n)
            remembered[n] = val
            return val
    return call_if_not_evaluated

@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

if __name__ == '__main__':
    for i in range(10):
        print("fib(%d) = %d" % (i, fib(i)))
