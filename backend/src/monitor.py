from playwright.sync_api import sync_playwright
import time
import os
import winsound  # Gera som
from plyer import notification  # Gera o balãozinho no canto da tela

class WhatsappMonitor:
    def __init__(self):
        # Define onde salvar a sessão
        self.session_path = os.path.abspath(os.path.join("data", "session"))

    def alertar_sistema(self, qtd_mensagens):
        """
        Gera um alerta sonoro e visual no Windows
        """
        print(f"\n🔔 ALERTA: {qtd_mensagens} novas mensagens!")
        
        # Notificação Visual (Balão do Windows)
        try:
            notification.notify(
                title='🦁 ORYON ALERTOU!',
                message=f'Você tem {qtd_mensagens} novos clientes respondendo no WhatsApp!',
                app_name='Oryon',
                timeout=10
            )
        except:
            pass # Se der erro na notificação visual, segue pro som

        # Alerta Sonoro (Sequência de Bips tipo Sirene)
        # Frequência (Hz), Duração (ms)
        try:
            for _ in range(3):
                winsound.Beep(1000, 200) # Agudo
                winsound.Beep(800, 200)  # Grave
        except:
            print("🔊 (Bip sonoro falhou, verifique seu áudio)")

    def iniciar_vigilia(self):
        print("👀 Iniciando Monitoramento Local...")
        print("🔈 Aumente o volume do seu PC.")
        print("❌ Para parar, pressione Ctrl+C no terminal.")

        with sync_playwright() as p:
            browser = None
            try:
                # Abre navegador persistente
                browser = p.chromium.launch_persistent_context(
                    user_data_dir=self.session_path,
                    headless=False,
                    args=["--start-maximized"]
                )
                
                page = browser.pages[0]
                page.goto("https://web.whatsapp.com")
                
                print("⏳ Aguardando carregamento do WhatsApp...")
                try:
                    page.wait_for_selector("#pane-side", timeout=60000)
                    print("✅ Monitor Ativo! Pode minimizar a janela (NÃO FECHE).")
                except:
                    print("❌ Login demorou demais. Tente novamente.")
                    return

                # Teste de som inicial
                winsound.Beep(600, 100)

                while True:
                    # Verifica se o navegador ainda está aberto
                    if page.is_closed():
                        print("❌ Navegador foi fechado manualmente.")
                        break

                    try:
                        # Busca bolinhas verdes (mensagens não lidas)
                        unread_count = page.locator('span[aria-label*="não lida"]').count()
                        
                        if unread_count > 0:
                            self.alertar_sistema(unread_count)
                            
                            # Pausa longa para você atender o cliente (60s)
                            # Assim ele não fica apitando na sua orelha enquanto você digita
                            print("⏸️ Pausando monitor por 60s para você responder...")
                            time.sleep(60) 
                            print("👀 Voltando a monitorar...")
                        else:
                            # Imprime um ponto para mostrar que está vivo
                            print(".", end="", flush=True)

                        time.sleep(5) # Checa a cada 5 segundos
                        
                    except Exception as e:
                        # Se o erro for de navegador fechado, para o loop limpo
                        if "Target closed" in str(e):
                            break
                        print(f"Erro no loop: {e}")
                        time.sleep(5)

            except KeyboardInterrupt:
                print("\n🛑 Monitor parado pelo usuário.")
            
            except Exception as e:
                print(f"\n❌ Erro fatal: {e}")
            
            finally:
                # Fecha o navegador de forma segura (evita aquele erro vermelho gigante)
                if browser:
                    try:
                        browser.close()
                    except:
                        pass