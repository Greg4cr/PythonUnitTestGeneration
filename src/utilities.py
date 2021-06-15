import os
import json

def parseMetadata(filename):
    # Does the file exist?
    if not os.path.isfile(filename):
        raise FileNotFoundError('Metadata JSON not found.')

    with open(filename, 'r') as file:
        data = file.read()

    file.close()

    metadata = json.loads(data)

    return metadata
