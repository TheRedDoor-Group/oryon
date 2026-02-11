from src.scraper import GoogleMapsScraper
from src.sender import WhatsappSender

def main():
    print("\n--- 🦁 ORYON: MENU ---")
    print("1. Garimpar Leads (Google Maps)")
    print("2. Disparar Mensagens (WhatsApp)")
    opcao = input("Escolha (1 ou 2): ")
    
    if opcao == "1":
        termo = input("O que buscar? (ex: Pizzaria Mooca): ")
        qtd = int(input("Quantos leads buscar? "))
        GoogleMapsScraper().search(termo, limit=qtd)
        
    elif opcao == "2":
        # Pergunta de segurança
        print("⚠️  ATENÇÃO: Isso vai abrir seu WhatsApp.")
        qtd = int(input("Quantas mensagens enviar agora? (Recomendado: 3-5): "))
        WhatsappSender().enviar_fila(limite_envios=qtd)
        
    else:
        print("Opção inválida.")

if __name__ == "__main__":
    main()