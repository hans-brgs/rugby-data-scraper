@echo off
setlocal EnableDelayedExpansion

:: Variables
set "DB_NAME=MY_DATABASE_NAME"
set "DB_USER=MY_USER_NAME"
set "DB_PASS=MY_DATABASE_PASSWORD"
set "MariaDB_PASS=MARIADB_PASSWORD"
set "MariaDB_PATH=C:\Program Files\MariaDB 11.5\bin\"
set "MariaDB_SCRIPT_FILE=create_tables.sql"

:: Check if MariaDB/MySQL is accessible
"%MariaDB_PATH%mysql.exe" --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Erreur : MySQL is not accessible. Check the path and installation. Path : %MariaDB_PATH%
    goto :EOF
)

:: Creates DB and user
echo Creating database and user...
"%MariaDB_PATH%mysql.exe" -u root -p%MariaDB_PASS% -e "CREATE DATABASE IF NOT EXISTS %DB_NAME%; CREATE USER IF NOT EXISTS '%DB_USER%'@'localhost' IDENTIFIED BY '%DB_PASS%'; GRANT ALL PRIVILEGES ON %DB_NAME%.* TO '%DB_USER%'@'localhost'; FLUSH PRIVILEGES;"
if %ERRORLEVEL% neq 0 (
    echo Error during database or user creation.
    echo Error code : %ERRORLEVEL%
	goto :EOF
) else (
    echo DB successfully created.
)

:: Set Up DB
echo Run a SQL script to create tables...
"%MariaDB_PATH%mysql.exe" -u %DB_USER% -p%DB_PASS% %DB_NAME% < "%~dp0%MariaDB_SCRIPT_FILE%"
if %ERRORLEVEL% neq 0 (
    echo Error when executing SQL script.
    echo Error code : %ERRORLEVEL%
    goto :EOF
) else (
    echo DB setup completed successfully.
)
	
pause
endlocal