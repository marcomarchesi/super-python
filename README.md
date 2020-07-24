# python-python
All I need on Python

[Coding Style](#Coding-Style)  
[Truth Value Testing](#Truth-Value-Testing)  
[String vs Bytes](#Strings-vs-Bytes)  
[Threading](#Threading)  
[Functions](#Functions)  
[String Templates](#String-Templates)  
[Built-in Functions](#Built-in-Functions)  
[itertools module](#itertools-module)  
[Logging](#Logging)

## Coding Style
- to follow PEP8

## Truth Value Testing
- all objects are true by default apart empty lists, dictionaries and sets, `None` and `False` (of course)

## Strings vs Bytes
- use `byte_data.decode('utf-8)` to convert to `string`
- use `string_data.encode()` to convert to bytes


## Threading
- multiple processes run and share the same Python Interpreter (because of Global Interpreter Lock)
- they run in turns, not concurrently, at least on CPython (standard interpreter)
- CPython is bound on GIL
- When to use it:
1. if the task needs to wait long for external resources or events
2. to simplify design

```python
import threading
import time


def thread_function(name):
    print('hello world, thread {}'.format(name))
    time.sleep(2)
    print('hello world')


if __name__ == "__main__":
    
    x = threading.Thread(target=thread_function, args=(1,))
    # start the thread
    x.start()
    # wait for the thread to finish
    x.join()
    print('it''s over')
```

- `Daemon` threads run in background and they are killed once the main program is over.

```python
x = threading.Thread(target=thread_function, args=(1,), daemon=True)
```

- `.join()` makes the main thread waits for the secondary thread to complete
- threads can run in an unpredictable order, decided by the OS
- to instance multiple threads we can use `ThreadPoolExecutor`:

```python
import concurrent.futures

# [rest of code]

if __name__ == "__main__":

    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        executor.map(thread_function, range(3))  # instancing three threads and join each of them
```

- [ALERT] `ThreadPoolExecutor` can hide exceptions raised from a thread, for example if we pass an argument to a thread with zero arguments.
- **Race conditions** happen when two or more threads share data
- ** Locks ** help synchronising threads

## Functions
```python
def do_something(*args, **kwargs):  # positional and named arguments
    pass
```

## String Templates
- More powerful than `"Hello {}".format("World")` or `"Hello %s" % "World"`.  
- you can use a `dictionary` alternatively.  
```python
from string import Template

templ = Template("Hello ${what}")
print (templ.substitute(what="World"))
```

## Built-in Functions

```python
list1 = [1,2,3,4,0,6]

print(any(list1)) #True
print(all(list1)) #False
print(sum(list1)) #16
print(min(list1)) #0
print(max(list1)) #6
```

### Iterators

```python
days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
days_ita = ['Dom', 'Lun', 'Mar', 'Mer', 'Gio', 'Ven', 'Sab']
# Classic iteration
for d in days:
    print(d)
# or enumerating
for index, d in enumerate(days):
    print(index, d)
# with zip it merges two lists and each element is a tuple
for d in zip(days, days_ita):
    print(d)
# with iterators
i = iter(days)
print(next(i)) #Sun
print(next(i)) #Mon
print(next(i)) #Tue
```

### Transform functions

- `filter(callable_func, iterable)`
```python
days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

def filter_func(x):
    if x[0] == 'M': #check any item which starts with 'M'
        return True
    return False

not_m = filter(filter_func, days) #filter days by filter_func criteria
print(next(not_m)) #Mon
```

- `map(callable_func, iterable)`  
```python
numbers = [1,34,6,76,44,8]

def map_func(x):
    return x+1

items = list(map(map_func, numbers))
print(items) #[2, 35, 7, 77, 45, 9]
```

- other good ones: `sorted()`

## itertools module
 - part of the Python standard library

 - `cycle`
 ```python
 import itertools

numbers = [1,34,6]
i = itertools.cycle(numbers)
print(next(i)) #1
print(next(i)) #34
print(next(i)) #6
print(next(i)) #1
```
- `count`
```python
count = itertools.count(3,100) #start, step
print(next(count)) #3
print(next(count)) #103
print(next(count)) #203
```
- `accumulate`
Each element is the sum (by default) of the current and the previous items
```python
numbers = [1,34,6,76,44,8]
acc = itertools.accumulate(numbers)
print(list(acc)) #[1, 35, 41, 117, 161, 169]
```
but we can use also different operations:
```python
numbers = [1,34,6,76,44,8]
acc = itertools.accumulate(numbers, max)
print(list(acc)) #[1, 34, 34, 76, 76, 76]
```
- `chain`
Create a chain of sequences
```python
acc = itertools.chain("ABC", "123")
print(list(acc)) 
```

- `dropwhile` and `takewhile`
- `dropwhile` ignore values until the predicate in the test function is satisfied
- `takewhile` include values while the predicate in the test function is satisfied
```python
numbers = [10,34,6,76,44,8]

def test_func(x):
    return x > 9

print(list(itertools.dropwhile(test_func, numbers)))
# [6, 76, 44, 8]
print(list(itertools.takewhile(test_func, numbers)))
# [10, 34]
```

## Docstring
- callable with `[VALUE].__doc__`. More on docstring style on PEP 257.

```python
def good_func(arg1, arg2=None):
    '''
    good_func(arg1, arg2=None) --> print "Hello World"

    Parameters:
        arg1: first argument
        arg2: second argument. Default to None
    '''
    print("Hello World")

print(good_func.__doc__)
```

## Variable arguments
- We add a `*` to make the argument variable. Vars come after all the other arguments.

```python
def addition(*args):

    result = 0
    for arg in args:
        result += arg
    return result

numbers = [2,3,4,5,6]

print(addition(2,3,4,5,6)) #20
print(addition(*numbers)) #20 by calling the list
```
- possible drawback: if we change the signature of the function all the calls to the function need to change.

## Keyword-only arguments
- they stand after the positional arguments
```python
def my_function(arg1, arg2, this_argument=False):
    print(arg1)
    print(arg2)
    print(this_argument)

my_function(2,"ciao", this_argument=True)
```

## mix of arguments
```python
def my_function(arg1, arg2, *args,  **kwargs):
    for arg in args:
        print(arg)
    for k in kwargs.keys():
        print(kwargs[k])

my_function(2,'ciao', 'cats', 'dogs', this_argument=True, another_argument='Hello')
#cats
#dogs
#True
#Hello
```

## Lambda functions
- written as `lambda parameters : expression`
- define full functions inline, making everything more readable. But let's not overuse them.
```python
l = lambda x,y: x + y

print(l(3,4)) #7
```

## Basic and advanced collections

The 4 basic data collection types:
- `List`: mutable sequence of values
- `Tuple`: fixed sequence of values
- `Set`: sequence of distinct values
- `Dictionary`: unordered mutable collection of key, value pairs

More advanced ones are imported from `collections` module:
- `namedtuple`: tuple with named fields
- `OrderedDict`, `defaultdict`
- `Counter`: counts distinct values
- `deque`: double-ended list

### namedtuple
- useful for give names to tuple values, instead of access by index
- avoid on complex objects, better to use class
```python
import collections

Point = collections.namedtuple("Point", "x y")
p1 = Point(10,30)
print(p1)
print(p1.x)
print(p1._replace(x=25))
```

### defaultdict
- useful to avoid the check step if keys exist or not.
- don't use if we expect missing keys (and we want to check whether they exist)
```python
import collections

animals = ['tiger', 'gazelle', 'giraffe', 'lion', 'tiger','giraffe']

# classic dictionary
animals_counter = {}
for animal in animals:
    if animal in animals_counter.keys():
        animals_counter[animal] += 1
    else:
        animals_counter[animal] = 1
print(animals_counter)
#{'tiger': 2, 'gazelle': 1, 'giraffe': 2, 'lion': 1}

#with defaultdict no need for checking the keys 
default_animals_counter = collections.defaultdict(int) #int is the default type to use
for animal in animals:
    default_animals_counter[animal] += 1
print(dict(default_animals_counter))
#{'tiger': 2, 'gazelle': 1, 'giraffe': 2, 'lion': 1}
```

### Counter
- good for keeping count of data in lists
```python
from collections import Counter

animals = ['tiger', 'gazelle', 'giraffe', 'lion', 'tiger','giraffe']
other_animals = ['elephant','gazelle', 'kangaroo', 'lion', 'crocodile','giraffe']

counter = Counter(animals)
# how many giraffes are
print(counter['giraffe']) #2
# how many values totally
print(sum(counter.values())) #6
# merge two lists
counter.update(other_animals)
print(counter['giraffe']) #3
# get the two most common animals
print(counter.most_common(2)) #[('giraffe', 3), ('tiger', 2)]
```

### OrderedDict
- it keeps the order of key,values pairs inserted
- we can compare a OrderedDict with a regular dict, but the order doesn't matter anymore

### Deque
- pronounced "deck"
- it stands for double-ended queue
- elements can be removed from both ends
- memory efficient
```python
from collections import deque

animals = ['tiger', 'gazelle', 'giraffe', 'lion', 'tiger','giraffe']
collection = deque(animals)
collection.appendleft('elephant') #append on the left side
collection.pop() #remove from the right side
print(list(collection)) #['elephant', 'tiger', 'gazelle', 'giraffe', 'lion', 'tiger']
collection.rotate(-2) #rotate by -2 (to the left)
print(list(collection)) #['gazelle', 'giraffe', 'lion', 'tiger', 'elephant', 'tiger']
```

## Advanced Classes

### Enumerations
- no duplicate names but same values are allowed
- useful to avoid magic numbers
```python
from enum import Enum, auto

class Animal(Enum):
    GIRAFFE = 0
    TIGER = 1
    ELEPHANT = 2
    LION = auto()

animal = Animal.GIRAFFE
print(animal.name) #GIRAFFE
print(animal.value) #0
print(Animal.LION.value) #3
```

- by using the `unique` decorator, we prevent duplicated values
- by using the function `auto()` we assign a value automatically

### Class string functions
- We want to extend the control on how string and bytes types are represented
```python
class Profile:

    def __init__(self):
        self.name = "Marco"
        self.surname = "Marchesi"
        self.age = 43
    # let's override repr
    def __repr__(self):
        return "<Profile - class: name:{0} surname:{1} age:{2}".format(self.name, self.surname, self.age)
    # let's override bytes
    def __bytes__(self):
        value = "Profile:{0}:{1}:{2}".format(self.name, self.surname, self.age)
        return value.encode('utf-8')
    # we can also override str
    def __str__(self):
        pass

marco = Profile()
print(repr(marco)) #<Profile - class: name:Marco surname:Marchesi age:43
print(bytes(marco)) #b'Profile:Marco:Marchesi:43'
```

### Class attribute functions
- `__getattr__` is called only when the attribute can't be found
- `__getattribute__` is always called
- `__setattr__` when an attribute is set with a value
- `__delattr__` to delete the attribute
- `__dir__` when the user wants to discover the available attribute functions with `dir()`

They can be all overriden

### Class numerical operators
- they can be used to introduce operations between instances of a class
Example with addition operation:
```python
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)
    
    def __str__(self):
        return "Point({0},{1})".format(self.x, self.y)

p1 = Point(2,4)
p2 = Point(3,5)
p3 = p1 + p2
print(p3) #Point(5,9)
```

### Class comparison operators
- same concept as the numerical operators above
- we use some class attribute to compare, otherwise Python will raise an error
- we can use `sorted()` etc. as well

## Logging
- captures and records events while the app is running
- useful for debugging
- events can be categorized
- history of the program can be stored in files
- the output is highly customisable










