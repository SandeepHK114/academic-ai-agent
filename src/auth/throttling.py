import time
from fastapi import HTTPException, status

#Time Window
GLOBAL_TIME_LIMIT_SECONDS = 60

#For unauthenticated users
GLOBAL_RATE_LIMIT = 3

#Storage for time_stamps: user_requests = {userid1: [timestamp1,timestamp2], userid2: [timestamp1, timestamp2]}
user_requests = {}

def apply_rate_limit(user_id: str):
    curr = time.time()
    time_limit = GLOBAL_TIME_LIMIT_SECONDS
    rate_limit = GLOBAL_RATE_LIMIT

    if user_id not in user_requests:
        user_requests[user_id] = []

    #Filtering out timestamps that are outside current window
    user_requests[user_id] = [t for t in user_requests[user_id] if t > curr - time_limit]


    #If the number of requests exceeds the limit then send error
    if len(user_requests[user_id]) >= rate_limit:
        raise HTTPException(status_code = status.HTTP_429_TOO_MANY_REQUESTS,
                            detail = "Please try again later")

    user_requests[user_id].append(curr)
    return True


