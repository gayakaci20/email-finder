def normalize_accented_chars(text):
    """
    Replace accented characters with their non-accented equivalents.
    Specifically handles é, è, ç, à, ô, î and converts them to e, e, c, a, o, i.
    """
    if not text:
        return text
        
    # Define character mappings
    char_map = {
        'é': 'e',
        'è': 'e',
        'ê': 'e',
        'ë': 'e',
        'ç': 'c',
        'à': 'a',
        'â': 'a',
        'ä': 'a',
        'ô': 'o',
        'ö': 'o',
        'î': 'i',
        'ï': 'i',
        'ù': 'u',
        'û': 'u',
        'ü': 'u'
    }
    
    # Replace each accented character
    normalized_text = ''
    for char in text:
        normalized_text += char_map.get(char, char)
    
    return normalized_text