import os
import psutil
import logging
import line_profiler
from memory_profiler import memory_usage
import matplotlib.pyplot as plt

# Set up the logging
# TODO: add the file, if you need to log memeory usage
# logging.basicConfig(filename='memory_usage.log', level=logging.INFO, format='%(asctime)s - %(message)s')


def measure_memory_usage(funck):
    def wrapper(*args, **kwargs):
        process = psutil.Process(os.getpid())
        start_memory = process.memory_info().rss

        result = funck(*args, **kwargs)

        end_memory = process.memory_info().rss
        memory_usage_bytes = end_memory - start_memory

        logging.info(f"Function '{funck.__name__}' memory usage: {memory_usage_bytes} bytes")

        # Create and save the memory usage chart
        profiler = line_profiler.LineProfiler(funck)
        profiler.enable()
        profiler.disable()

        line_numbers = []
        memory_values = []
        for func, line, mem, _ in profiler.get_stats().timings[funck]:
            line_numbers.append(line)
            memory_values.append(mem)

        plt.plot(line_numbers, memory_values)
        plt.xlabel('Line Number')
        plt.ylabel('Memory Usage (bytes)')
        plt.title(f'Memory Usage for {funck.__name__}')
        plt.savefig(f'{funck.__name__}_memory_chart.png')
        plt.close()

        return result

    return wrapper


# Write a function to check the memory usage of the function
@measure_memory_usage
def my_func():
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a


if __name__ == '__main__':
    try:
        value = my_func()
    except Exception as err:
        print("Error Occurred")
        print(err)
