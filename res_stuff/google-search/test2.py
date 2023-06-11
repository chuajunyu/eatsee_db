import pandas as pd
import numpy as np
import math
from math import sqrt
from geopy.distance import geodesic
import csv
import ast
from googlesearch import search
import time
import threading

query = 'Seafood Zi Char'
# query = query.replace(" ", "")
print(query)

# Function to be executed
def my_function():
    print(next(search(query, num_results=2)))

# Set the timeout duration in seconds
timeout_duration = 3

# Create an Event object to track the timeout
timeout_event = threading.Event()

# Function to handle the timeout
def timeout_handler():
    timeout_event.set()

def start_threading():
    # Create a thread for the function execution
    thread = threading.Thread(target=my_function)

    # Start the thread
    thread.start()

    # Set the timeout handler function to run after the specified duration
    timer = threading.Timer(timeout_duration, timeout_handler)
    timer.start()

    # Wait for the thread to complete or the timeout event to be set
    thread.join(timeout_duration)

    # Check if the thread is still alive
    if thread.is_alive():
        # Timeout occurred, handle it as desired
        print("Function execution timed out.")
        # Terminate the thread if necessary
        thread.join()

    # Cancel the timer
    timer.cancel()

for i in range(3):
    start_threading()