import json

import exifread


def restructure(metadata: dict) -> dict:
    """Restructures a flat metadata dictionary into one composed of objects by Image File Directory (IFD)
    
    Uses the first word of each key to form the IFD objects
    """
    new_metadata = {}
    for (key, value) in metadata.items():
        # Custom logic for certain fields
        if key == "JPEGThumbnail":
            add_IFD(new_metadata, "Thumbnail")
            new_metadata["Thumbnail"].update({key: value})
            continue

        split_key = key.split()
        if len(split_key) == 1:
            # If key has no IFD, just append to top level
            new_metadata.update({key: value})
        elif len(split_key) > 1:
            # Create a new IFD then add the data to that IFD
            add_IFD(new_metadata, split_key[0])
            new_metadata[split_key[0]].update({" ".join(split_key[1:]): value})

    return new_metadata


def add_IFD(metadata: dict, ifd: str) -> dict:
    """Adds an empty object to a dictionary if one does not already exist"""
    if ifd not in metadata:
        metadata.update({ifd: {}})

    return metadata


def remove_thumbnail(metadata: dict) -> dict:
    """Removes the JPEGThumbnail property if it exists"""
    if "JPEGThumbnail" in metadata:
        del metadata["JPEGThumbnail"]
    elif "Thumbnail" in metadata:
        if "JPEGThumbnail" in metadata["Thumbnail"]:
            del metadata["Thumbnail"]["JPEGThumbnail"]

    return metadata


def to_json(metadata: dict) -> str:
    """Creates a valid json string out of a metadata dictionary"""

    def serialize(value):
        """Custom serializer to handle exifread classes"""
        if isinstance(value, exifread.classes.IfdTag):
            return value.printable
        else:
            return str(value)

    return json.dumps(metadata, default=serialize, sort_keys=True)
