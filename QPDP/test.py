from random import choices, seed
from time import time

from qpdp import qpm, ldm

population = 5
isaac_method_constant = 0.88
test_count = 100000

queue = [i for i in range(1, population + 1)]

start_time = time()
ldm_prob_list = ldm(population, isaac_method_constant)
end_time = time()

ldm_time = end_time - start_time

start_time = time()
qpm_prob_list = qpm(population)
end_time = time()

qpm_time = end_time - start_time


ldm_tests = []
qpm_tests = []

for i in range(test_count):
    seed(i)
    qpm_pred = choices(queue, qpm_prob_list)[0]
    ldm_pred = choices(queue, ldm_prob_list)[0]

    ldm_tests.append(ldm_pred)
    qpm_tests.append(qpm_pred)

print('LDM Time:', ldm_time)
print('QPM Time:', qpm_time)

if ldm_time > qpm_time:
    print('QPM was faster by', ldm_time - qpm_time)
elif ldm_time < qpm_time:
    print('LDM was faster by', qpm_time - ldm_time)
else:
    print('Both methods took the exact same amount of time')

print()

print('LDM Average:', sum(ldm_tests) / len(ldm_tests))
print('QPM Average:', sum(qpm_tests) / len(qpm_tests))

print()

print('LDM One Count:', ldm_tests.count(1))
print('QPM One Count:', qpm_tests.count(1))

print()

print('LDM One Probability:', ldm_tests.count(1) / len(ldm_tests))
print('QPM One Probability:', qpm_tests.count(1) / len(qpm_tests))

print()

print('LDM Max Count:', ldm_tests.count(population))
print('QPM Max Count:', qpm_tests.count(population))

print()

print('LDM Weights:', ldm_prob_list)
print('QPM Weights:', qpm_prob_list)
