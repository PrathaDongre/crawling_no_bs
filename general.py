import os
import pandas as pd
import metadata_parser
#import mysql
import mysql.connector


#attempt to use pandas, adding the crawled and queued links to the dataframe and then getting its metadata.
def create_project_df(file_name_queued):
    print('creating dataframe with crawled links ')
    data = {
    'links':[],
    'meta': []
    }
    df = pd.DataFrame(data)
    list__of_links =[]
    list__of_links = file_to_list(file_name_queued)
    for i in range(len(list__of_links)):
        if i%2 == 0:
            df_links= list__of_links[i]
            df_meta= list__of_links[i+1]
            df.loc[len(df.index)] =  [df_links,df_meta]
    #data_queued = pd.read_csv(file_name_queued, error_bad_lines=False)
    return df

#each website you crawl is a separate project (folder)
def create_project_dir(directory):
  if not os.path.exists(directory):
    print('creating project' + directory)
    os.makedirs(directory)

create_project_dir('wikicrawl')

def create_data_files(project_name,base_url):
  queue = project_name+'/queue.txt'
  crawled = project_name+'/crawled.txt'
  if not os.path.isfile(queue):
    write_file(queue, base_url)
  if not os.path.isfile(crawled):
    write_file(crawled,'')

    #create a new file
def write_file(path,data):
  f=open(path,'w')
  f.write(data)
  f.close()

create_data_files('wikicrawl','https://en.wikipedia.org/wiki/Adjacency_list')

#add data onto an existing file
def append_to_file(path,data):
  with open(path, 'a',  encoding="utf-8") as file:
    file.write(data+'\n')


#delete content of an excisting file
def delete_file_contents(path):
  with open(path,'w'):
    pass

    #'set' can only have unique elements
#read a file and convert each line to set items
#rt : read text file
def file_to_set(file_name):
    results = set()
    with open(file_name,'rt') as f:
        for line in f:
            results.add(line.replace('\n',''))
    return results


 #iterate through a set, each item will be a new line it the file
def set_to_file(links,file):
  delete_file_contents(file)
  for link in sorted(links):
    append_to_file(file,link)

#create new files called meta crawl and queue
create_project_dir('wikicrawl_metalinks')
create_data_files('wikicrawl_metalinks','https://en.wikipedia.org/wiki/Adjacency_list')

#take links from wikicrawl/queue or crawled and append it
#to new file called wikicrawl_metalinks/queue or crawled.
'''with open('wikicrawl/queue.txt', "rt") as f1:
    for url in f1:
        page = metadata_parser.MetadataParser(url)
        new_line  = str(url) +',' +str(page.metadata)
        append_to_file('wikicrawl_metalinks/queue.txt',new_line)
f.close()
#adding both queued and crawled to the same link
with open('wikicrawl/crawled.txt', "rt") as f2:
    for url in f2:
        page = metadata_parser.MetadataParser(url)
        new_line  = url +',' +str(page.metadata)
        append_to_file('wikicrawl_metalinks/queue.txt',new_line)
f.close()'''

#fn similar to file_to_set:
def file_to_list(file_name):
    results = list()
    with open(file_name,'rt') as f:
        for line in f:
            results.append(line.replace('\n',''))
    return results


dataframe_links = create_project_df('wikicrawl_metalinks/queue.txt')
dataframe_links.to_csv(r'D:\Users\Pratha S Dongre\Downloads\web_scraping\web_scraping_crawling_pratha\testproj\df_links.csv')


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="255198"
)

print(mydb)
