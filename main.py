from src.scraper import GoogleMapsScraper

def main():
    print("--- 🦁 ORYON: LEAD HUNTER ---")
    termo = input("O que você quer buscar? (ex: Pizzaria em Moema SP): ")
    qtd = int(input("Quantos leads? (ex: 5): "))
    
    bot = GoogleMapsScraper()
    bot.search(termo, limit=qtd)

if __name__ == "__main__":
    main()