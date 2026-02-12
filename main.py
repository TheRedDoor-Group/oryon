from src.scraper import GoogleMapsScraper
from src.sender import WhatsappSender
from src.monitor import WhatsappMonitor

def main():
    print("\n--- 🦁 ORYON: MENU ---")
    print("1. Garimpar Leads (Google Maps)")
    print("2. Disparar Mensagens (WhatsApp)")
    print("3. Monitorar Respostas (Telegram)") # Agora é opção 3

    opcao = input("Escolha: ")
    
    if opcao == "1":
        termo = input("O que buscar? (ex: Pizzaria Mooca): ")
        qtd = int(input("Quantos leads buscar? "))
        GoogleMapsScraper().search(termo, limit=qtd)
        
    elif opcao == "2":
        # Pergunta de segurança
        print("⚠️  ATENÇÃO: Isso vai abrir seu WhatsApp.")
        qtd = int(input("Quantas mensagens enviar agora? (Recomendado: 3-5): "))
        WhatsappSender().enviar_fila(limite_envios=qtd)

    elif opcao == "3":
        # Inicia o monitor (verifique se o .env está com o token!)
        mon = WhatsappMonitor()
        mon.iniciar_vigilia()
        
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()