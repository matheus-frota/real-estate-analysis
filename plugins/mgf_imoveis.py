from bs4 import BeautifulSoup
import requests
import json

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


def get_cond_price(content):
    try:
        value = content.find('p', class_='pl-4').text
        if 'CONDOM' in value:
            return value
        return None
    except AttributeError:
        return None


def get_total_price(content):
    try:
        value = content.find('p', class_='h5 mt-4').text
        if 'TOTAL' in value:
            return value
        return None
    except AttributeError:
        return None


def get_bedroom_qty(content):
    try:
        value = [i.text for i in content.find_all('h4', class_='fw-light mb-4')][0]
        if 'Dormitório' in value:
            return value
        return None
    except AttributeError:
        return None


def get_bathroom_qty(content):
    try:
        value = [i.text for i in content.find_all('h4', class_='fw-light mb-4')][1]
        if 'Banheiro' in value:
            return value
        return None
    except AttributeError:
        return None


def get_garage_qty(content):
    try:
        value = [i.text for i in content.find_all('h4', class_='fw-light mb-4')][2]
        if 'garagem' in value:
            return value
        return None
    except AttributeError:
        return None


def get_total_area(content):
    try:
        value = [i.text for i in content.find_all('h4', class_='fw-light mb-4')][3]
        if 'Área' in value:
            return value
        return None
    except AttributeError:
        return None


def get_all_info_real_estate(urls):
    infos = []
    for url in urls:
        content = get_content(url)
        print(url)
        info = {
            'codigo': content.find('p', class_='fs-6 fw-light badge bg-secondary me-2 mb-2 mb-sm-0').text,
            'titulo': content.find('h1', class_='display-6').text,
            'endereco': ', '.join(
                [i.text for i in content.find('h2', class_='fs-4').find_all('a')]),
            'ultima_atualizacao': content.find('p', class_='fs-6 fw-light badge bg-secondary me-2 mb-0').text,
            'preco': [i.text for i in content.find_all('h3', class_='mb-4')][1],
            'preco_condominio': get_cond_price(content),
            'preco_total': get_total_price(content),
            'quantidade_dormitorios': get_bedroom_qty(content),
            'quantidade_banheiros': get_bathroom_qty(content),
            'quantidade_vagas_garagem': get_garage_qty(content),
            'area': get_total_area(content)
        }
        infos.append(info)
    return infos

def crawler():
    content = get_content(_URL)
    urls = get_all_links_real_estates([content])
    infos = get_all_info_real_estate(urls)

    with open('data.json', 'w') as f:
        json.dump(infos, f)

if __name__ == '__main__':
    crawler()