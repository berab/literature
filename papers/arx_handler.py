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
    journal = paper.journal_ref or ''
    # Create the dir
    n_dirs = len([0 for path in os.listdir('./') if os.path.isdir(path)]) + 1
    dir_name = "1_" + str(n_dirs)
    os.mkdir(dir_name)

    # Download , save pdf
    pdf_response = requests.get((paper.entry_id + '.pdf').replace('abs', 'pdf'), timeout=180)
    with open(os.path.join(dir_name, dir_name + '.pdf'), 'wb') as f:
        f.write(pdf_response.content)

    # Create .md and edit and save
    title = '# ' + title
    summary = '## Abstract\n' + summary
    publish_date = 'Publish date: ' + publish_date
    current_date = 'Data added to papers: ' + current_date
    authors = 'Authors: ' + authors
    journal = 'Journal: ' + journal
    with open(os.path.join(dir_name, 'README.md'), 'a', encoding='utf-8') as f:
        for info in [title, summary, authors, publish_date, current_date]:
            f.write(info + '\n\n')

if __name__ == '__main__':
    def main():
        """
            Example usage
        """
        parser = argparse.ArgumentParser(prog='xarviToMD')
        parser.add_argument('-i', '--id') # Paper id
        downloadPDF_create_text_arx(fetch_data_arx(parser.parse_args().id))
    main()
