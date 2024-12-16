from random import shuffle

def bubble_sort(array):
    for i in range(len(array)):
        for n in range(0, len(array) - i - 1):
            if array[n] > array[n+1]:
                array[n], array[n+1] = array[n+1], array[n]
    return array

array = [8, 3, 2, 1, 5]

print('array:', array)
print('product:', bubble_sort(array))
