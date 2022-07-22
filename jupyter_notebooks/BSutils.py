# BSutils.py
# Improvised utilities to deal with BeautifulSoup results, to make some sense of the tree
import bs4 as bs

class TagPair():
    def __init__(self, ltag, rtag):
        self.ltag = ltag
        self.rtag = rtag
    
    def luca_by_ltag(self):         # last common ancestor, climbing left tag
        ltag_asc = self.ltag        # ltag ascendancy
        while not self.rtag in ltag_asc.descendants:
            ltag_asc = ltag_asc.parent
        return ltag_asc            

    def luca_by_rtag(self):         # last common ancestor, climbing right tag
        rtag_asc = self.rtag
        while not self.ltag in rtag_asc.descendants:
            rtag_asc = rtag_asc.parent
        return rtag_asc

    def is_luca_sane(self):
        return self.luca_by_ltag() == self.luca_by_rtag()

class TagHierarchy():
    def __init__(self, node):
        self.taglist = []
        while node: # Go upwards until hitting None brickwall
            self.taglist.append({'node' : node, 'attrs' : node.attrs})
            node = node.parent
#     def attrs_hierarchy(self):
#         for tag in self.taglist:
