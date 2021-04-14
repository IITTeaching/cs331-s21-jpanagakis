from unittest import TestCase
import random
import functools

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################
class Heap:
    def __init__(self, key=lambda x:x):
        self.data = []
        self.key  = key

    @staticmethod
    def _parent(idx):
        return (idx-1)//2

    @staticmethod
    def _left(idx):
        return idx*2+1

    @staticmethod
    def _right(idx):
        return idx*2+2
    
    def swap(self, parent, child):
        pval = self.data[parent]
        cval = self.data[child]
        self.data[parent] = cval
        self.data[child] = pval
    
    def pos_exists(self, n):
        return n < len(self)
    
    def heapify(self, idx=0):
        ### BEGIN SOLUTION
        if self.pos_exists(idx):
            lidx = self._left(idx)
            ridx = self._right(idx)
            val = self.key(self.data[idx])
        
            if self.pos_exists(lidx):
                if self.pos_exists(ridx):
                    lval = self.key(self.data[lidx])
                    rval = self.key(self.data[ridx])
                    if lval > val or rval > val:
                        if lval > rval:
                            self.swap(idx, lidx)
                            self.heapify(lidx)
                        else:
                            self.swap(idx, ridx)
                            self.heapify(ridx)
                else:
                    lval = self.key(self.data[lidx])
                    if lval > val:
                        self.swap(idx, lidx)
                        self.heapify(lidx)
            elif self.pos_exists(ridx):
                rval = self.data[ridx]
                if rval > val:
                    self.swap(idx,ridx)
                    self.heapify(ridx)
        ### END SOLUTION
    
    def trickle_up(self, n):
        if n > 0:
            pidx = self._parent(n)
            pval = self.key(self.data[pidx])
            curval = self.key(self.data[n])
            if pval < curval:
                self.swap(pidx, n)
                self.trickle_up(pidx)
    
    def add(self, x):
        ### BEGIN SOLUTION
        self.data.append(x)
        self.trickle_up(len(self.data)-1)
        ### END SOLUTION

    def peek(self):
        return self.data[0]

    def pop(self):
        ret = self.data[0]
        self.data[0] = self.data[len(self.data)-1]
        del self.data[len(self.data)-1]
        self.heapify()
        return ret

    def __iter__(self):
        return self.data.__iter__()

    def __bool__(self):
        return len(self.data) > 0

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return repr(self.data)

################################################################################
# 1. IMPLEMENT THIS HEAP
################################################################################

# (6 point)
def test_key_heap_1():
    from unittest import TestCase
    import random

    tc = TestCase()
    h = Heap()

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [97, 61, 65, 49, 51, 53, 62, 5, 38, 33])

# (6 point)
def test_key_heap_2():
    tc = TestCase()
    h = Heap(lambda x:-x)

    random.seed(0)
    for _ in range(10):
        h.add(random.randrange(100))

    tc.assertEqual(h.data, [5, 33, 53, 38, 49, 65, 62, 97, 51, 61])

# (6 points)
def test_key_heap_3():
    tc = TestCase()
    h = Heap(lambda s:len(s))

    h.add('hello')
    h.add('hi')
    h.add('abracadabra')
    h.add('supercalifragilisticexpialidocious')
    h.add('0')

    tc.assertEqual(h.data,
                   ['supercalifragilisticexpialidocious', 'abracadabra', 'hello', 'hi', '0'])

# (6 points)
def test_key_heap_4():
    tc = TestCase()
    h = Heap()

    random.seed(0)
    lst = list(range(-1000, 1000))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in range(999, -1000, -1):
        tc.assertEqual(x, h.pop())

# (6 points)
def test_key_heap_5():
    tc = TestCase()
    h = Heap(key=lambda x:abs(x))

    random.seed(0)
    lst = list(range(-1000, 1000, 3))
    random.shuffle(lst)

    for x in lst:
        h.add(x)

    for x in reversed(sorted(range(-1000, 1000, 3), key=lambda x:abs(x))):
        tc.assertEqual(x, h.pop())

################################################################################
# 2. MEDIAN
################################################################################
def running_medians(iterable):
    ### BEGIN SOLUTION
    maxHeap = Heap()
    minHeap = Heap(lambda x:-x)
    medians = []
    
    for i, x in enumerate(iterable):
        if not minHeap and not maxHeap:
            minHeap.add(x) 
            medians.append(x) 
        elif len(minHeap) > len(maxHeap):
            if x > medians[i-1]:
                maxHeap.add(minHeap.pop())
                minHeap.add(x)
            else:
                maxHeap.add(x) 
            medians.append((maxHeap.peek() + minHeap.peek())/2)
        elif len(minHeap) < len(maxHeap):
            if x < medians[i-1]:
                minHeap.add(maxHeap.pop())
                maxHeap.add(x)
            else:
                minHeap.add(x) 
            medians.append((maxHeap.peek() + minHeap.peek())/2)
        else:
            if x > medians[i-1]:
                minHeap.add(x)
                medians.append(minHeap.peek())
            else:
                maxHeap.add(x)
                medians.append(maxHeap.peek())
    return medians
    ### END SOLUTION

################################################################################
# TESTS
################################################################################
def running_medians_naive(iterable):
    values = []
    medians = []
    for i, x in enumerate(iterable):
        values.append(x)
        values.sort()
        if i%2 == 0:
            medians.append(values[i//2])
        else:
            medians.append((values[i//2] + values[i//2+1]) / 2)
    return medians

# (13 points)
def test_median_1():
    tc = TestCase()
    tc.assertEqual([3, 2.0, 3, 6.0, 9], running_medians([3, 1, 9, 25, 12]))

# (13 points)
def test_median_2():
    tc = TestCase()
    vals = [random.randrange(10000) for _ in range(1000)]
    tc.assertEqual(running_medians_naive(vals), running_medians(vals))

# MUST COMPLETE IN UNDER 10 seconds!
# (14 points)
def test_median_3():
    tc = TestCase()
    vals = [random.randrange(100000) for _ in range(100001)]
    m_mid   = sorted(vals[:50001])[50001//2]
    m_final = sorted(vals)[len(vals)//2]
    running = running_medians(vals)
    tc.assertEqual(m_mid, running[50000])
    tc.assertEqual(m_final, running[-1])

################################################################################
# 3. TOP-K
################################################################################
def topk(items, k, keyf):
    ### BEGIN SOLUTION
    heap = Heap(keyf)
    klst = []
    for i in items:
        heap.add(i)
    for i in range(k):
        klst.append(heap.pop())
    return klst
    ### END SOLUTION

################################################################################
# TESTS
################################################################################
def get_age(s):
    return s[1]

def naive_topk(l,k,keyf):
    revkey = lambda x: keyf(x) * -1
    return sorted(l, key=revkey)[0:k]

# (30 points)
def test_topk_students():
    tc = TestCase()
    students = [ ('Peter', 33), ('Bob', 23), ('Alice', 21), ('Gertrud', 53) ]

    tc.assertEqual(naive_topk(students, 2, get_age),
                   topk(students, 2, get_age))

    tc.assertEqual(naive_topk(students, 1, get_age),
                   topk(students, 1, get_age))

    tc.assertEqual(naive_topk(students, 3, get_age),
                   topk(students, 3, get_age))

################################################################################
# TEST HELPERS
################################################################################
def say_test(f):
    print(80 * "*" + "\n" + f.__name__)

def say_success():
    print("SUCCESS")

################################################################################
# MAIN
################################################################################
def main():
    for t in [test_key_heap_1,
              test_key_heap_2,
              test_key_heap_3,
              test_key_heap_4,
              test_key_heap_5,
              test_median_1,
              test_median_2,
              test_median_3,
              test_topk_students
              ]:
        say_test(t)
        t()
        say_success()

if __name__ == '__main__':
    main()
