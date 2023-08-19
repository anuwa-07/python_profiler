
# CUSTOM PYTHON PROFILER

## What is this repo about?
This repo is made to check function Performance and Memory Usages.
Python `Line-Profiler` and `Memory-Profiler` are used to check the performance and memory usage of the functions.


## How to use this repo as Lib?
0. Make a virtual environment using `python3 -m venv <env_name>` or `pipenv install`
1. Install the package using `pip install git+
2. Import the package using `import custom_profiler`
3. Use the package as shown in the example below.
   ```python
    from code_profiler import CodeProfiler
    profiler = CodeProfiler(
        file_path='<Path in Your local machine>',
        log_details=True,
    )
   
    # 01. To check the performance of a function ( time taken by each line of code in the function )
    @profiler.line_profiler_time()
    def test_function():
        #  Some code here...
    
   # 02. To check the memory usage of a function ( memory usage by each line of code in the function )
    @profiler.line_profiler_memory()
    def test_function():
        #  Some code here...
   #
   ##-# For more details, please check the example.py file in the repo.
    ```
4. Run the code and check the logs in the file path provided in the `CodeProfiler` class.
---

## What is mean from the results?

### 01. Time taken by each line of code in the function
```
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
    15                                           @test_profiler.line_profiler_time()
    16                                           def say_myname(name: str) -> None:
    17         1     147000.0 147000.0      0.1      names: list = []
    18         1          0.0      0.0      0.0      big_list = []
    19      1000      74000.0     74.0      0.0      for i in range(1000):
    20      1000      96000.0     96.0      0.0          names.append("Hello World!!1")
    21                                               #
    22      1000     104000.0    104.0      0.1      for i in range(1000):
    23      1000      80000.0     80.0      0.0          big_list.append(names)
    24                                               #
    25         1  202860000.0 202860000.0     99.7      time.sleep(0.2)
    26         1      25000.0  25000.0      0.0      print(f"You are {name}")
    27         1       2000.0   2000.0      0.0      print("You are god damn right!!")
```
What is mean from the above result?
- `Line #` - Line number of the code
- `Hits` - How many times the line of code is executed
- `Time` - Time taken by the line of code to execute
- `Per Hit` - Time taken by the line of code to execute per hit
- `% Time` - Percentage of time taken by the line of code to execute ( Important Point )
- `Line Contents` - Code in the line
---
### 02. Memory usage by each line of code in the function
```
Line #    Mem usage    Increment  Occurrences   Line Contents
=============================================================
    31     20.7 MiB     20.7 MiB           1   @test_profiler.line_profiler_memory()
    32                                         def memory_intensive_function(n) -> int:
    33     20.7 MiB      0.0 MiB           1       numbers: list = []
    34     20.8 MiB      0.0 MiB        1001       for i in range(n):
    35     20.8 MiB      0.0 MiB        1000           numbers.append(i)
    36                                         
    37                                             # Sum all the integers in the list
    38     20.8 MiB      0.0 MiB           1       total = sum(numbers)
    39     20.8 MiB      0.0 MiB           1       return total
```
What is mean from the above result?
- `Line #` - Line number of the code
- `Mem usage` - Memory usage by the line of code
- `Increment` - Memory usage increment by the line of code
- `Occurrences` - How many times the line of code is executed
- `Line Contents` - Code in the line
- `Important Point` - If the `Increment` is `0.0 MiB`, then the line of code is not using any memory.
---

## W A R N I N G ! ! !
> When you testing you code using this package, please make sure to remove the decorators from the functions after testing.
Otherwise, it will affect the performance of the code in production or in other environments. Because, 
this package will add some extra code to the functions to check the performance and memory usage of the functions.
---


