import multithreading
import threading
from queue import Queue
from spider import Spider
from domain import *
from general import *

PROJECT_NAME = 'wikicrawl'
STARTPAGE = 'https://en.wikipedia.org/wiki/Adjacency_list'
DOMAIN_NAME = get_domain_name(STARTPAGE)
QUEUE_FILE = PROJECT_NAME + '/queue.txt'
CRAWLED_FILE = PROJECT_NAME + '/crawled.txt'
NUMBER_OF_THREADS = 1
queue =Queue()

Spider(PROJECT_NAME, STARTPAGE, DOMAIN_NAME)

#Create worker threads (will die when main exits)
def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()

#above we created workers, now we need make them work
#while true makes the worker run forever
def work():
    link_id = 0
    while True:
        #send a number here, to crawl_page,
        #there it adds the link to the queue. "link_id"
        url = queue.get()
        Spider.crawl_page(threading.current_thread().name, url, link_id)
        link_id += 1
        queue.task_done()

#each queued link is a new job
def create_jobs():
    for link in file_to_set(QUEUE_FILE):
        queue.put(link)
    queue.join()
    crawl()

#check items in queue, if so crawl them
def crawl():
    queued_links = file_to_set(QUEUE_FILE)
    if len(queued_links) > 0:
        print(str(len(queued_links)) + 'links in the queue')
        create_jobs()

create_workers()
crawl()
