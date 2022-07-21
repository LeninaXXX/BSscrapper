# BSutils.py
# Improvised utilities to deal with BeautifulSoup results, to make some sense of the tree

def BSdepth(node):
    depth = 0
    while node:
        node = node.parent
        depth += 1
    return depth