import os
import requests
import argparse
from datetime import date

def fetch_data_doi(doi: str):
    url = "https://api.crossref.org/v1/works/doi/" + doi
    return requests.get(url).json()['message']

def downloadPDF_create_text_doi(paper_info):
    current_date = date.today().strftime("%m/%d/%Y")
    publish_date = paper_info['created']['date-time']
    title = ': '.join(paper_info['title'] + paper_info['subtitle'])
    authors = ''
    for author in paper_info['author']:
        authors += ' '.join([author['given'], author['family']]) + ', '


    journal = paper_info['container-title'][0]
    subjects = ''
    if 'subject' in paper_info.keys():
        subjects = 'Subjects: ' + ', '.join(paper_info['subject'])

    # Create the dir
    n_dirs = [0 for path in os.listdir('./') if os.path.isdir(path)].__len__() + 1
    dir_name = "1_" + str(n_dirs)
    os.mkdir(dir_name)

#   Download , save pdf
    pdf_response = requests.get(paper_info['link'][0]['URL'])
    with open(os.path.join(dir_name, dir_name + '.pdf'), 'wb') as f:
        f.write(pdf_response.content)

#   Create .md and edit and save
    title = '# ' + title
    publish_date = 'Publish date: ' + publish_date
    current_date = 'Data added to papers: ' + current_date
    authors = 'Authors: ' + authors
    journal = 'Journal: ' + journal
    with open(os.path.join(dir_name, 'README.md'), 'a') as f:
        for info in [title, authors, subjects, publish_date, current_date]:
            f.write(info + '\n\n')

# Example usage
def main():
    parser = argparse.ArgumentParser(prog='DOI2MD')
    parser.add_argument('-i', '--doi') # Paper id
    downloadPDF_create_text_doi(fetch_data_doi(parser.parse_args().doi))

main()
