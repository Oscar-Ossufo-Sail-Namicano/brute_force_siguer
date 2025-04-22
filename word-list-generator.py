# Nomes próprios comuns em Moçambique
nomes = [
    "jose", "amina", "maria", "fernando", "joaquim"
]

# Em um pentest real, devem ter so nomes do alvo que pretende atacar para evitar gerar wordlist gran
# Mas como este script ee educacional, deixo esses todos nomes so para fins didaticos

# Sobrenomes/sufixos opcionais
sobrenomes = [
    "", "cumbe", "gove", "nhantumbo"
]

# Anos e datas prováveis
anos = [str(i) for i in range(0, 2025)]

# Sufixos realistas de senha
sufixos = ["", "123", "@2024", "!", "#mz", "_mz", "@up", "@"]
 
# Limite de combinações por nome completo (para não gerar milhões)
LIMIT_POR_COMBINACAO = 10_000

# Geração de combinações
wordlist = set() # Remove duplicações automáticas
'''
exemplo de funcionamento do set:
            lista = ["ana2024", "ana2024", "carlos2024"]
            conjunto = set(lista)
            print(conjunto)

            {'ana2024', 'carlos2024'}

'''

for nome in nomes:
    for sobrenome in sobrenomes:
        base = nome + sobrenome
        for ano in anos:
            for sufixo in sufixos:
                senha = base + ano + sufixo
                wordlist.add(senha.capitalize())

# Salvar no arquivo
with open("senhas.txt", "w", encoding="utf-8") as f:
    for senha in sorted(wordlist):
        f.write(senha + "\n")

print(f"[#] Wordlist gerada com {len(wordlist)} senhas realistas.")
