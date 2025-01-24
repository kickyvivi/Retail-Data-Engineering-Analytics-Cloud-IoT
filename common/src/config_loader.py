import json

# Load configuration
def load_config(config_path):
    """
    Load the configuration file.
    
    Args:
        config_path (str): Path to the configuration file.
        
    Returns:
        dict: Configuration data.
    """
    with open(config_path, 'r') as config_file:
        return json.load(config_file)