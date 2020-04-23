**estpop** is a Python package providing population forecasting from historical data. This method is based on cohort change ratio[1].

# Sample Code

## Change Ratio

```python
import numpy as np
import openpyxl
import estpop

sheet = openpyxl.load_workbook('data.xlsx').worksheets[0]

pops = {}
for i in range(1, sheet.max_row):
    code = sheet.cell(i+1, 3).value

    if not code in pops:
        pops[code] = []

    males, females = [], []
    for j in range(29, 50):
        males.append(sheet.cell(i+1, j).value)
        females.append(sheet.cell(i+1, j+22).value)
    pops[code].append([males, females])

ratios = {}
for k, v in pops.items():
    change_ratios, baby_ratios, tail_ratios = [], [], []
    try:
        for i in range(len(v) - 5):
            change_ratio, baby_ratio, tail_ratio = estpop.ratios(v[i], v[i+5])
            change_ratios.append(change_ratio)
            baby_ratios.append(baby_ratio)
            tail_ratios.append(tail_ratio)

        ratios[k] = {
            'change_ratio': np.mean(change_ratios, axis=0).tolist(),
            'baby_ratio': float(np.mean(baby_ratios)),
            'tail_ratio': float(np.mean(tail_ratios))
        }
    except:
        pass
```

## Simulation

```python
import openpyxl
import estpop

f = open('result.csv', mode='w')
f.write('code,year\n')

for k, v in pops.items():
    if k in [411, 421, 521]:
        change_ratio = ratios[0]['change_ratio']
        baby_ratio = ratios[0]['baby_ratio']
        tail_ratio = ratios[0]['tail_ratio']
    else:
        change_ratio = ratios[k]['change_ratio']
        baby_ratio = ratios[k]['baby_ratio']
        tail_ratio = ratios[k]['tail_ratio']
    
    try:
        year = 2020
        estimates = v[5]

        for i in range(7):
            estimates = estpop.simulate(estimates, change_ratio,
                                        baby_ratio, tail_ratio)
            f.write('%s,%s,%s,%s\n' % (k, year+i*5,
                                       ','.join(map(str, estimates[0])),
                                       ','.join(map(str, estimates[1]))))
    except:
        print(k)

f.close()
```

# References

1. Einoshin SUZUKI, Kaoru MORI, Koichi NAGASE, Masatoshi TAMAMURA, Ikuyo KANEKO: The Development of the Future Predictive Model of 'Potentially Disappearing Neighborhood Associations' Using Demographic Data of the Neighborhood Association Base, Journal of the Japan Association of Regional Development and Vitalization, Vol.6, pp.20-30, 2015.
