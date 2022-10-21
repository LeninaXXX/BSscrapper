# BSutils.py
# Improvised utilities to deal with BeautifulSoup results, to make some sense of the tree

def tag_depth(node):
    """
    Returns depth of node in hierarchy
    """
    depth = 0
    while node:
        node = node.parent
        depth += 1
    return depth

def tag_nearest_attrs(tag, attr):
    """
    Given a tag, walks upwards the hierarchy and stops when reaching a tag
    with at least one tag in its descendants hierarchy having attr attribute
    defined, and returns a list of the nodes with that attribute defined
    """
    cursor = tag
    while cursor:
        attrs = [tag for tag in cursor.find_all(lambda f: f.get(attr)) if tag]  # 'if tag' just in case tag is None
        if attrs:                                                               # NOTE: shouldn't this actually guard against
            return attrs                                                        #   accessing something that ain't mapping?
        else:
            cursor = cursor.parent
    else:
        return None

def tag_nearest_attr_val(tag, attr, val):
    """
    Given a tag, walks upwards the hierarchy and stops when reaching a tag
    with at least one tag in its descendants hierarchy having attr attribute
    with value val, and returns a list of the nodes with that attribute equal
    to val.
    """
    cursor = tag
    while cursor:
        # lambda f: f.has_attr('class') and 'volanta' in f.get('class')
        attrs = [tag for tag in cursor.find_all(lambda f: f.has_attr(attr) and val in f.get(attr)) if tag] # 'if tag' just in case tag is None
        if attrs:                                                   # NOTE: shouldn't this actually guard against
            return attrs                                            #   accessing something that ain't mapping?
        else:
            cursor = cursor.parent
    else:
        return None

def tag_nearest_name(tag, name):
    """
    Given a tag, walks upwards the hierarchy and stops when reaching a tag
    whose name is 'name' and returns it. 
    If none with name name is found, it returns None
    """
    cursor = tag
    while cursor:
        if cursor.name == name:
            return cursor
        else:
            cursor = cursor.parent
    else:
        return None