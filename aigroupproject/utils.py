class RT:
    """Class used to measure runtime performance of functions."""

    function_runtimes: dict[str, float] = {}

    @classmethod
    def update_runtime(cls, function_name: str, start_time: float, end_time: float):
        # Update the runtime in the dictionary for the given function
        elapsed_time = end_time - start_time
        if function_name not in cls.function_runtimes:
            # print(cls.function_runtimes)
            cls.function_runtimes[function_name] = 0
        cls.function_runtimes[function_name] += elapsed_time
