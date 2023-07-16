import os
import time
import logging
import cProfile
import pstats
import webbrowser
#
from typing import Callable


def cprofile_decorator(file_path: str, log_details: bool = False, log_record_count: int = 10) -> Callable:
    if not os.path.exists(file_path):
        logging.error(f":: [ Creating.... ] File path: {file_path} ::")
        os.makedirs(file_path)  # Create the directory if not exists.

    def decorator(func: Callable) -> Callable:
        _file_path: str = f"{file_path}/{func.__name__}_profiling.prof"

        def wrapper(*args, **kwargs):
            with cProfile.Profile() as profile:
                func(*args, **kwargs)

            profile.dump_stats(_file_path)
            results = pstats.Stats(_file_path)
            # Use to print the log details.
            if log_details and log_record_count > 0:
                results.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(log_record_count)
            #
            webbrowser.open_new_tab(f"http://localhost:8080/snakeviz/{_file_path}")
        #
        return wrapper
    return decorator


@cprofile_decorator(file_path='/Users/anuruddha/Desktop/profilerv2', log_details=True, log_record_count=10)
def say_myname(name: str) -> None:
    time.sleep(2)
    print(f"Hello my Name is: {name}")


#
if __name__ == "__main__":
    say_myname("John Doe")
