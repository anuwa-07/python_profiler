
import time
from code_profiler import CodeProfiler


# Make a new instance of the CodeProfiler class
test_profiler = CodeProfiler(
    file_path='/Users/anuruddha/Desktop/profiler',
    log_details=True,
)


# Use the line_profiler_time() decorator to profile the function execution time and write the profiling data to a file.
@test_profiler.line_profiler_time()
def say_myname(name: str) -> None:
    names: list = []
    big_list = []
    for i in range(1000):
        names.append("Hello World!!1")
    #
    for i in range(1000):
        big_list.append(names)
    #
    time.sleep(0.2)
    print(f"You are {name}")
    print("You are god damn right!!")


# Use the line_profiler_memory() decorator to profile the function memory usage and write the profiling data to a file.
@test_profiler.line_profiler_memory()
def memory_intensive_function(n) -> int:
    numbers: list = []
    for i in range(n):
        numbers.append(i)

    # Sum all the integers in the list
    total = sum(numbers)
    return total


if __name__ == "__main__":
    # Execute the functions to be profiled.
    say_myname("Heisenberg")
    memory_intensive_function(1000)
