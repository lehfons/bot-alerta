import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configurações de log para ajudar na depuração
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Função de resposta ao comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Olá! Eu sou o seu bot. Como posso te ajudar?')

# Função principal para configurar o bot e rodar o polling
def main():
    # Substitua pelo seu token
    application = Application.builder().token("8111344047:AAHBTZltGGKR9se-6vE4OwehnCU6jRaNQPs").build()

    # Adiciona o handler para o comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o bot e começa a ouvir as mensagens
    logging.info("Bot está pronto para receber mensagens!")
    application.run_polling()  # Apenas chame a função de polling diretamente

if __name__ == "__main__":
    main()  # Apenas chama a função main diretamente
