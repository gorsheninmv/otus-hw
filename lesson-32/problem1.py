import collections
import math
from scipy import stats

Tuple = collections.namedtuple('Tuple', ['success', 'total'])

a = Tuple(3, 175)
b = Tuple(32, 200)

p_diff = a.success/a.total - b.success/b.total
success = a.success + b.success
total = a.total + b.total
p_total = success/total
norm_koeff = math.sqrt(p_total * (1-p_total) * (1/a.total+1/b.total))
T = p_diff / norm_koeff

alpha = 0.05
left_edge = stats.norm.ppf(alpha/2)
right_edge = stats.norm.ppf(1 - alpha/2)

is_trusted = False if T < left_edge or right_edge < T else True

print('Ho: p1 = p2')
print('Ha: p1 != p2')

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
