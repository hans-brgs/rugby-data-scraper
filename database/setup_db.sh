#!/bin/bash

# Variables
DB_NAME="rugby_db"
DB_USER="MY_USER_NAME"
DB_PASS="MY_DB_PASS"
MariaDB_PASS="MY_MARIA_DB_PASS"
MariaDB_SCRIPT_FILE="create_tables.sql"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if MySQL/MariaDB is accessible
if command_exists mysql; then
    MYSQL_CMD="mysql"
elif command_exists mariadb; then
    MYSQL_CMD="mariadb"
else
    echo "Error: MySQL/MariaDB is not accessible. Check installation."
    exit 1
fi

# Crée la base de données et l'utilisateur
echo "Database and user creation..."
$MYSQL_CMD -u root -p"$MariaDB_PASS" <<EOF
CREATE DATABASE IF NOT EXISTS $DB_NAME;
CREATE USER IF NOT EXISTS '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS';
GRANT ALL PRIVILEGES ON $DB_NAME.* TO '$DB_USER'@'localhost';
FLUSH PRIVILEGES;
EOF

if [ $? -ne 0 ]; then
    echo "Error during database or user creation."
    echo "Error code : $?"
    exit 1
else
    echo "Database successfully created."
fi

# Configuration de la base de données
echo "Execute SQL script to create tables..."
$MYSQL_CMD -u "$DB_USER" -p"$DB_PASS" "$DB_NAME" < "$(dirname "$0")/$MariaDB_SCRIPT_FILE"

if [ $? -ne 0 ]; then
    echo "Error when executing SQL script."
    echo "Error code : $?"
    exit 1
else
    echo "Database configuration successfully completed."
fi

echo "Press Enter to continue..."
read -r