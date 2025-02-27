import datetime

def get_current_timestamp():
    """Returns the current timestamp"""
    return datetime.datetime.now().isoformat()  # Fix: Use "." instead of ","
