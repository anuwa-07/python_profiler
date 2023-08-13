
import time
from code_profiler import CodeProfiler

if __name__ == "__main__":
    test_profiler = CodeProfiler(
        file_path='/Users/anuruddha/Desktop/profiler',
        log_details=True,
        log_record_count=100
    )

    @test_profiler.line_profiler_decorator()
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
    #
    say_myname("Heisenberg")