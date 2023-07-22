from multiprocessing import Manager


# The default message broker
manager = Manager()
store = manager.dict()

def start_store():
    """
    Start the store
    """
    global store
    store["last_message"] = 0

def new_traffic_notification():
    """
    Trigger a message to any listening web sockets
    """
    global store
    store["last_message"] += 1
