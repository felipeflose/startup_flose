# src/flose/connectors/gemma_local.py

def process_data(data: dict) -> dict:
    """
    Process data from Gemma Local connector.

    Args:
        data (dict): Input data dictionary.

    Returns:
        dict: Processed data.
    """
    processed_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            processed_data[key] = value.upper()
        else:
            processed_data[key] = value
    return processed_data