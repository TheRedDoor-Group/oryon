from src.database import LeadManager
from src.utils import PhoneCleaner

def adicionar_teste():
    db = LeadManager()
    cleaner = PhoneCleaner()

    print("--- 🧪 MODO DE TESTE: ADICIONAR LEAD MANUAL ---")
    nome = input("Nome do Teste (ex: Eu Mesmo): ")
    telefone = input("Seu Número (com DDD, ex: 11999998888): ")

    # Limpa o telefone usando a mesma lógica do scraper
    resultado = cleaner.clean(telefone)

    if resultado['valid'] and resultado['type'] == 'mobile':
        # Salva no banco
        sucesso = db.add_lead(
            name=nome,
            phone_raw=telefone,
            phone_clean=resultado['clean_number'],
            lead_type='mobile'
        )
        
        if sucesso:
            print(f"✅ Sucesso! {nome} ({resultado['clean_number']}) foi salvo.")
            print("Agora rode o 'main.py' e escolha a opção 2!")
        else:
            print("⚠️ Esse número já está no banco de dados!")
    else:
        print("❌ Número inválido! Certifique-se de colocar DDD + 9 dígitos.")

if __name__ == "__main__":
    adicionar_teste()