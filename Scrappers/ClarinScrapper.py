# ClarinScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

from Scrappers.Scraps.ScrapsSQL import SQLArticlesScrapV1Row as Row

import bs4 as bs
import lxml
import logging
from datetime import datetime

class ClarinScrapper(Scrapper):    
    def go_scrape(self, ret):
        # FIXME: 02/11/2022 : This kludge is here to allow each job to refer to different tables
        #        with different column format
        self.SQL_cols = self.scraps.scraps_SQL.SQL_articles_scrap_v1_cols
        # ##########################
        # First, tuck away raw data:
        # ##########################
        soup = bs.BeautifulSoup(ret.text, 'lxml')
        beg_size = len(str(soup))
       
        for discard_tag in ("script", "style"):     # decompose all instances of irrelevant tags
            for t in soup.find_all(discard_tag): t.decompose()

        # output some statistics regarding pruning
        pruned_text = str(soup)
        end_size = len(pruned_text)
        print(self.job_name + " | end_size :: ", end_size)
        logging.info(self.job_name + " | end_size :: " + str(end_size))
        print(self.job_name + " | beg_size :: ", beg_size)
        logging.info(self.job_name + " | beg_size :: " + str(beg_size))
        
        try:
            print(self.job_name + " | % saving :: ", (beg_size - end_size)/beg_size * 100)
            logging.info(self.job_name + " | % saving :: " + str((beg_size - end_size)/beg_size * 100))
        except ZeroDivisionError:
            print('ZeroDivisionError Exception -- Presume empty request or request failure')
            logging.error('ZeroDivisionError Exception -- Presume empty request or request failure')
        print('-' * 60)
        
        self.scraps.set_rawdata(ret, pruned_text)
        # #######
        # end_of: raw data saving ... soup's already pruned, so no need to reparse it.
        # #######

        # Measure size of <head> -- keep in mind that <script> and <style> tags have been stripped
        head_list = list(soup.find_all('head'))
        if head_list:
            if len(head_list) > 1:
                logging.info("In " + self.job_name + " <head> tag should be only one!")
            # use head_list[0] as <head>
            head = head_list[0]
            self.scraps.doc_level0()['head-size'] = len(str(head))
            
            # deal with <title>, considering <head>
            title_list = list(head.find_all('title'))
            if title_list:
                if len(title_list) > 1:
                    logging.info("In " + self.job_name + " <title> tag should be only one! MALFORMED HTML!!!")
                # use title_list[0] as <title>
                title = title_list[0]
                self.scraps.doc_level0()['title'] = str(title.get_text())
            else:
                logging.warning("In " + self.job_name + " <title> tag does not exist!")            
        else:
            logging.warning("In " + self.job_name + " <head> tag should exist!  MALFORMED HTML!!!")

        # Measure size of <body> -- keep in mind that <script> and <style> tags have been stripped
        body_list = list(soup.find_all('body'))
        if body_list:
            if len(body_list) > 1:
                logging.info("In " + self.job_name + " <body> tag should be only one! MALFORMED HTML!!!")
            # use body_list[0] as <body>
            self.scraps.doc_level0()['body-size'] = len(str(body_list[0]))
        else:
            logging.warning("In " + self.job_name + " <body> tag should exist! MALFORMED HTML!!!")
        
        # harvest <head>'s <meta> and <link> tags and how many of each
        # ... first <meta>s
        meta_list = list(head.find_all('meta'))
        self.scraps.doc_level0()['n-meta-tags'] = len(meta_list)
        self.scraps.doc_level0()['meta-tags'] = [str(meta) for meta in meta_list]  # str()'ify - meta ain't type() str
        # ... then <link>s
        link_list = list(head.find_all('link'))
        self.scraps.doc_level0()["n-link-tags"] = len(link_list)
        self.scraps.doc_level0()["link-tags"] = [str(link) for link in link_list]  # str()'ify
        # these can provide some intel on target's market, and function as an alert on modifications to the site

        # Count <h>s:
        hs = {i : list(soup.find_all('h' + str(i))) for i in range(1, 7)}
        for i in hs:
            self.scraps.doc_level0()["n-h" + str(i) + "-tags"] = len(hs[i])
        
        # Count <section>s, <article>s, <header>s, and <footer>s:
        for tag in ['section', 'article', 'header', 'footer']:
            self.scraps.doc_level0()["n-" + tag + '-tags'] = len(list(soup.find_all(tag)))

        # ########
        # Level 1: "The particulars of the scrapee"
        # ########
        # CLARIN: only <h2>s are relevant when it comes to information presented to the reader
        #   the criteria is that if an <h2> is contained within a <section>, such an <h2> is deemed relevant
        #   separate every <h2> according to the section that contains it
        h2s_by_section = [list(section.find_all('h2')) for section in [section for section in soup.find_all('section')]]
        # articles_by_h2 = [tag_nearest_name(h2, 'article') for h2 in soup.find_all('h2')]
        # 
        # # GENERAL: get the nearest upward tag containing tags with 'href' attribute
        # #   the criteria is that, in most cases, 
        # h2s_data = []    # TODO: this should be a list of namedtuples?
        # for i_section, section in enumerate(h2s_by_section):
        #     for h2 in section:
        #         href_tags = tag_nearest_attrs(h2, 'href')
        #         if not href_tags:   # anomalous condition --- this should never happen
        #             logging.warning('CLARIN: No href attribute was found for <h2>[' + hs[2].index(h2) + ']\'s hierarchy')
        #         # process href attribute
        #         h2s_data.append(
        #             {'h2'                   : h2,                                               # <h2> itself
        #              'containing_section'   : i_section,                                        # ... which section, by index, it belongs to
        #              'index'                : hs[2].index(h2),                                  # ... position among all <h2>s
        #              'text'                 : h2.get_text().strip(),                            # ... get text
        #              'has_href'             : True if href_tags else False,                     # ...  
        #              'many_hrefs'           : True if len(href_tags) > 1 else False             # ...
        #              'primary_href'         : href_tags[0].get('href')                          # ... it defaults to None if no href exists, so it's cool
        #              'hrefs_list'           : [href_tag.get('href') for href_tag in href_tags]  # ... none should be None, but the fuck would I know...
        #             }
        #         )
        ## LEVEL 1 IS IN STAND BY UNTIL NEW NOTICE!!!

        # ########
        # Level 2: "The generalities with, albeit simple, general semantic content"
        # ########
        # CLARIN:
        
        # First, use <h2> tags, to pivot to <article>s

# SQLArticlesScrapV1Row = namedtuple('SQLArticlesScrapV1Row',     # CREATE TABLE articles_scrap_v1 (
#                                    [ 'UKEY',                    # 	UKEY VARCHAR(100),
#                                      'JOB',                     # 	JOB VARCHAR(50),
#                                      'TITLE',                   # 	TITLE VARCHAR(200),
#                                      'TITLE_WORD_COUNT',        # 	TITLE_WORD_COUNT INT,
#                                      'AUTHOR',                  # 	AUTHOR VARCHAR(50),
#                                      'SUMMARY',                 # 	SUMMARY VARCHAR(500),
#                                      'VOLANTA',                 # 	VOLANTA VARCHAR(100),
#                                      'CATEGORY',                # 	CATEGORY VARCHAR(100),
#                                      'SLUG',                    # 	SLUG VARCHAR(300),
#                                      'Origen',                  # 	Origen VARCHAR(50),
#                                      'FechaFiltro',             # 	FechaFiltro DATE,           # Origin Date
#                                      'FechaCreacion',           # 	FechaCreacion DATE,         # Row insertion Date
#                                      'FechaModificacion',       # 	FechaModificacion DATE      # Row modification Date
#                                    ]                            # )
#                                   )
        article_descriptors = []
        for i, section in enumerate(h2s_by_section):
            for j, h2 in enumerate(section):
                h2_parents_names = [tag.name for tag in h2.parents]
                try:        # 01/11/2022 :: Skip over those <h2>s without a parent <article>
                    h2_article = list(h2.parents)[h2_parents_names.index('article')]
                except ValueError:
                    logging.info(f"<h2> with no <article> in parents")
                    logging.info(f"<h2> :: {h2}")
                    continue

                # article title
                TITLE = h2.get_text()
                
                TITLE_WORD_COUNT = len(TITLE.split(' '))
                
                # Try extract <article>'s author -- default to None if none is found
                article_author_tag = h2_article.find(class_ = 'author') or h2_article.find(class_ = 'author-rel')
                try:
                    AUTHOR = article_author_tag.get_text()
                except AttributeError:
                    AUTHOR = None       # TODO: Cuando AUTHOR == DIARIO OLE ... 
                
                # Try extract <article>'s summary -- default to None if none is found; most of the times isn't
                article_summary_tag = h2_article.find(class_ = 'summary') or h2_article.find(class_ = 'summary-rel')
                try:
                    SUMMARY = article_summary_tag.get_text()
                except AttributeError:
                    SUMMARY = None

                # Try extract <article>'s volanta -- default to None if none is found
                article_volanta_tag = h2_article.find(class_ = 'volanta') or h2_article.find(class_ = 'section-rel')
                try:
                    VOLANTA = article_volanta_tag.get_text()
                except AttributeError:
                    VOLANTA = None
                
                # Now it gets interesting -- category extraction is tricky
                article_hrefs_list = list(h2_article.find_all(href = True))
                if not article_hrefs_list:  # If no href is found, try a couple of nodes above. This happens in 'ULTIMO MOMENTO'
                    article_hrefs_list = list(h2_article.parent.parent.find_all(href = True))
                article_main_href = article_hrefs_list[0]['href'] if article_hrefs_list else None
                    # the fact that 'href' exist, should be ensured by the fact that article_href_list is nonempty
                    #   and the result of .find_all(href = True)
                
                # First try at a slug ...
                article_slug = article_main_href if article_main_href and article_main_href[0] == '/' else None
                CATEGORY = article_slug.split('/')[1] if article_slug else None
                if (article_main_href and 
                    article_main_href.split('/')[2] in ('www.clarin.com', 'www.ole.com.ar', 'elle.clarin.com' ) and 
                    not CATEGORY):
                   CATEGORY = article_main_href.split('/')[3]

                SLUG = article_slug

                Origen = self.url
                
                FechaFiltro = self.capture_datetime
                FechaCreacion = self.capture_datetime
                FechaModificacion = self.capture_datetime

                # Build row corresponding to <h2>'s <article>
                row = Row(str(datetime.now()) + '-' + str(i) + '-' + str(j), 
                          self.job_name, 
                          TITLE, 
                          TITLE_WORD_COUNT, 
                          AUTHOR, SUMMARY, 
                          VOLANTA, 
                          CATEGORY, 
                          SLUG, 
                          Origen, 
                          FechaFiltro, 
                          FechaCreacion, 
                          FechaModificacion)
                article_descriptors.append(row)

        # At this point, article_descriptors should have all the scrapped data
        # No UKEY, FechaFiltro, FechaCreacion, FechaModificacion are defined
        for descriptor in article_descriptors:
            if self.scraps.SQL_stash_row(descriptor):
                pass
            else:
                logging.error(f"Error while stashing row:")
                logging.error(f"Row: {descriptor}")
        


