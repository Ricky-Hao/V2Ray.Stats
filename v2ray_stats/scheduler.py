import functools
import threading

import schedule


def catch_exceptions(job_func, cancel_on_failure=False):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            traceback.print_exc()
            if cancel_on_failure:
                return schedule.CancelJob

    return wrapper


def run_threaded(job_func, *args, **kwargs):
    job_func = functools.partial(job_func, *args, **kwargs)
    job_thread = threading.Thread(target=job_func)
    job_thread.start()
