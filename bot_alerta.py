import logging
import json
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurações de log
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Caminho do arquivo de persistência
ARQUIVO_DADOS = "palavras.json"

# Dicionário global de palavras por usuário
usuarios_palavras = {}

# Função para carregar dados do arquivo JSON
def carregar_dados():
    global usuarios_palavras
    if os.path.exists(ARQUIVO_DADOS):
        with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
            usuarios_palavras = json.load(f)
            # Converte listas para sets
            for k in usuarios_palavras:
                usuarios_palavras[k] = set(usuarios_palavras[k])
    else:
        usuarios_palavras = {}

# Função para salvar dados no arquivo JSON
def salvar_dados():
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        # Converte sets para listas
        json.dump({k: list(v) for k, v in usuarios_palavras.items()}, f, ensure_ascii=False, indent=2)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = (
        "Olá. Seja muito bem-vindo!\n\n"
        "Esse bot vai te notificar sobre produtos que deseja após cadastrar as palavras-chave.\n\n"
        "/add ex:cupom - Adiciona uma palavra chave de notificação\n"
        "/lista - Mostra a lista com todas suas palavras chaves cadastradas\n"
        "/apagar ex:cupom - Remove a palavra-chave da lista\n\n"
        "Veja o exemplo, para adicionar use:\n"
        "/add s23 ultra\n\n"
        "Adicione uma palavra e receba a notificação sempre que houver uma oferta do mesmo."
    )
    await update.message.reply_text(msg)

# Comando /add
async def add_palavra(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = str(update.effective_user.id)
    palavra = " ".join(context.args).strip()

    if not palavra:
        await update.message.reply_text("Por favor, informe a palavra-chave. Ex: /add notebook")
        return

    usuarios_palavras.setdefault(user_id, set()).add(palavra.lower())
    salvar_dados()
    await update.message.reply_text(f"✅ Palavra-chave '{palavra}' adicionada com sucesso!")

# Função principal
def main():
    carregar_dados()

    application = Application.builder().token("8111344047:AAHBTZltGGKR9se-6vE4OwehnCU6jRaNQPs").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("add", add_palavra))

    logging.info("Bot está pronto para receber mensagens!")
    application.run_polling()

if __name__ == "__main__":
    main()
