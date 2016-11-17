from collections import defaultdict
import random
import json
import numpy

import click

class Trial(object):
    def __init__(self, pool_size, iteration, give_up_after):
        self.pool = [False] * pool_size
        self.pool[iteration % pool_size] = True
        self.pool_size = pool_size
        self.give_up_after = give_up_after

    def run(self):
        for i in range(self.give_up_after):
            if random.choice(self.pool):
                return i
        return self.give_up_after

def run_trials(pool_size, iterations, give_up_after=200):
    answers = defaultdict(int)
    for i in range(iterations):
        t = Trial(pool_size, i, give_up_after)
        answers[t.run()] += 1
    return answers

def analyze(trial):
    result = expand(trial)
    m = max(result)
    count_at_max = len([x for x in result if x == m])
    print "  - Mean: {}, Median: {}, Std dev: {}, Variance: {}, Max: {}, Count at max: {} ({:.3}%)".format(
            numpy.mean(result),
            numpy.median(result),
            numpy.std(result),
            numpy.var(result),
            m,
            count_at_max,
            count_at_max / len(result)
            )
    for x in range(10, 100, 10):
        print "  - {:.3}% at/under {}".format(x, result[(x * len(result)) // 100])

def expand(trial):
    answer = []
    for k, v in trial.items():
        answer += [k] * v
    return answer

@click.command()
@click.option("--iterations", default=5000000)
def main(iterations=5000):
    random.seed()
    trials_by_pool = dict()
    for x in (10, 20, 30, 40, 50):
        result = run_trials(x, iterations)
        trials_by_pool[x] = result
        print "Trials with pool_size={}".format(x)
        analyze(result)
    with open('results.json', 'w') as out:
        json.dump(trials_by_pool, out)

if __name__ == '__main__':
    main()
