# LanacionScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

from Scrappers.Scraps.ScrapsSQL import SQLArticlesScrapV2Row as Row

import bs4 as bs
import lxml
import logging
from datetime import datetime

class LanacionScrapper(Scrapper):    
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
        tags = {tag_str : soup.find_all(tag_str) for tag_str in tags_tuple}

        # clusters_by_article = {}
        # clusters_list = []
        print("Extracting La Nacion's 'data-pos' attributes")
        data_pos_by_article = {}
        for i, article in enumerate(tags['article']):
            # Compute data-pos for each <article>
            if data_pos := article.attrs.get('data-pos'):
                data_pos_by_article[article] = (data_pos[:-2], data_pos[-2:])
            else:
                continue
            
            # TODO: structural clusterization
            # # Tuck away cluster associated with each <article>, accessible by <article>
            # clusters_by_article[article] = article.parent
            # while len(clusters_by_article[article].find_all('article')) == 1:
            #     clusters_by_article[article] = clusters_by_article[article].parent  # save cluster, accessible by article
            # # Tuck away clusters as they appear
            # if clusters_by_article[article] not in clusters_list:
            #     clusters_list.append(clusters_by_article[article])  # save clusters, as they appear in order
        # renumerate CLUSTER and CLUSTER_POSITION_IN so as to fit a tidy integer
      
        print("Computing clusterization based on 'data-pos' attribute")
        logging.info("Computing clusterization based on 'data-pos' attribute")
        clusters = []               # tuck away the label of each cluster as it appears in the page
        clusters_by_article = {}    # ... it's index in the list will allow to univocally enumerate them
        for article in data_pos_by_article: # The dictionary allow for the calculation of size and position within the cluster
            if data_pos_by_article[article][0] not in clusters:
                    clusters.append(data_pos_by_article[article][0])
            clusters_by_article[article] = tuple(art for art in data_pos_by_article 
                                                  if data_pos_by_article[art][0] == data_pos_by_article[article][0])
        
        print("Harvesting information -- Scrapping!")
        logging.info("Harvesting information -- Scrapping!")
        article_reports = {}
        for i, article in enumerate(tags['article']):
            article_report = {}
            article_report['UKEY'] = None
            article_report['JOB'] = self.job_name

            article_report['ARTICLE'] = i

            # TODO: com-title returns None value -- shouldn't
            article_report['TITLE'] = a.get_text() if (a := article.find(class_ = ('title'))) != None else None
           
            article_report['TITLE_WORD_COUNT'] = len(a.split(' ')) if (a := article_report['TITLE']) != None else None

            article_report['LANACION_data_pos'] = article.attrs.get('data-pos')
            article_report['LANACION_data_pos_cluster'] = data_pos_by_article.get(article)[0]
            article_report['LANACION_data_pos_cluster_member'] = data_pos_by_article.get(article)[1]
            article_report['LANACION_hrefs_list'] = list(hrefs_set := set(href_tag.get('href') for href_tag in article.find_all(href = True)))

            try:
                article_report['CLUSTER'] = clusters.index(data_pos_by_article[article][0])
            except ValueError:
                article_report['CLUSTER'] = None

            try:
                article_report['CLUSTER_INDEX'] = clusters_by_article[article].index(article)
                article_report['CLUSTER_SIZE'] = len(clusters_by_article[article])
            except ValueError:
                article_report['CLUSTER_INDEX'] = None
                article_report['CLUSTER_SIZE'] = None

            article_report['CLUSTER_UNIQUE'] = None # Irrelevant

            author_text = author_tags[0].get_text() if (author_tags := list(article.find_all('strong'))) else None
            article_report['AUTHOR'] = (author_text[3:].strip() if author_text.find('Por ') == 0 else author_text) if author_text else None
            article_report['SUMMARY'] = t[0].get_text() if (t := tuple(article.find_all(class_ = 'com-subhead'))) else None
            article_report['VOLANTA'] = lead_tag.get_text() if (lead_tag := article.find(class_ = 'com-lead')) else None

            if hrefs_set:
                internal_hrefs_set = {href for href in hrefs_set if href[0] == '/'}
                external_hrefs_set = hrefs_set - internal_hrefs_set

                if internal_hrefs_set:
                    article_report['SLUG'] = (slug := list(internal_hrefs_set)[0])
                    article_report['SLUG_INTERNAL'] = True

                    category_list = slug.split('/')
                    while '' in category_list:
                        category_list.remove('')

                    if len(category_list) >= 2:
                        article_report['CATEGORY'] = category_list[0]
                        if len(category_list) >= 3:
                            article_report['SUBCATEGORY'] = category_list[1]
                        else:
                            article_report['SUBCATEGORY'] = None
                    else:
                        article_report['CATEGORY'] = None
                        article_report['SUBCATEGORY'] = None

                elif external_hrefs_set:
                    article_report['SLUG'] = list(external_hrefs_set)[0]
                    article_report['SLUG_INTERNAL'] = False

            else:
                article_report['SLUG'] = None
                article_report['SLUG_INTERNAL'] = None
                article_report['CATEGORY'] = None
                article_report['SUBCATEGORY'] = None

            article_report['Origen'] = self.url
            article_report['FechaFiltro'] = self.capture_datetime
            article_report['FechaCreacion'] = self.capture_datetime
            article_report['FechaModificacion'] = self.capture_datetime

            article_reports[article] = article_report
        
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