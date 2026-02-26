
import pandas as pd
import requests
import time
import hashlib
import json
import glob
import os
import shutil
from dotenv import load_dotenv # 💡 NOVA BIBLIOTECA: O leitor do nosso "cofre"

# ==========================================
# 1. SUAS CONFIGURAÇÕES GERAIS (AGORA SEGURAS)
# ==========================================
# 💡 PASSO A: Isso manda o Python ler o arquivo .env e carregar as senhas na memória
load_dotenv()

# 💡 PASSO B: Em vez de escrever a senha aqui, usamos os.getenv('NOME_DA_VARIAVEL')
# para pegar a informação que está guardada no cofre de forma segura.
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
SHOPEE_APP_ID = os.getenv('SHOPEE_APP_ID')
SHOPEE_APP_SECRET = os.getenv('SHOPEE_APP_SECRET')
botlink = os.getenv('BOTLINK')
URL_SHOPEE_GRAPHQL = 'https://open-api.affiliate.shopee.com.br/graphql'

# Configuração de Pastas
PASTA_PRODUTOS = 'produtos/'
PASTA_PROCESSADOS = 'produtos_processados/'

# ==========================================
# 2. FUNÇÃO: ENVIAR PARA O TELEGRAM
# ==========================================
def publicar_no_telegram(imagem_url, texto_postagem):
    """
    Envia a postagem formatada para o canal do Telegram.
    """
    url_telegram = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    dados = {
        "chat_id": TELEGRAM_CHAT_ID,
        "photo": imagem_url,
        "caption": texto_postagem,
        "parse_mode": "HTML"
    }

    resposta = requests.post(url_telegram, data=dados)

    if resposta.status_code == 200:
        print("✅ Postagem enviada com sucesso para o Telegram!")
    else:
        print(f"❌ Erro no Telegram: {resposta.text}")


# ==========================================
# 3. FUNÇÃO: BUSCAR IMAGEM COM GRAPHQL
# ==========================================
def pegar_imagem_shopee_graphql(item_id):
    """
    Busca a imagem do produto usando a API Oficial da Shopee.
    """
    query_shopee = f"""
    {{
      productOfferV2(itemId: {item_id}) {{
        nodes {{
          imageUrl
        }}
      }}
    }}
    """

    payload_dict = {"query": query_shopee}
    payload_str = json.dumps(payload_dict, separators=(',', ':'))

    timestamp = str(int(time.time()))
    texto_base = SHOPEE_APP_ID + timestamp + payload_str + SHOPEE_APP_SECRET
    assinatura = hashlib.sha256(texto_base.encode('utf-8')).hexdigest()

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'SHA256 Credential={SHOPEE_APP_ID}, Timestamp={timestamp}, Signature={assinatura}'
    }

    try:
        resposta = requests.post(URL_SHOPEE_GRAPHQL, data=payload_str, headers=headers)
        dados = resposta.json()

        if 'errors' in dados:
            print(f"❌ A Shopee recusou a Query: {dados['errors'][0]['message']}")
            return None

        if 'data' in dados and dados['data'].get('productOfferV2') is not None:
            lista_produtos = dados['data']['productOfferV2']['nodes']
            if len(lista_produtos) > 0:
                return lista_produtos[0]['imageUrl']
            else:
                print(f"⚠️ 0 produtos encontrados para o ID: {item_id}")
                return None
        else:
            print(f"⚠️ Resposta inesperada da API: {dados}")
            return None

    except Exception as e:
        print(f"❌ Erro de conexão com a web: {e}")
        return None


# ==========================================
# 4. FUNÇÃO PRINCIPAL: AUTOMATIZADA
# ==========================================
def processar_planilhas():
    """
    Procura os arquivos CSV na pasta, processa, e move para a pasta de processados.
    """
    # 💡 PASSO A: Garante que a pasta de 'processados' exista
    # O comando 'os.makedirs' cria a pasta. O 'exist_ok=True' diz: "Se a pasta já existir, não dê erro, apenas ignore".
    os.makedirs(PASTA_PROCESSADOS, exist_ok=True)

    padrao_busca = os.path.join(PASTA_PRODUTOS, '*.csv')
    arquivos_csv = glob.glob(padrao_busca)

    if not arquivos_csv:
        print(f"🔎 Nenhum arquivo .csv encontrado na pasta '{PASTA_PRODUTOS}'. O bot vai descansar.")
        return

    print(f"🔎 Encontrado(s) {len(arquivos_csv)} arquivo(s) na pasta. Iniciando automação...\n")

    for caminho_arquivo in arquivos_csv:
        print(f"================")
        print(f"📁 LENDO O ARQUIVO: {caminho_arquivo}")
        print(f"================")

        try:
            tabela = pd.read_csv(caminho_arquivo)

            for index, linha in tabela.iterrows():
                item_id = linha['Item Id']
                nome_produto = linha['Item Name']
                preco = linha['Price']
                link_afiliado = linha['Offer Link']

                print(f"\n[{index + 1}] Processando: {nome_produto}")

                imagem = pegar_imagem_shopee_graphql(item_id)

                if imagem:
                    texto_formatado = f"🔥 <b>PROMOÇÃO IMPERDÍVEL!</b> 🔥\n\n"
                    texto_formatado += f"📦 <b>Produto:</b> {nome_produto}\n"
                    texto_formatado += f"💰 <b>Preço:</b> R$ {preco}\n\n"
                    texto_formatado += f"👉 <b>COMPRE AQUI:</b> {link_afiliado}\n\n"
                    texto_formatado += (f"🤖 <b>Bot de promoções no telegram "
                                        f"🤖:</b> {botlink}\n\n ")

                    publicar_no_telegram(imagem, texto_formatado)
                else:
                    print("Pulando postagem pois a imagem não foi encontrada.")

                time.sleep(5)

                # 💡 PASSO B: Mover o arquivo finalizado
            # Esta linha só roda DEPOIS que todas as linhas do CSV atual foram postadas
            shutil.move(caminho_arquivo, PASTA_PROCESSADOS)
            print(f"✅ Arquivo finalizado e movido para: {PASTA_PROCESSADOS}\n")

        except Exception as e:
            print(f"❌ Ocorreu um erro ao ler a planilha {caminho_arquivo}: {e}")

    print("🎉 Automação concluída! Você pode fechar o programa.")


# ==========================================
# 5. INICIAR O SCRIPT
# ==========================================
if __name__ == "__main__":
    processar_planilhas()