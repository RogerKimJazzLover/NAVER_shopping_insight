import custom_exceptions
import sys, time

def DisplayTimer(t: int):
    '''
    Prints out the timer into the terminal
    '''
    print("\nTimer Starting:")
    for i in range(t,0,-1):
        sys.stdout.write(str(i)+' ')
        sys.stdout.flush()
        time.sleep(1)

def ReAttemptUntilFailure(max_attempt: int, time: int):
    '''
    An decorator function
    Waits for 30 seconds when the function fails.
    '''
    def ReAttemptUntilFailureFunction(func):
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts != max_attempt:
                if attempts == max_attempt:
                    raise custom_exceptions.ReAttemptFail(max_attempt)
                try:
                    data = func(*args, **kwargs)
                except custom_exceptions.ResponseError as e:
                    if e.status_code == 413:
                        raise custom_exceptions.ReAttemptFail(max_attempt) #IF THE ERROR CODE IS 413, it means a special case where the request in invalid. So for now, just skip it.
                    print(f"{e.messaage}\nRetrying: {attempts} attempts / {max_attempt} max attempts")
                    DisplayTimer(time)
                    attempts += 1
                    continue
                except Exception as e:
                    print(f"{e}\nRetrying: {attempts} attempts / {max_attempt} max attempts")
                    DisplayTimer(time)
                    attempts += 1
                    continue
                break
            return data
        return wrapper
    return ReAttemptUntilFailureFunction