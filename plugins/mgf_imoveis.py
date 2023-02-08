from bs4 import BeautifulSoup
import requests

_URL = 'https://www.mgfimoveis.com.br/aluguel/apartamento/ce-sobral'


def get_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup
    else:
        raise(f'Status code: {response.status_code}')


def get_all_link_pages(content):
    """ Captura o link de todas as páginas.
        Obs:
        O site em específico tem um problema, toda vez que
        clicamos no link da próxima página o site redireciona
        para a página 1.
    """
    pages = [_URL]
    while True:
        next_page = content.find('a', class_='page-link')['href']
        content = get_content(next_page)
        pages.append(next_page)
        if next_page is None:
            break


def get_all_links_real_estates(pages):
    """ Captura o link de todos os imoveis em todas as páginas. """
    urls = []
    for page in pages:
        rows = page.find(id='slist').find(class_='row')
        for row in rows.find_all(class_='col-12'):
            if row.find('a', class_='h-100') is not None:
                for a_tag in row.find_all('a'):
                    url = a_tag['href']
                    if url != '#':
                        urls.append(url)
    return urls


def get_all_info_real_estate(urls):
    infos = {}
    for url in urls:
        content = get_content(url)
        titulo = content.find('h1', class_='display-6').text
        print(titulo)
        break

def crawler():
    content = get_content(_URL)
    urls = get_all_links_real_estates([content])

if __name__ == '__main__':
    crawler()