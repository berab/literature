import os
import requests
import argparse
from datetime import date
from arxiv import Search, Client

def fetch_data_arx(paper_id):
    # Perform the query
    paper_id = "2308.14711"
    search = Search(id_list = [paper_id], max_results=1)
    # Extract information from the results
    paper = [i for i in Client().results(search)][0]
    return paper

def downloadPDF_create_text_arx(paper):
    current_date = date.today().strftime("%m/%d/%Y")
    publish_date = paper.published.strftime("%m/%d/%Y")
    title = paper.title
    authors = ', '.join([str(auth) for auth in paper.authors])
    summary = paper.summary
    journal = ''
    if paper.journal_ref:
        journal = journal_ref

    # Create the dir
    n_dirs = [0 for path in os.listdir('./') if os.path.isdir(path)].__len__() + 1
    dir_name = "1_" + str(n_dirs)
    os.mkdir(dir_name)

#   Download , save pdf
    pdf_response = requests.get((paper.entry_id + '.pdf').replace('abs', 'pdf'))
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
# Example usage
def main():
    parser = argparse.ArgumentParser(prog='xarviToMD')
    parser.add_argument('-i', '--id') # Paper id
    downloadPDF_create_text_arx(fetch_data_arx(parser.parse_args().id))

main()
