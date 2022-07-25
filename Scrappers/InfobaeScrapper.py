# InfobaeScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml
import re

class InfobaeScrapper(Scrapper):    
    def go_scrape(self, ret):
        # First, tuck away raw data:
        soup = bs.BeautifulSoup(ret.text, 'lxml')
        beg_size = len(str(soup))
       
        for discard_tag in ("script", "style"):
            for t in soup.find_all(discard_tag): t.extract()

        pruned_text = str(soup)
        end_size = len(pruned_text)

        print(self.name + " | beg_size :: ", beg_size)
        print(self.name + " | end_size :: ", end_size)
        print(self.name + " | % saving :: ", (beg_size - end_size)/beg_size * 100)
        self.scraps.set_rawdata(ret, pruned_text)




#        # tuck away rawdata
#        self.scraps.set_rawdata(ret)
#
#        soup = bs.BeautifulSoup(ret.text, 'lxml')
#        
#        # MAIN ARTICLE
#        # Pivot tag for main article
#        articles_tags = list(soup.find_all('h2', class_ = 'cst_hl'))    # + list(soup.find_all('h2', class_ = 'opi_hl'))
#                                                                        # FIXME!: opi_hl -- Opinion articles
#                                                                        # These have a different wrapping and href resides
#                                                                        # presumably higher in the tree
#        headline_tag, articles_tags = articles_tags[:1], articles_tags[1:]
#        headline_tag = headline_tag[0]
#
#                                        # Puede haber mas de un headline
#        # headline_tag = soup.find('h2')  # Puede haber mas de un headline
#                                        # XXX: Ya mostro la fragilidad... no siempre la clase es la misma
#                                        # Durante una noche fue "dkt_fs_40" ...
#                                        #                   ... paso a ser "dkts_fs_36"
#                                        # Es mas seguro confiar en que es el primer <h2>
#        # headline_tag = headlines_tags[0]    # me quedo con uno porque me tengo que quedar con alguno...
#        
#        # Extract headline article title
#        headline_title = str(headline_tag.string)
#
#        # Use headline tag to pivot upwards in the tree
#        headline_parent = headline_tag.parent
#        headline_slug = headline_parent.attrs['href']
#        headline_category = headline_slug.split('/')[1]
#        # XXX: CAREFUL, BRITTLE: This assumes a lead in the first <div> tag
#        headline_lead = headline_parent.find('div', class_ = re.compile("_deck")).string
#        
#        self.scraps.add_main_article(MainArticle(headline_title,
#                                                 headline_slug,
#                                                 headline_category,
#                                                 headline_lead))
#        # ARTICLES
#        #                                   general.................................................opinion
#        # articles_tags = list(soup.find_all('h2', class_ = 'cst_hl')) + list(soup.find_all('h2', class_ = 'opi_hl'))
#        # articles_tags = articles_tags[1:]   # Trim the first, otherwise it's gonna be included twice
#        # print('len(article_tags) ==', len(articles_tags))
#        for i, a in enumerate(articles_tags):
#            a_title = a.string
#            a_parent = a.parent
#            try:
#                a_slug = a_parent.attrs['href']
#            except:
#                print('-' * 20, i, '-' * 20)
#                print(a_parent.prettify())
#            a_category = a_slug.split('/')[1]
#            self.scraps.add_article(Article(a_title, a_slug, a_category, None))
#