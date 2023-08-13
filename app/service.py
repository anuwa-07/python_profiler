
import os
import time
import logging
import cProfile
import pstats
import webbrowser
import socket
import subprocess
import line_profiler
#
from typing import Callable


class BluezyProfiler:
    def __init__(
            self,
            file_path: str,
            log_details: bool = False,
            log_record_count: int = 10,
            enable_snakeviz_server: bool = True,
            port: int = 8087,
            sort_by: str = 'time'
    ) -> None:
        self.__file_path = self.__validate_file_path(file_path)
        self.__log_details = log_details
        self.__log_record_count = log_record_count
        self.__port = port
        self.__host = f'http://127.0.0.1:{self.__port}/snakeviz/'
        self.__server_process = None
        self.__sort_by = sort_by
        self.__enable_snakeviz_server = enable_snakeviz_server

        # check the file path exists. if not create the directory.
        if not os.path.exists(self.__file_path):
            logging.error(f":: [ Creating.... ] File path: {self.__file_path} ::")
            os.makedirs(self.__file_path)

        # If the snakeviz server is not running, start the snakeviz server.
        if self.__enable_snakeviz_server:
            if not self.__check_server_running('127.0.0.1', self.__port) and not self.__server_process:
                self.__server_process = subprocess.Popen(
                    ['snakeviz', '--port', str(self.__port), './data/sample_profiling.prof']
                )
            #
            if self.__server_process:
                logging.info(f":: [Snakeviz Server] is Started On http://127.0.0.1:{self.__port}/... ::")

    def __str__(self) -> str:
        return f"BluezyProfiler(file_path={self.__file_path}, log_details={self.__log_details}, " \
               f"log_record_count={self.__log_record_count}, port={self.__port})"

    def cprofile_decorator(self) -> Callable:
        """
            This is the decorator function to profile the function.
            This will create the profile file in the given file path and open the browser tab with the profile details.
            :return: Callable
        """
        def decorator(func: Callable) -> Callable:
            __new_file_path: str = f"{self.__file_path}/{func.__name__}_profiling.prof"

            def wrapper(*args, **kwargs):
                with cProfile.Profile() as profile:
                    func(*args, **kwargs)

                profile.dump_stats(__new_file_path)
                results = pstats.Stats(__new_file_path)
                #
                # Use to print the log details.
                if self.__log_details and self.__log_record_count > 0:
                    if self.__sort_by == 'cumulative':
                        # This will print the cumulative time taken by each function.
                        results.strip_dirs().sort_stats(pstats.SortKey.CUMULATIVE).print_stats(self.__log_record_count)
                    elif self.__sort_by == 'calls':
                        # This will print the number of calls made by each function.
                        results.strip_dirs().sort_stats(pstats.SortKey.CALLS).print_stats(self.__log_record_count)
                    elif self.__sort_by == 'name':
                        # This will print the function name.
                        results.strip_dirs().sort_stats(pstats.SortKey.NAME).print_stats(self.__log_record_count)
                    else:
                        # This will print the time taken by each function.
                        results.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(self.__log_record_count)
                #
                if self.__enable_snakeviz_server:
                    print(f"{self.__host}{__new_file_path}")
                    webbrowser.open_new_tab(f"{self.__host}{__new_file_path}")
            #
            return wrapper
        return decorator

    def line_profiler_decorator_v3(self) -> Callable:
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
                profile_file = os.path.abspath(f"{self.__file_path}/{func.__name__}_line_profiling.lprof")
                line_profiler_instance.dump_stats(profile_file)

                # Print profiling information to the console
                print(f"Line-by-Line Profiling for function: {func.__name__}")
                line_profiler_instance.print_stats()

                if self.__enable_snakeviz_server:
                    # Print the file path
                    profile_file_v1 = os.path.abspath(f"{self.__file_path}/hello.prof")
                    print(profile_file_v1)
                    webbrowser.open_new_tab(f"{self.__host}{profile_file_v1}")
                #
                return result
            return wrapper
        return decorator

    def stop_snakeviz_server(self) -> None:
        """
            This will kill the upped snakeviz server.
            :return: None
        """
        if self.__server_process:
            self.__server_process.kill()
            logging.info(":: [Snakeviz Server] is Stopped ::")

    @staticmethod
    def __check_server_running(server_host, server_port) -> bool:
        """
        This will check the server is running on given host and port.
        If the server is running, it will return True, else it will return False.
        :param server_host: str
        :param server_port: int
        :return: bool
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)  # Timeout in case the port is not open
            s.connect((server_host, server_port))
            s.close()
            return True
        except Exception as err:
            return False

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


profiler_x = BluezyProfiler(
        file_path='/Users/anuruddha/Desktop/profiler',
        log_details=True,
        log_record_count=100,
        port=8087,
        sort_by='time',
        enable_snakeviz_server=True
)
if __name__ == "__main__":
    # @profiler_x.line_profiler_decorator_v3()
    @profiler_x.line_profiler_decorator_v3()
    def say_myname(name: str) -> None:
        # Loop till 100
        names: list = []
        big_list = []
        for i in range(1000):
            names.append("Hello World!!1")
        #
        for i in range(1000):
            big_list.append(names)
        #
        time.sleep(0.02)
        print(f"You are {name}")
        print("You are god damn right!!")
    #
    say_myname("Heisenberg")
    time.sleep(10)
    profiler_x.stop_snakeviz_server()
