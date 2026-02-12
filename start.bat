@echo off
title ORYON: LEAD HUNTER - Launcher
echo 🦁 Iniciando ORYON: LEAD HUNTER...
echo Aguarde enquanto o sistema e iniciado...
echo.
echo [AVISO] Esta janela monitora o launcher. Nao a feche.
echo ---------------------------------------------------

:: [1/2] Inicia o Backend (API)
echo [1/2] Ligando Motor Python (API)...
:: Se usar venv, descomente a linha abaixo e ajuste o caminho:
:: start "Oryon Backend" cmd /k "cd backend && ..\venv\Scripts\activate && python -m uvicorn api:app --reload"
start "Oryon Backend API" cmd /k "cd backend && python -m uvicorn api:app --reload"

:: Pequena pausa para o banco de dados/API respirar
timeout /t 3 /nobreak >nul

:: [2/2] Inicia o Frontend (Vite/React/Next)
echo [2/2] Ligando Painel Visual (Frontend)...
start "Oryon Frontend Dashboard" cmd /k "cd frontend && npm run dev"

:: Espera o Vite subir totalmente antes de abrir o navegador
echo Aguardando inicializacao do servidor web...
timeout /t 5 /nobreak >nul

echo ✅ Abrindo interface no navegador...
start http://localhost:5173

echo.
echo ✅ Tudo pronto! Verifique as janelas abertas.
pause