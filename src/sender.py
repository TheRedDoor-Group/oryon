from playwright.sync_api import sync_playwright
import time
import random
import urllib.parse
import os
from .database import LeadManager

class WhatsappSender:
    def __init__(self):
        self.db = LeadManager()
        self.session_path = os.path.abspath(os.path.join("data", "session"))
        
        self.saudacoes = [
            "Oi, é da {nome}?",
            "Olá, tudo bem? É da {nome}?",
            "Opa, bom dia. Falo com o responsável da {nome}?",
            "Olá, vi o contato da {nome} no Google. É por aqui o atendimento?"
        ]

    def enviar_fila(self, limite_envios=3):
        leads = self.db.get_leads_to_contact(limit=limite_envios)
        
        if not leads:
            print("💤 Nenhum lead novo (mobile) para enviar.")
            return

        print(f"🚀 Iniciando disparo para {len(leads)} leads...")

        with sync_playwright() as p:
            try:
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=self.session_path,
                    headless=False,
                    args=["--start-maximized", "--no-sandbox"]
                )
            except Exception as e:
                print(f"❌ Erro ao abrir navegador: {e}")
                return

            page = browser.pages[0]
            print("📱 Acessando WhatsApp Web...")
            page.goto("https://web.whatsapp.com")
            
            try:
                print("⏳ Aguardando login...")
                page.wait_for_selector("#pane-side", timeout=60000) 
                print("✅ WhatsApp Conectado!")
            except:
                print("❌ Tempo esgotado! Login não detectado.")
                browser.close()
                return

            for lead in leads:
                id_lead, nome_empresa, telefone = lead
                
                msg_base = random.choice(self.saudacoes)
                mensagem = msg_base.format(nome=nome_empresa)
                
                print(f"📤 Enviando para: {nome_empresa} ({telefone})...")

                # Estratégia Híbrida: Link preenche, mas Robot confirma
                texto_encoded = urllib.parse.quote(mensagem)
                link = f"https://web.whatsapp.com/send?phone={telefone}&text={texto_encoded}"
                
                page.goto(link)
                
                try:
                    print("⏳ Aguardando chat carregar...")
                    
                    # Espera a caixa de texto aparecer (div editável)
                    # Esse seletor é o campo onde digita a mensagem
                    caixa_texto = page.wait_for_selector('div[contenteditable="true"]', timeout=30000)
                    time.sleep(1) # Respiro
                    
                    # "Acorda" a interface
                    caixa_texto.click() # Garante o foco
                    
                    # Digita um espaço e apaga. Isso força o botão 'Enviar' a aparecer.
                    page.keyboard.press("Space")
                    page.keyboard.press("Backspace")
                    time.sleep(1) 

                    # Tenta Clicar no Botão Enviar (Prioridade)
                    botao_enviar = page.locator('span[data-icon="send"]')
                    
                    if botao_enviar.is_visible():
                        print("👉 Clicando no botão enviar...")
                        botao_enviar.click()
                    else:
                        print("⌨️ Botão não visível, tentando ENTER...")
                        page.keyboard.press("Enter")
                    
                    print("✅ Mensagem enviada!")
                    self.db.mark_hello_sent(telefone)
                    
                    tempo_espera = random.randint(10, 20)
                    print(f"☕ Aguardando {tempo_espera}s...")
                    time.sleep(tempo_espera)

                except Exception as e:
                    # Checa se é número inválido
                    if page.locator('div[data-animate-modal-popup="true"]').count() > 0:
                        print(f"❌ Número inválido (sem WhatsApp): {telefone}")
                    else:
                        print(f"⚠️ Erro no envio: {e}")
            
            print("🏁 Fila finalizada.")
            time.sleep(2)
            browser.close()