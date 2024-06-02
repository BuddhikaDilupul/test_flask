from datetime import datetime

def convert_timestamp_to_datetime(timestamp):
    # Convert milliseconds to seconds
    timestamp_in_seconds = timestamp / 1000.0
    # Create datetime object from the timestamp
    dt_object = datetime.fromtimestamp(timestamp_in_seconds)
    # Format the datetime object to the desired format
    formatted_time = dt_object.strftime('%d/%m/%Y %H:%M:%S')
    return formatted_time