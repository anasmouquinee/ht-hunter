@echo off
title Industrial Hunter Daemon - 6H Auto Research & Email Digest
cd /d "%~dp0\.."
echo =====================================================================
echo  INDUSTRIAL HUNTER DAEMON (HOUDA TAZI - GENIE INDUSTRIEL)
echo  Cycle de veille automatique : Toutes les 6 heures
echo =====================================================================
python run_agent.py --loop --interval-hours 6 --live
pause
