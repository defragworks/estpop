import numpy as np


def ratios(pops1, pops2):
    totals1 = np.array(pops1[0]) + np.array(pops1[1])
    totals2 = np.array(pops2[0]) + np.array(pops2[1])

    change_ratio = np.delete(totals2, 0) / np.delete(totals1, -1)
    change_ratio = np.delete(change_ratio, -1)
    baby_ratio = totals2[0] / np.sum(np.array(pops1[1])[3:10])
    tail_ratio = totals2[-1] / np.sum(totals1[-2:])

    return change_ratio.tolist(), baby_ratio, tail_ratio


def simulate(pops, change_ratio, baby_ratio, tail_ratio):
    estimates = [[], []]

    mothers = np.sum(np.array(pops[1])[3:10])
    estimates[0].append(mothers * baby_ratio * (105 / (105 + 100)))
    estimates[1].append(mothers * baby_ratio * (100 / (105 + 100)))

    males = (np.array(pops[0])[:-2] * np.array(change_ratio)).tolist()
    females = (np.array(pops[1])[:-2] * np.array(change_ratio)).tolist()
    estimates[0] += males
    estimates[1] += females

    estimates[0].append(np.sum(pops[0][-2:]) * tail_ratio)
    estimates[1].append(np.sum(pops[1][-2:]) * tail_ratio)

    return estimates
