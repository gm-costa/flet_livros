from urllib.parse import parse_qs, urlparse
import flet as ft
import requests
from connect import get_livros, URL_API
from functools import partial


def main(page: ft.Page):

    page.title = 'Controle de Livros'
    page.window.width = 400
    # page.theme_mode = ft.ThemeMode.DARK

    def cadastro_livros_page(): 

        titulo_text = ft.Text('Cadastro', size=30, style='Bold')
        nome_input = ft.TextField(label='Nome do livro', autofocus=True)

        streaming_select = ft.Dropdown(
            options=[
                ft.dropdown.Option('A', text='Amazon Klinde'),
                ft.dropdown.Option('F', text='Físico'),
            ],
            label='Selecione a streaming'
        )

        def limpar_controles_livro():
            nome_input.value = ''
            streaming_select.value = ''
            nome_input.focus()

        def carregar_livros():

            def redirect(e, livro_id):
                page.go(f'/review?id={livro_id}')

            lista_livros.controls.clear()

            for livro in get_livros():
                lista_livros.controls.append(
                    ft.Container(
                        ft.Text(livro['nome']),
                        bgcolor=ft.colors.BLACK12,
                        padding=15,
                        alignment=ft.alignment.center,
                        margin=3,
                        border_radius=10,
                        on_click=lambda e, livro_id=livro['id']: page.go(f"/review?id={livro_id}")
                    )
                )
                page.update()

        def cadastrar(e):
            data = {
                'nome': nome_input.value,
                'streaming': streaming_select.value,
                'categorias': [], #TODO: Desenvolver as categorias
            }

            # if not all(list(data.values())):
            if not all([data['nome'], data['streaming']]):
                page.snack_bar = ft.SnackBar(ft.Text('Informe o nome e o streaming!', color='black', size=16), bgcolor='#F3ECD1')

            else:
                try:
                    response = requests.post(f'{URL_API}/livros/', json=data)
                    print(response.json())
                    response_msg = response.json()['status']

                    if response.status_code == 200:

                        limpar_controles_livro()
                        carregar_livros()

                        page.snack_bar = ft.SnackBar(ft.Text(response_msg, color='black'), bgcolor='#D1F3DA')
                    else:
                        page.snack_bar = ft.SnackBar(ft.Text(response_msg, color='black'), bgcolor='#F3ECD1')
                        
                except Exception as e:
                    page.snack_bar = ft.SnackBar(ft.Text(f'Erro: {e}.'), bgcolor='red')

            page.snack_bar.open = True
            nome_input.focus()

            page.update()

        cadastrar_btn = ft.ElevatedButton('Cadastrar', on_click=cadastrar)

        lista_livros = ft.ListView(auto_scroll=True, expand=True)

        carregar_livros()

        page.views.append(
            ft.View(
                '/',
                controls=[
                    titulo_text,
                    nome_input,
                    streaming_select,
                    # categorias_select,
                    cadastrar_btn,
                    lista_livros
                ]
            )
        )

    def review_page(livro_id):
        nota_input = ft.TextField(label='Nota', value='1', width=100, autofocus=True)
        comentario_input = ft.TextField(label='Comentário', multiline=True, expand=True)

        def avaliar(e):
            data = {
                'nota': int(nota_input.value),
                'comentario': comentario_input.value,
            }

            if not data['nota']:
                page.snack_bar = ft.SnackBar(ft.Text('Informe a nota!', color='black', size=16), bgcolor='#F3ECD1')
            else:
                try:
                    response = requests.put(f'{URL_API}/livros/{livro_id}', json=data)
                    if response.status_code == 200:
                        page.snack_bar = ft.SnackBar(ft.Text(response.json()['status'], color='black'), bgcolor='#D1F3DA')
                    else:
                        page.snack_bar = ft.SnackBar(ft.Text(response.json()['status'], color='black'), bgcolor='#F3ECD1')
                
                except Exception as e:
                    page.snack_bar = ft.SnackBar(ft.Text(f'Erro: {e}.'), bgcolor='red')

            page.snack_bar.open = True
            page.update()

        avaliar_btn = ft.ElevatedButton('Avaliar', on_click=avaliar)
        voltar_btn = ft.ElevatedButton('Voltar', on_click=lambda _: page.go('/'))

        page.views.append(
            ft.View(
                '/review',
                controls=[
                    ft.Text('Review page', size=20, text_align=ft.TextAlign.CENTER),
                    ft.Text(f'Detalhes do livro com id: {livro_id}', size=20),
                    nota_input,
                    comentario_input,
                    avaliar_btn,
                    voltar_btn
                ]
            )
        )

    def route_change(e):  # e -> event
        page.views.clear()
        if page.route == '/':
            cadastro_livros_page()
        elif page.route.startswith('/review'):
            parsed_url = urlparse(page.route)
            query_params = parse_qs(parsed_url.query)
            livro_id = query_params['id'][0]
            review_page(livro_id)

        page.update()


    page.on_route_change = route_change
    page.go('/')

ft.app(main)