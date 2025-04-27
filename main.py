from crawler import Crawler


if __name__ == '__main__':
    film = input('Enter film code: ')
    pages_to_fetch = int(input('Enter the number of pages: '))
    Crawler().run(film, pages_to_fetch)
