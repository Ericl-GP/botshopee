1 . Crie a estrutura de pastas:
Na mesma pasta onde está o arquivo main.py, crie as seguintes pastas (se ainda não existirem):

produtos/ (Onde você vai colocar as planilhas novas)

produtos_processados/ (Para onde as planilhas vão depois de lidas)

2 .  Configure o seu "Cofre" de senhas:
Crie um arquivo chamado exatamente .env na raiz do projeto e adicione as suas credenciais no formato abaixo (sem aspas e sem espaços antes/depois do =):
==========================================# 1. SUAS CONFIGURAÇÕES GERAIS# ==========================================

TELEGRAM_TOKEN = 'COLOQUE_SEU_TOKEN_DO_BOTFATHER_AQUI'

TELEGRAM_CHAT_ID = '@NOME_DO_SEU_CANAL'

SHOPEE_APP_ID = 'SEU_APP_ID_AQUI'

SHOPEE_APP_SECRET = 'SUA_SENHA_AQUI'

URL_SHOPEE_GRAPHQL = 'https://open-api.affiliate.shopee.com.br/graphql'
--------------------------------------------------------------------------------------------------------------------------------------------------------------
▶️ Como Usar
Acesse o painel de Afiliados da Shopee e gere os seus links em lote.

Baixe o arquivo .csv fornecido pela plataforma.

Coloque este arquivo .csv dentro da pasta produtos/.

Execute o script principal:

Relaxe! O bot fará a leitura, buscará as imagens, postará no seu canal do Telegram e organizará a planilha na pasta de concluídos quando terminar.

📝 Desenvolvido com automação e praticidade em mente para impulsionar vendas de afiliados!
