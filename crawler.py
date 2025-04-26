import requests
from bs4 import BeautifulSoup


class Crawler:
    def extract_film_synopsis(self, film):      
        try:
            url = "https://www.adorocinema.com/filmes/" + film +'/'
            response = requests.get(url)
            response.raise_for_status()
            bsS = BeautifulSoup(response.text, 'html.parser')
            synopsis_tag = bsS.find('div', class_="content-txt")
            if synopsis_tag:
                return synopsis_tag.get_text(strip=True)
            return 'Synopsis not found.'
        except Exception as e:
            print(f'Error extracting synopsis: {e}')
            return None
    
    def salvarSinopseFilme(self, filme, sinopse):
        arq_saida = open(filme+'_sinopse.txt', 'w',encoding='utf-8')
        for line in sinopse:
            arq_saida.write(line)
        arq_saida.close()

    def extrairComentariosFilme(self, filme, n):
        comentarios = []
        for i in range(1,n+1):
            url = 'http://www.adorocinema.com/filmes/' + filme + '/criticas/espectadores/?page=' + str(i)
            htmlComentarios = requests.get(url).text
            bsC = BeautifulSoup(htmlComentarios, 'html.parser')
            comentarios_com_tags = bsC.find_all('div', class_="content-txt review-card-content")
            for comentario_com_tag in comentarios_com_tags:
                comentarios.append(comentario_com_tag.get_text().strip())
        return comentarios

    def salvarComentariosFilme(self, filme, comentarios):
        arq_saida = open(filme+'_comentarios.txt', 'w', encoding='utf-8')
        for comentario in comentarios:
            arq_saida.write(comentario + '\n\n')
        arq_saida.close()


filme = input('Digite o código do filme, conforme listado na barra de endereço do site https://www.adorocinema.com/: ')
n = int(input('Digite quantas páginas de comentários você deseja consultar: '))
crawler = Crawler()
sinopse = crawler.extract_film_synopsis(filme)
crawler.salvarSinopseFilme(filme, sinopse)
comentarios = crawler.extrairComentariosFilme(filme, n)
crawler.salvarComentariosFilme(filme, comentarios)
print('Programa executado com sucesso. Consulte os arquivos gerados com a sinopse e os comentários do filme.')
