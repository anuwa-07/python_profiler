
import os
import io
import logging
import subprocess
import line_profiler
#
from memory_profiler import profile as mem_profile
from typing import Callable


class CodeProfiler:
    def __init__(
            self,
            file_path: str,
            log_details: bool = False,
            log_record_count: int = 10
    ) -> None:
        self.__file_path = self.__validate_file_path(file_path)
        self.__file_path_lprof = f"{self.__file_path}/prof"
        self.__file_path_time = f"{self.__file_path}/time-based"
        self.__file_path_mem = f"{self.__file_path}/mem-based"
        self.__log_details = log_details
        self.__log_record_count = log_record_count

        # check the file path exists. if not create the directory.
        if not os.path.exists(self.__file_path):
            logging.error(f":: [ Creating.... ] File path: {self.__file_path} ::")
            os.makedirs(self.__file_path)
        #
        if not os.path.exists(f"{self.__file_path}/profile-lprof"):
            logging.error(f":: [ Creating.... ] File path: {self.__file_path}/profile-lprof ::")
            os.makedirs(f"{self.__file_path}/profile-lprof")
        #
        if not os.path.exists(f"{self.__file_path}/profile-text"):
            logging.error(f":: [ Creating.... ] File path: {self.__file_path}/profile-text ::")
            os.makedirs(f"{self.__file_path}/profile-text")

    def __str__(self) -> str:
        return f"CodeProfiler(file_path={self.__file_path}, log_details={self.__log_details}, " \
               f"log_record_count={self.__log_record_count}"

    def line_profiler_time(self) -> Callable:
        """
        This is the decorator function to perform line-by-line profiling of the function.
        This will create the profile file in the given file path and open the browser tab with the profile details.
        :return: Callable
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                # Create a line profiler for the current function
                line_profiler_instance = line_profiler.LineProfiler()

                # Wrap the function with the line profiler
                wrapped_func = line_profiler_instance(func)

                # Call the wrapped function
                result = wrapped_func(*args, **kwargs)

                # Dump the line-by-line profiling data to a file
                profile_file = os.path.abspath(f"{self.__file_path_lprof}/{func.__name__}_line_profiling.lprof")
                line_profiler_instance.dump_stats(profile_file)
                #
                # Log the profile details, if it allowed.
                if self.__log_details:
                    print("::::      PROFILE TIME SPEND DETAILS      :::::")
                    line_profiler_instance.print_stats()
                #
                txt_output_filename = f"{self.__file_path_time}/{func.__name__}_line_profiling.txt"
                with open(txt_output_filename, "w") as txt_file:
                    subprocess.run(["python", "-m", "line_profiler", profile_file], stdout=txt_file)
                #
                return result
            return wrapper
        return decorator

    def line_profiler_memory(self) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                file_name = os.path.abspath(f"{self.__file_path_mem}/{func.__name__}_memory_profile.txt")
                buffer = io.StringIO()

                # Use the memory profiler @profile decorator to profile memory
                decorated_func = mem_profile(stream=buffer)(func)

                # Call the decorated function
                result = decorated_func(*args, **kwargs)

                # Write to File.
                profile_data = buffer.getvalue()
                with open(file_name, 'w') as f:
                    f.write(profile_data)
                #
                # Log the profile details, if it allowed.
                if self.__log_details:
                    print("::::      PROFILE MEMORY USAGE DETAILS      :::::")
                    print(profile_data)
                #
                return result
            return wrapper
        return decorator

    @staticmethod
    def __validate_file_path(dir_path: str) -> str or None:
        """
            This will validate the directory path before passing the class variable.
            :param dir_path: str
            :return: None
        """
        if not isinstance(dir_path, str) or not dir_path.strip():
            raise ValueError(":: [ERROR] Directory path must be a non-empty string. ::")
        #
        normalized_path = os.path.normpath(dir_path)

        if not normalized_path.startswith('/'):
            normalized_path = '/' + normalized_path

        if normalized_path.endswith('/'):
            normalized_path = normalized_path[:-1]
        #
        return normalized_path
