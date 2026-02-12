# 🦁 ORYON: Lead Hunter & Automation System

Oryon é um sistema Fullstack de prospecção e automação de vendas. Ele captura leads do Google Maps, gerencia uma base de dados local, dispara mensagens automáticas no WhatsApp e monitora respostas em tempo real.

![Status](https://img.shields.io/badge/Status-Active-success)
![Python](https://img.shields.io/badge/Backend-FastAPI-blue)
![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-violet)

## ✨ Funcionalidades

- **🕵️ Garimpo de Leads:** Scraper inteligente que busca empresas no Google Maps e valida telefones (Fixo vs Celular).
- **🚀 Disparador de WhatsApp:** Envia mensagens personalizadas automaticamente simulando um humano (Playwright).
- **👀 Monitor de Respostas:** Vigia o WhatsApp Web e emite alertas sonoros/visuais no Windows quando um cliente responde.
- **📊 Dashboard Interativo:** Interface moderna em React para gerenciar leads e controlar as automações.

---

## 🛠️ Pré-requisitos

Certifique-se de ter instalado na sua máquina:

- **Python 3.10+**: [Download](https://www.python.org/)
- **Node.js 18+**: [Download](https://nodejs.org/)
- **Git**: [Download](https://git-scm.com/)
- **Google Chrome**: Navegador instalado.

---

## 📦 Instalação

Siga os passos abaixo para configurar o projeto pela primeira vez.

### 1. Backend (API Python)

Abra o terminal na pasta `backend`:

```bash
    cd backend

    # Instale as dependências
    pip install -r requirements.txt

    # Instale os navegadores do Playwright
    playwright install chromium
```