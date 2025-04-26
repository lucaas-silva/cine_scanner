import requests
from bs4 import BeautifulSoup


class Crawler:
    def extract_film_synopsis(self, film):      
        try:
            url = "https://www.adorocinema.com/filmes/" + film +'/'
            response = requests.get(url)
            response.raise_for_status()
            bs_s = BeautifulSoup(response.text, 'html.parser')
            synopsis_tag = bs_s.find('div', class_="content-txt")
            if synopsis_tag:
                return synopsis_tag.get_text(strip=True)
            return 'Synopsis not found.'
        except Exception as e:
            print(f'Error extracting synopsis: {e}')
            return None
    
    def save_film_synopsis(self, film, synopsis):
        with open(f'{film}_synopsis.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(synopsis)

    def find_total_pages(self, film):
        try:
            url = f"https://www.adorocinema.com/filmes/{film}/criticas/espectadores/?page=1"
            response = requests.get(url)
            response.raise_for_status()
            bs = BeautifulSoup(response.text, 'html.parser')
            pagination = bs.find('div', class_='pagination-item-holder')
            if pagination:
                pages = pagination.find_all('span')
                if pages:
                    numbers = [int(page.get_text()) for page in pages if page.get_text().isdigit()]
                    if numbers:
                        return max(numbers)
            return 1
        except Exception as e:
            print(f'Error finding page number: {e}')
            return 1

    def extract_film_comments(self, film, page):
        total_pages = self.find_total_pages(film)
        if page > total_pages:
            print(f'total pages: {total_pages}')
            page = total_pages

        comments = []
        for i in range(1, page + 1):
            try:
                url = 'http://www.adorocinema.com/filmes/' + filme + '/criticas/espectadores/?page=' + str(i)
                response = requests.get(url)
                response.raise_for_status()
                bs_c = BeautifulSoup(response.text, 'html.parser')
                comments_tags = bs_c.find_all('div', class_="content-txt review-card-content")
                for comment_tag in comments_tags:
                    comment = comment_tag.get_text(strip=True)
                    comments.append(comment)
            except Exception as e:
                print(f'Error extracting comment on page {i}: {e}')
                continue
        return comments

    def save_movie_comments(self, film, comments):
        with open(f'{film}_comments.txt', 'w', encoding='utf-8') as output_file:
            for comment in comments:
                output_file.write(comment + '\n')


# filme = input('Digite o código do filme, conforme listado na barra de endereço do site https://www.adorocinema.com/: ')
# n = int(input('Digite quantas páginas de comentários você deseja consultar: '))
filme = 'filme-260627'
n = 7
crawler = Crawler()
sinopse = crawler.extract_film_synopsis(filme)
crawler.save_film_synopsis(filme, sinopse)
comentarios = crawler.extract_film_comments(filme, n)
crawler.save_movie_comments(filme, comentarios)
print('Programa executado com sucesso. Consulte os arquivos gerados com a sinopse e os comentários do filme.')
