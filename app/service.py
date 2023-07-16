
import os
import time
import logging
import cProfile
import pstats
import webbrowser
import subprocess
import snakeviz.cli

from typing import Callable


class BluezyProfiler:
    def __init__(
            self,
            file_path: str,
            log_details: bool = False,
            log_record_count: int = 10,
            port: int = 8087
    ) -> None:
        # TODO: Add some proper validations for file_path, log_details, log_record_count, port
        self.__file_path = file_path
        self.__log_details = log_details
        self.__log_record_count = log_record_count
        self.__port = port
        self.__host = f'http://127.0.0.1:{self.__port}/snakeviz/'
        self.__server_process = None

        # check the file path exists. if not create the directory.
        if not os.path.exists(self.__file_path):
            logging.error(f":: [ Creating.... ] File path: {self.__file_path} ::")
            os.makedirs(self.__file_path)

        # TODO: Currently not in use.
        # snakeviz.cli.main(['--port', str(self.__port), './data/sample_profiling.prof'])

        # start the snakeviz server in background.
        self.__server_process = subprocess.Popen(
            ['snakeviz', '--port', str(self.__port), './data/sample_profiling.prof']
        )
        if self.__server_process:
            logging.info(f":: [Snakeviz Server] is Started On http://127.0.0.1:{self.__port}/... ::")

    def cprofile_decorator(self) -> Callable:
        """
            This is the decorator function to profile the function.
            This will create the profile file in the given file path and open the browser tab with the profile details.
            :return: Callable
        """
        # TODO: Remove the duplicate code.
        if not os.path.exists(self.__file_path):
            logging.error(f":: [ Creating.... ] File path: {self.__file_path} ::")
            os.makedirs(self.__file_path)  # Create the directory if not exists.

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
                    results.strip_dirs().sort_stats(pstats.SortKey.TIME).print_stats(self.__log_record_count)
                #
                webbrowser.open_new_tab(f"{self.__host}{__new_file_path}")
            #
            return wrapper
        return decorator

    def stop_snakeviz_server(self) -> None:
        """
            This will stop the snakeviz server.
            :return: None
        """
        if self.__server_process:
            self.__server_process.kill()
            logging.info(":: [Snakeviz Server] is Stopped ::")


profiler_x = BluezyProfiler(
        file_path='/Users/anuruddha/Desktop/profiler',
        log_details=True,
        log_record_count=10,
        port=8087
)
if __name__ == "__main__":
    @profiler_x.cprofile_decorator()
    def say_myname(name: str) -> None:
        time.sleep(2)
        print(f"You are {name}")
        print("You are god damn right!!")
    #
    say_myname("Heisenberg")
    time.sleep(3)
    profiler_x.stop_snakeviz_server()

"""
 This if tgof the Testing opepto thisd will gi e you the 
 Sod thytk ghar in This tis the best waytto the thk


"""

