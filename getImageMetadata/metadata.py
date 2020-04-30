import json

import exifread


def restructure(metadata: dict) -> dict:
    """Restructures a flat metadata dictionary into one composed of nested objects
    
    Uses the first word of each key to form the nested "group" objects
    """
    new_metadata = {}
    for (key, value) in metadata.items():
        # Custom logic for certain fields
        if key == "JPEGThumbnail":
            add_group(new_metadata, "Thumbnail")
            new_metadata["Thumbnail"].update({key: value})
            continue

        split_key = key.split()
        if len(split_key) == 1:
            # If key has no group, just append to top level
            new_metadata.update({key: value})
        elif len(split_key) > 1:
            # Create a new group then add the data to that group
            add_group(new_metadata, split_key[0])
            new_metadata[split_key[0]].update({" ".join(split_key[1:]): value})

    return new_metadata


def add_group(metadata: dict, group: str) -> dict:
    """Adds an empty object to a dictionary if one does not already exist"""
    if group not in metadata:
        metadata.update({group: {}})

    return metadata


def to_json(metadata):
    """Creates valid json out of a metadata dictionary"""

    def serialize(value):
        if isinstance(value, exifread.classes.IfdTag):
            return value.printable
        else:
            return str(value)

    return json.dumps(metadata, default=serialize, sort_keys=True)
