import urllib.request
import re
import time
import sys
import os

# Global variables

host_name = "https://en.wikipedia.org"
wiki_ref = '<a href="\/wiki\/.*?"'
crawled_file_name = "URLsCrawled.txt"
stat_file = "stats.txt"
exclude_word = "Cookie_statement"
file_mode = 'w+'
max_depth = 5
page_size = 0
min_page_size = sys.maxsize
max_page_size = 0


def wiki_crawler(seedUrl, num_pages):
    """ Crawl the wikipedia page with given seed url and number of pages to be crawled
    Args:
        seedUrl: seed URL for crawling
        num_pages: maximum number of pages need to be crawled
    """
    stats = [sys.maxsize, 0, 0, 1] # Storing statistics information 
    page_to_be_crawled = [] # queue data structure
    page_crawled = set() # set storing crawled pages
    page_to_be_crawled.append(seedUrl)
    depth = 0
    f = open(crawled_file_name, file_mode)
    while page_to_be_crawled and len(page_crawled) < num_pages:
        size = len(page_to_be_crawled)
        for i in range(size):
            frontier = page_to_be_crawled.pop(0)
            crawl_links(frontier, page_to_be_crawled, page_crawled, f, stats)
            if len(page_crawled) > num_pages:
                break
        depth += 1
        if depth > max_depth:
            break
    f.close()
    f = open(stat_file, file_mode) 
    f.write("Maximum size: " + str(stats[1]) + " bytes\n")
    f.write("Minimum size: " + str(stats[0]) + " bytes\n")
    f.write("Average size: " + str(stats[2] / num_pages) + " bytes\n")
    f.write("Maximum depth reach: " + str(depth))
    f.close()
    return

def crawl_links(link, page_to_be_crawled, page_crawled, f, stats):
    """ Crawl the current page and looking for wiki page contained 
    Args:
        link: current link
        page_to_be_crawled: a queue storing the pages need to be crawled
        page_crawled: a set storing pages that have be crawled
        f: file where we need to write the content to
        stats: statistics information about the crawling
    """
    page_contents = get_link_content(link, f, stats)
    urls = re.findall(wiki_ref, page_contents)
    for url in urls:
        url = host_name + url[9:-1]
        if url.count(":") <= 1 and "Main_Page" not in url and exclude_word not in url:
            if url not in page_crawled and url not in page_to_be_crawled:
                page_to_be_crawled.append(url)
    page_crawled.add(link)
    return

def get_link_content(link, f, stats):
    """ Get the page's markup html content
    Args:
        link: link where we need to extract information from
        f: file where we need to write the content to
        stats: statistics information about the crawling
    """
    # time.sleep(1) # politeness rule
    save_path = os.getcwd() + "/crawled_files/"
    complete_path_name = os.path.join(save_path, str(stats[3]) + ".txt");
    urllib.request.urlretrieve(link, complete_path_name)
    raw_response = urllib.request.urlopen(link).read()
    size = sys.getsizeof(raw_response)
    stats[0] = min(stats[0], size)
    stats[1] = max(stats[1], size)
    stats[2] += size
    stats[3] += 1
    f.write(link + "\n")
    contents = raw_response.decode('utf-8')
    return contents
