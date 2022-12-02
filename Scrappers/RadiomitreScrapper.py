# RadiomitreScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

from Scrappers.Scraps.ScrapsSQL import SQLArticlesScrapV2Row as Row

import bs4 as bs
import lxml
import logging
from datetime import datetime

class RadiomitreScrapper(Scrapper):    
    def go_scrape(self, ret):
        # FIXME: 02/11/2022 : This kludge is here to allow each job to refer to different tables
        #        with different column format
        self.SQL_cols = self.scraps.scraps_SQL.SQL_articles_scrap_v2_cols
        # ##########################
        # First, tuck away raw data:
        # ##########################
        soup = bs.BeautifulSoup(ret.text, 'lxml')
        beg_size = len(str(soup))
       
        for discard_tag in ("script", "style"):
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

        # #######
        # Level 1: Left for later... maybe never...
        # #######

        # ######
        # Level 2
        # ######
        
        from Scrappers.Scraps.ScrapsSQL import SQL_articles_scrap_v2_schema as SQL_schema

        tags_tuple = ('article', 'section', 'header', 'footer', 'aside') + tuple(('h' + str(i) for i in range(1, 7)))
        tags = {tag_str : list(soup.find_all(tag_str)) for tag_str in tags_tuple}

        print("Harvesting information -- Scrapping!")
        logging.info("Harvesting information -- Scrapping!")
        article_reports = {}
        for i, article in enumerate(soup.find_all('article')):
            article_report = {}
            article_report['UKEY'] = None
            article_report['JOB'] = self.job_name

            article_report['ARTICLE'] = i
            
            titles_list = list(article.find_all('h2', class_ = 'title'))
            if not titles_list:
                continue
            else:
                title_tag = titles_list[0]
            title = title_tag.get_text().strip()
            
            if not title:
                continue

            article_report['TITLE'] = title if title else None
            article_report['TITLE_WORD_COUNT'] = len(tuple(article_report['TITLE'].split(' '))) if title else None

            article_report['CLUSTER'] = None
            article_report['CLUSTER_INDEX'] = None
            article_report['CLUSTER_SIZE'] = None
            article_report['CLUSTER_UNIQUE'] = None # Irrelevant

            article_report['AUTHOR'] = 'RADIO_MITRE ARTICLES ARE NOT AUTHORED!'
            article_report['SUMMARY'] = summary[0].get_text() if (summary := list(article.find_all('p', class_ = 'subtitle'))) else None
            article_report['VOLANTA'] = 'RADIO_MITRE ARTICLES HAS NO VOLANTAS!'

            hrefs_set = set(href_tag.get('href') for href_tag in article.find_all(href = True))

            if hrefs_set:
                internal_hrefs_set = {href for href in hrefs_set 
                                           if href.find('https://radiomitre.cienradios.com/') == 0 or
                                              href.find('http://radiomitre.cienradios.com/') == 0 or
                                              href.find('/') == 0}
                external_hrefs_set = hrefs_set - internal_hrefs_set
                
                if internal_hrefs_set:
                    article_report['SLUG'] = (slug := list(internal_hrefs_set)[0])
                    article_report['SLUG_INTERNAL'] = True
                else: # if not internal_hrefs_set and hrefs_set then external_hrefs_set 
                    article_report['SLUG'] = (slug := list(external_hrefs_set)[0])
                    article_report['SLUG_INTERNAL'] = False
                
                try:
                    category_list = slug.split('/')
                except:
                    logging.info(str(internal_hrefs_set))
                    print('internal_hrefs_set', internal_hrefs_set)
                    logging.info(str(external_hrefs_set))
                    print('external_hrefs_set', external_hrefs_set)
                    raise
                
                if category_list.index('') == 0:    # assume relative url
                    pass
                elif category_list.index('') == 1:  # assume absolute url
                    category_list = category_list[1:]
                else:
                    category_list = []
                
                while '' in category_list:
                    category_list.remove('')
                
                if category_list:
                    category_list = category_list[1:]
                    if len(category_list) >= 2:
                        article_report['CATEGORY'] = category_list[0]
                        article_report['SUBCATEGORY'] = category_list[1] if len(category_list) >= 3 else None
                    else:
                        article_report['CATEGORY'] = None
                        article_report['SUBCATEGORY'] = None
            else:
                article_report['SLUG'] = None
                article_report['SLUG_INTERNAL'] = None
                article_report['CATEGORY'] = None
                article_report['SUBCATEGORY'] = None

            article_report['Origen'] = self.url
            article_report['FechaFiltro'] = self.capture_datetime
            article_report['FechaCreacion'] = self.capture_datetime
            article_report['FechaModificacion'] = self.capture_datetime

            article_reports[i] = article_report
        
        # Stash it away
        for article in article_reports:
            UKEY = str(datetime.now()) + '-' + str(article_reports[article]['ARTICLE'])
            row = Row(UKEY,    # UKEY
                      article_reports[article]['JOB'],
                      article_reports[article]['TITLE'],
                      article_reports[article]['TITLE_WORD_COUNT'],
                      article_reports[article]['ARTICLE'],
                      article_reports[article]['CLUSTER'],
                      article_reports[article]['CLUSTER_INDEX'],
                      article_reports[article]['CLUSTER_SIZE'],
                      article_reports[article]['CLUSTER_UNIQUE'],
                      article_reports[article]['AUTHOR'],
                      article_reports[article]['SUMMARY'],
                      article_reports[article]['VOLANTA'],
                      article_reports[article]['CATEGORY'],
                      article_reports[article]['SUBCATEGORY'],
                      article_reports[article]['SLUG'],
                      article_reports[article]['SLUG_INTERNAL'],
                      article_reports[article]['Origen'],
                      article_reports[article]['FechaFiltro'],
                      article_reports[article]['FechaCreacion'],
                      article_reports[article]['FechaModificacion'],
                     )

            if self.scraps.SQL_stash_row_given_schema(row, SQL_schema, Row):
                pass
            else:
                logging.error(f"Error while stashing row:")
                logging.error(f"Row: {row}")