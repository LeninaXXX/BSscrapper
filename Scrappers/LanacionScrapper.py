# LanacionScrapper.py -- Scrapper subclass

from Scrappers.Scrapper import Scrapper
from Scrappers.Scrapper import MainArticle
from Scrappers.Scrapper import Article
from Scrappers.Scrapper import Scraps

import bs4 as bs
import lxml

import logging

class LanacionScrapper(Scrapper):    
    def go_scrape(self, ret):
        # First, tuck away raw data:
        soup = bs.BeautifulSoup(ret.text, 'lxml')
        beg_size = len(str(soup))
       
        for discard_tag in ("script", "style"):
            for t in soup.find_all(discard_tag): t.decompose()

        #
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
        # end_of: raw data saving ... soup's already pruned, so no need to reparse it.

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