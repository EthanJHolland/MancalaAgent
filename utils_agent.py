import random

def find_optimal(choices, order):
    """ given a non-empty list of pairs (a, b) and either min or max returns (l, b*) where b* is the min/max b and l is all a paired with b* """
    assert order in [min, max]

    _, best_b = order(choices, key=lambda pair: pair[1], default=None)
    optimal_as = [a for a, b in choices if b == best_b]

    return optimal_as, best_b

def random_optimal(choices, order):
    optimal_as, best_b = find_optimal(choices, order)
    return random.choice(optimal_as), best_b