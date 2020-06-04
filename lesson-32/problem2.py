import math
import functools
from scipy import stats

class RandValue:
    def __init__(self, sample_type, value, rang):
        self.sample_type = sample_type
        self.value = value
        self.rang = rang
        
    def __repr__(self):
        return f'{self.sample_type}\t{self.value}\t{self.rang}'

a_s = [
    RandValue ('A', 30, 0),
    RandValue ('A', 28, 0),
    RandValue ('A', 46, 0),
    RandValue ('A', 42, 0),
    RandValue ('A', 35, 0),
    RandValue ('A', 33, 0),
    RandValue ('A', 44, 0),
    RandValue ('A', 43, 0),
    RandValue ('A', 31, 0),
    RandValue ('A', 38, 0),
]

b_s = [
    RandValue ('B', 26, 0),
    RandValue ('B', 38, 0),
    RandValue ('B', 39, 0),
    RandValue ('B', 28, 0),
    RandValue ('B', 30, 0),
    RandValue ('B', 27, 0),
    RandValue ('B', 32, 0),
    RandValue ('B', 35, 0),
]

u_s = a_s + b_s
u_s = sorted(u_s, key=lambda item: item.value)
u_s = map(lambda item, n: RandValue(item.sample_type, item.value, n), u_s, range(1, len(u_s)+1))
u_s = list(u_s)

count = 0
prev = None

for item in u_s:
    if prev is not None and prev.value != item.value:
        prev.rang = sum(range(prev.rang, prev.rang - count, -1)) / count
        count = 0

    prev = item
    count += 1
else:
    if count > 1:
        prev.rang = sum(range(prev.rang, prev.rang - count, -1)) / count

prev = None

for item in reversed(u_s):
    if prev is not None and prev.value == item.value:
        item.rang = prev.rang

    prev = item

W = functools.reduce(lambda acc, item: acc+item.rang if item.sample_type == 'B' else acc, u_s, 0)
M = (len(a_s)+len(b_s)+1) * len(b_s) / 2
D = (len(a_s)+len(b_s)+1) * len(a_s) * len(b_s) / 12

T = (W-M) / math.sqrt(D)

alpha = 0.05
left_edge = stats.norm.ppf(alpha/2)
right_edge = stats.norm.ppf(1 - alpha/2)
is_trusted = False if T < left_edge or right_edge < T else True

print('Ho: theta == 0')
print('Ha: theta != 0')

print(f'Значение статистики критерия = {round(T,2)}.')

if (is_trusted):
    print(f'''Статистика критерия попала в доверительную область,
тогда гипотеза Ho принимается на уровне значимости {alpha}.''')
else:
    print(f'''Статистика критерия не попала в доверительную область,
тогда гипотеза Ho отвергается в пользу Ha на уровне значимости {alpha}.''')

t_cdf = stats.norm.cdf(T)
p_value = min(2*t_cdf, 2-2*t_cdf)
print(f'P-значение = {round(p_value, 2)}.')
