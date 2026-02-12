from playwright.sync_api import sync_playwright
import time
import random
from .utils import PhoneCleaner
from .database import LeadManager

class GoogleMapsScraper:
    def __init__(self):
        self.cleaner = PhoneCleaner()
        self.db = LeadManager()

    def search(self, query, limit=5):
        print(f"🕵️  Oryon iniciando busca por: {query}")
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            page = browser.new_page()
            
            page.goto(f"https://www.google.com/maps/search/{query}")
            # Espera a barra lateral carregar
            page.wait_for_selector('div[role="feed"]', timeout=60000)

            leads_collected = 0
            
            # Loop principal
            while leads_collected < limit:
                # Pega os cards visíveis
                listings = page.locator('div[role="article"]').all()
                
                print(f"🔎 Encontrados {len(listings)} cards na tela...")

                for card in listings:
                    if leads_collected >= limit: break
                    
                    try:
                        # Pega o nome do aria-label do link dentro do card
                        name = card.get_attribute("aria-label")
                        
                        if not name or "Resultados" in name:
                            continue # Pula se não achou nome válido

                        # Clica para ver o telefone
                        card.click()
                        time.sleep(random.uniform(1.5, 3.0)) # Delay humano

                        # Procura botões que começam com 'phone:'
                        phone_btn = page.locator('button[data-item-id^="phone:"]').first
                        
                        if phone_btn.count() > 0:
                            raw_phone = phone_btn.get_attribute('aria-label')
                            raw_phone = raw_phone.replace("Ligar para: ", "").replace("Ligar para ", "").strip()
                            
                            cleaned = self.cleaner.clean(raw_phone)
                            
                            if cleaned['valid']:
                                saved = self.db.add_lead(
                                    name, raw_phone, cleaned['clean_number'], cleaned['type']
                                )
                                status = "✅ NOVO" if saved else "⚠️ DUPLICADO"
                                print(f"{status} [{cleaned['type']}] {name} -> {cleaned['clean_number']}")
                                if saved: leads_collected += 1
                            else:
                                print(f"❌ Telefone inválido: {raw_phone}")
                        else:
                            print(f"💨 {name}: Sem telefone visível")

                    except Exception as e:
                        # Erros normais de elemento não encontrado, segue o jogo
                        pass

                # Se não atingiu o limite, faz scroll para carregar mais
                if leads_collected < limit:
                    print("🔄 Rolando para baixo...")
                    page.locator('div[role="feed"]').hover()
                    page.mouse.wheel(0, 3000)
                    time.sleep(3)
            
            browser.close()
            print(f"🏁 Fim! {leads_collected} leads novos capturados.")