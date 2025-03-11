'''
a text hash function, which can be used to hash a text to a unique fixed length hash value.
'''
def hash_text(text: str) -> str:
    '''
    Hash a text to a unique fixed length hash value.

    Args:
        text: The text to be hashed.

    Returns:
        str: The hashed value.
    '''
    return hashlib.md5(text.encode()).hexdigest()