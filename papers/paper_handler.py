import os
import requests
import argparse
from datetime import date
from arxiv import Search, Client

def fetch_data_arx(paper_id: str):
    # Perform the query
    paper_id = "2308.14711"
    search = Search(id_list = [paper_id], max_results=1)
    # Extract information from the results
    paper = [i for i in Client().results(search)][0]
    return paper

def fetch_data_doi(doi: str):
    url = "https://api.crossref.org/v1/works/doi/" + doi
    return requests.get(url, timeout=180).json()['message']

def write_infos(url, title, summary, publish_date, authors, journal);
    current_date = date.today().strftime("%m/%d/%Y")

    # Create the dir
    n_dirs = [0 for path in os.listdir('./') if os.path.isdir(path)].__len__() + 1
    dir_name = "1_" + str(n_dirs)
    os.mkdir(dir_name)

#   Download , save pdf
    pdf_response = requests,get(paper_url, timeout=180)
    with open(os.path.join(dir_name, dir_name + '.pdf'), 'wb') as f:
        f.write(pdf_response.content)

#   Create .md and edit and save
    title = '# ' + title
    summary = '## Abstract\n' + summary
    publish_date = 'Publish date: ' + publish_date
    current_date = 'Data added to papers: ' + current_date
    authors = 'Authors: ' + authors
    journal = 'Journal: ' + journal
    with open(os.path.join(dir_name, 'README.md'), 'a') as f:
        for info in [title, summary, authors, publish_date, current_date]:
            f.write(info + '\n\n')

def process_arx(paper): 
    publish_date = paper.published.strftime("%m/%d/%Y")
    title = paper.title
    authors = ', '.join([str(auth) for auth in paper.authors])
    summary = paper.summary
    journal = paper.journal_ref or ''

    paper_url = (paper.entry_id + '.pdf').replace('abs', 'pdf')
    write_infos(paper_url, title, summary, publish_date, authors, journal)

def process_doi(paper_info):
    current_date = date.today().strftime("%m/%d/%Y")
    publish_date = paper_info['created']['date-time']
    title = ': '.join(paper_info['title'] + paper_info['subtitle'])
    authors = ''
    for author in paper_info['author']:
        authors += ' '.join([author['given'], author['family']]) + ', '
    summary = ''


    journal = paper_info['container-title'][0]
    subjects = ''
    if 'subject' in paper_info.keys():
        subjects = 'Subjects: ' + ', '.join(paper_info['subject'])

#   Download , save pdf
    paper_url = paper_info['link'][0]['URL']
    write_infos(paper_url, title, summary, publish_date, authors, journal)

# Example usage
def main():
    parser = argparse.ArgumentParser(prog='xarviToMD')
    parser.add_argument('-i', '--id') # Paper id
    parser.add_argument('-a', '--arxiv') # Paper id
    parser.add_argument('-d', '--doi') # Paper id
    args = parser.parse_args()
    if args.arxiv:
        process_arx(fetch_data_arx(args.id)
    else:
        process_doi(fetch_data_doi(args.id)

if __name__ == '__main__':
    main()
