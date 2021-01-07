from random import choice

from faker import Faker
from locust import task, between, HttpUser
from pyquery import PyQuery as pq

fake = Faker('pt_BR')


class MeuUsuario(HttpUser):
    wait_time = between(0.5, 10)

    def post(self, resposta_com_form, referer, path, data):
        arvore = pq(resposta_com_form.text)
        csrf_token_cookie = resposta_com_form.cookies['csrftoken']
        csrf_token = arvore("input[name='csrfmiddlewaretoken']").val()
        data["csrfmiddlewaretoken"] = csrf_token
        return self.client.post(
            path,
            data, headers={
                'X-CSRFToken': csrf_token,
                'Referer': referer
            },
            catch_response=True)

    @task(10)
    def responder_questionario(self):
        resposta = self.client.get('/')
        self.wait()
        email = fake.email()
        referer = self.host + '/'
        resposta = self.post(resposta, referer, '/', {'nome': fake.name(), 'email': email})
        with resposta as resposta:
            if not resposta.url.endswith('/perguntas/1'):
                resposta.failure('Não redirecionou para primeira pergunta')
            if resposta.elapsed.total_seconds() > 30:
                resposta.failure('Demorou demais')
        url_atual = resposta.url
        alternativas = '0 1 2 3'.split()
        while 'classificacao' not in url_atual:
            alternativa_escolhida = choice(alternativas)
            resposta = self.post(resposta, referer, url_atual, {'resposta_indice': alternativa_escolhida})
            referer = url_atual
            with resposta as resposta:
                if resposta.status_code != 200:
                    resposta.failure(f'{email} Falhou no envio da reposta: {resposta.status_code}')
                    print(email, resposta.status_code, referer, url_atual)
                    break
            url_atual = resposta.url
            print(email, url_atual, )
            self.wait()
        print(email, url_atual, 'fim')

    @task(1)
    def ver_classificacao(self):
        resposta = self.client.get('/')
        self.wait()
        email = fake.email()
        referer = self.host + '/'
        resposta = self.post(resposta, referer, '/', {'nome': fake.name(), 'email': email})
        with resposta as resposta:
            if not resposta.url.endswith('/perguntas/1'):
                resposta.failure('Não redirecionou para primeira pergunta')
            if resposta.elapsed.total_seconds() > 30:
                resposta.failure('Demorou demais')

        resposta = self.client.get('/classificacao')
        print(email, resposta.url, resposta.status_code)
