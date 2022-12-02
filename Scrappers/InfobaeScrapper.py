# InfobaeScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

from Scrappers.Scraps.ScrapsSQL import SQLArticlesScrapV2Row as Row

import bs4 as bs
import lxml
import logging
from datetime import datetime

class InfobaeScrapper(Scrapper):    
    def go_scrape(self, ret):
        # FIXME: 02/11/2022 : This kludge is here to allow each job to refer to different tables
        #        with different column format
        self.SQL_cols = self.scraps.scraps_SQL.SQL_articles_scrap_v2_cols
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

        # ######
        # Level 1: Left for later... maybe never...
        # ######

        # ######
        # Level 2: Left for later... maybe never...
        # ######
        
        from Scrappers.Scraps.ScrapsSQL import SQL_articles_scrap_v2_schema as SQL_schema
        import copy

        datamodel_dict = copy.copy(SQL_schema)              # shitty cruft done in order not to duplicate datamodel definition nor duplicating points of maintenance
        datamodel_dict = {f: None for f in datamodel_dict}  # Clean it...

        anchored_articles = {}      # Pivoting on <h2>s
        non_anchored_articles = {}  # 

        for i, h2 in enumerate(hs[2]):
            try:
                tuple(map(lambda tag: tag.name.lower(), h2.parents)).index('a')
            except ValueError:
                non_anchored_articles[h2] = h2
                print(f'Non-anchored <h2> found: [{i}]')
                continue
            anchored_articles[h2] = copy.copy(datamodel_dict)   # set a datamodel_dict apart 

        # 'anchored_articles' are those under the hierarchy of an <a> tag. Such 
        for i, h2 in enumerate(anchored_articles):
            # Routine data
            anchored_articles[h2]['UKEY'] = None
            anchored_articles[h2]['JOB'] = self.job_name
            anchored_articles[h2]['VOLANTA'] = "N/A -- INFOBAE HAS NO VOLANTAS!!!"
            anchored_articles[h2]['Origen'] = self.url
            anchored_articles[h2]['FechaFiltro'] = self.capture_datetime
            anchored_articles[h2]['FechaCreacion'] = self.capture_datetime
            anchored_articles[h2]['FechaModificacion'] = self.capture_datetime

            # ARTICLE : order of <h2> tag within <h2>s tags
            ARTICLE = hs[2].index(h2)
            anchored_articles[h2]['ARTICLE'] = ARTICLE

            # TITLE extraction
            TITLE = h2.get_text().strip()
            anchored_articles[h2]['TITLE'] = TITLE

            # AUTHOR extraction
            # AdHoc sanitization of AUTHOR fields
            anchor_cursor = h2
            while anchor_cursor.name.lower() != 'a':
                anchor_cursor = anchor_cursor.parent
            author_candidates_list = list(map(lambda tag: tag.get_text(), anchor_cursor.find_all(class_ = 'overlay_ctn')))
            author_candidate = author_candidates_list[0] if len(author_candidates_list) != 0 else None

            if author_candidate and isinstance(author_candidate, str):    # If at least there's an author_candidate and is a string (just in case)...
                if author_candidate.find(',') != -1: # Sometimes a clarification is made with a comma in the middle...
                    author_candidate = author_candidate[: author_candidate.find(',')]   # ... strip it
                if author_candidate.find('-') != -1: # Sometimes accompanying VIDEO/AUDIO is denoted separated by '-' 
                    author_candidate = author_candidate[: author_candidate.find('-')]
                author_candidate = author_candidate.strip()     # ... just to be sure...

                # Starting 'Por' denotes autorship...
                if author_candidate[0:4] == 'Por ':
                    author_candidate = author_candidate[3:].strip() # At this point, compromise into assuming it's an author

                if author_candidate.upper() == author_candidate:    # If it's all uppercase, almost certainly ain't an author
                    author_candidate = None
            else:
                author_candidate = None     # explicitly default to None if None or not-a-string, just for clarity

            AUTHOR = author_candidate
            anchored_articles[h2]['AUTHOR'] = AUTHOR

            # SUMMARY extraction
            summary_candidates_list = list(map(lambda tag: tag.get_text(), anchor_cursor.find_all(class_ = 'cst_deck')))
            summary_candidate = summary_candidates_list[0] if len(summary_candidates_list) != 0 else None

            SUMMARY = summary_candidate
            anchored_articles[h2]['SUMMARY'] = SUMMARY

            # SLUG extraction
            SLUG = h2.parent.get('href') # This is only going one parent upwards
            # I might wanna be looking for the nearest <a> tag upwards...
            # print(f'{i:3d}', tuple(map(lambda tag: tag.name, h2.parents))) # index of the nearest upwards <a>nchor tag
            anchored_articles[h2]['SLUG'] = SLUG

            # CATEGORY & SUBCATEGORY extraction
            if SLUG:    # Only if there's a SLUG present attempt to extract
                if SLUG[0] == '/':  # CATEGORY: Only if Relative address -- SLUG EXTERNAL == False
                    anchored_articles[h2]['SLUG_INTERNAL'] = 1
                    anchored_articles[h2]['CATEGORY'] = SLUG.split('/')[1]
                    if (SLUG.split('/')[2][0] in tuple(map(chr, range(ord('a'), ord('z') + 1))) + tuple(map(chr, range(ord('A'), ord('Z') + 1)))):
                        anchored_articles[h2]['SUBCATEGORY'] = SLUG.split('/')[2]
                elif SLUG[0:4].lower() in ('http://', 'https://'):
                    anchored_articles[h2]['SLUG_INTERNAL'] = 0
                    anchored_articles[h2]['CATEGORY'] = False
                    anchored_articles[h2]['SUBCATEGORY'] = False
                else:
                    anchored_articles[h2]['CATEGORY'] = None
                    anchored_articles[h2]['SUBCATEGORY'] = None
                    anchored_articles[h2]['SLUG_INTERNAL'] = -1
            else:   # if SLUG is None 'Category' should be None too
                anchored_articles[h2]['CATEGORY'] = None
                anchored_articles[h2]['SUBCATEGORY'] = None
                anchored_articles[h2]['SLUG_INTERNAL'] = -1

            anchored_articles[h2]['TITLE_WORD_COUNT'] = len(h2.get_text().strip().split(' '))

        # Stash it away
        for h2 in anchored_articles:
            UKEY = str(datetime.now()) + '-' + str(anchored_articles[h2]['ARTICLE'])
            # print("DBG::", UKEY)
            # print("DBG::", anchored_articles[h2]['JOB'])
            # print("DBG::", anchored_articles[h2]['TITLE'])
            # print("DBG::", anchored_articles[h2]['TITLE_WORD_COUNT'])
            # print("DBG::", anchored_articles[h2]['ARTICLE'])
            # print("DBG::", anchored_articles[h2]['CLUSTER'])
            # print("DBG::", anchored_articles[h2]['CLUSTER_INDEX'])
            # print("DBG::", anchored_articles[h2]['CLUSTER_SIZE'])
            # print("DBG::", anchored_articles[h2]['CLUSTER_UNIQUE'])
            # print("DBG::", anchored_articles[h2]['AUTHOR'])
            # print("DBG::", anchored_articles[h2]['SUMMARY'])
            # print("DBG::", anchored_articles[h2]['VOLANTA'])
            # print("DBG::", anchored_articles[h2]['CATEGORY'])
            # print("DBG::", anchored_articles[h2]['SUBCATEGORY'])
            # print("DBG::", anchored_articles[h2]['SLUG'])
            # print("DBG::", anchored_articles[h2]['SLUG_INTERNAL'])
            # print("DBG::", anchored_articles[h2]['Origen'])
            # print("DBG::", anchored_articles[h2]['FechaFiltro'])
            # print("DBG::", anchored_articles[h2]['FechaCreacion'])
            # print("DBG::", anchored_articles[h2]['FechaModificacion'])

            row = Row(UKEY,    # UKEY
                      anchored_articles[h2]['JOB'],
                      anchored_articles[h2]['TITLE'],
                      anchored_articles[h2]['TITLE_WORD_COUNT'],
                      anchored_articles[h2]['ARTICLE'],
                      anchored_articles[h2]['CLUSTER'],
                      anchored_articles[h2]['CLUSTER_INDEX'],
                      anchored_articles[h2]['CLUSTER_SIZE'],
                      anchored_articles[h2]['CLUSTER_UNIQUE'],
                      anchored_articles[h2]['AUTHOR'],
                      anchored_articles[h2]['SUMMARY'],
                      anchored_articles[h2]['VOLANTA'],
                      anchored_articles[h2]['CATEGORY'],
                      anchored_articles[h2]['SUBCATEGORY'],
                      anchored_articles[h2]['SLUG'],
                      anchored_articles[h2]['SLUG_INTERNAL'],
                      anchored_articles[h2]['Origen'],
                      anchored_articles[h2]['FechaFiltro'],
                      anchored_articles[h2]['FechaCreacion'],
                      anchored_articles[h2]['FechaModificacion']
                     )

            if self.scraps.SQL_stash_row_given_schema(row, SQL_schema, Row):
                pass
            else:
                logging.error(f"Error while stashing row:")
                logging.error(f"Row: {row}")