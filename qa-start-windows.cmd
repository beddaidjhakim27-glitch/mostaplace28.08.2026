@echo off
setlocal EnableExtensions
cd /d "%~dp0"

echo.
echo === MostaPlace - preparation QA ===
echo Dossier courant : %CD%
echo.

if not exist "package.json" (
  echo ERREUR : package.json est introuvable.
  echo Ce fichier doit etre place dans le dossier racine du projet MostaPlace.
  pause
  exit /b 2
)

if not exist ".env.qa.local" (
  echo ERREUR : .env.qa.local est introuvable.
  echo Creez ce fichier a cote de package.json avant de continuer.
  pause
  exit /b 2
)

where pnpm >nul 2>&1
if errorlevel 1 (
  echo ERREUR : pnpm n'est pas installe ou n'est pas accessible dans cette CMD.
  echo Installez pnpm ou ouvrez une nouvelle fenetre CMD apres son installation.
  pause
  exit /b 2
)

echo Structure du projet : OK
echo Fichier QA : present (valeurs non affichees)
echo.
echo === 1/3 Sessions QA A/B ===
pnpm qa:sessions
if errorlevel 1 (
  echo.
  echo QA BLOQUEE/ECHEC : les sessions QA n'ont pas abouti.
  pause
  exit /b 1
)

echo.
echo === 2/3 Audit Database et permissions ===
pnpm appwrite:db-audit
if errorlevel 1 (
  echo.
  echo AUDIT BLOQUE/ECHEC : la base ou les permissions n'ont pas ete validees.
  pause
  exit /b 1
)

echo.
echo === 3/3 Isolation Storage A/B ===
pnpm storage:isolation-ab
if errorlevel 1 (
  echo.
  echo STORAGE BLOQUE/ECHEC : l'isolation Storage n'a pas ete validee.
  pause
  exit /b 1
)

echo.
echo === CAMPAGNE QA DISTANTE TERMINEE ===
echo Sessions, Database et Storage ont retourne un code de succes.
pause
exit /b 0
