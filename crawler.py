from bs4 import BeautifulSoup
from comment_evaluator import CommentEvaluator
import requests
import time
import random


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
}


class Crawler:
    def extract_film_synopsis(self, film):      
        try:
            url = f'https://www.adorocinema.com/filmes/{film}/'
            response = requests.get(url, headers=HEADERS)
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
        with open(f'files/{film}_synopsis.txt', 'w', encoding='utf-8') as output_file:
            output_file.write(synopsis)

    def find_total_pages(self, film):
        try:
            url = f'https://www.adorocinema.com/filmes/{film}/criticas/espectadores/?page=1'
            response = requests.get(url, headers=HEADERS)
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
                url = f'https://www.adorocinema.com/filmes/{film}/criticas/espectadores/?page={i}'
                response = requests.get(url, headers=HEADERS)
                response.raise_for_status()
                bs_c = BeautifulSoup(response.text, 'html.parser')
                comments_tags = bs_c.find_all('div', class_="content-txt review-card-content")
                for comment_tag in comments_tags:
                    comment = comment_tag.get_text(strip=True)
                    comments.append(comment)
                time.sleep(random.uniform(1, 3))
            except Exception as e:
                print(f'Error extracting comment on page {i}: {e}')
                continue
        return comments

    def save_movie_comments(self, film, comments):
        comment_evaluator = CommentEvaluator()
        with open(f'files/{film}_comments.txt', 'w', encoding='utf-8') as output_file:
            for comment in comments:
                output_file.write(comment + '\n')
                output_file.write(comment_evaluator.evaluate_comment(comment) + '\n\n')

    def run(self, film, pages_to_fetch):
        print('Starting the crawler...')
        synopsis = self.extract_film_synopsis(film)
        if synopsis:
            self.save_film_synopsis(film, synopsis)
            print('Synopsis saved.')
        else:
            print('Synopsis not found.')

        comments = self.extract_film_comments(film, pages_to_fetch)
        if comments:
            self.save_movie_comments(film, comments)
            print('Comments saved.')
        else:
            print('No comments found.')
        print('Crawler finished.')
