@echo off
title RAG-Based Intelligent Programming Tutor
echo =====================================================================
echo    RAG-Based Intelligent Programming Tutor with Code Visualization
echo =====================================================================
echo.

:: Check if standard python command exists
where python >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Starting Streamlit Web App using system Python...
    python -m streamlit run app.py
    goto END
)

:: Fallback to local user Python path
set LOCAL_PY="C:\Users\SUMANTH\AppData\Local\Python\bin\python.exe"
if exist %LOCAL_PY% (
    echo Starting Streamlit Web App using Local Python installation...
    %LOCAL_PY% -m streamlit run app.py
    goto END
)

:: Fallback to py launcher
where py >nul 2>nul
if %ERRORLEVEL% equ 0 (
    echo Starting Streamlit Web App using py launcher...
    py -m streamlit run app.py
    goto END
)

echo [ERROR] Python not found on your system!
pause

:END
pause
