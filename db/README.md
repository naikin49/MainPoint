# Database Schema and Scripts

## Requirements

1. **Database Management System**:  
   - Microsoft SQL Server 2022.
   - Убедитесь, что сервер настроен на использование аутентификации через логин и пароль.
   - Включите поддержку подключения через **TCP/IP**.

2. **SQL Management Tools**:  
   - Для работы с базой данных используйте **Microsoft SQL Server Management Studio (SSMS)**.

---

## SQL Server Configuration

1. **Install Microsoft SQL Server 2022**:
   - Скачайте и установите SQL Server 2022 с официального сайта Microsoft.

2. **Enable Mixed Mode Authentication**:
   - Во время установки выберите режим **Mixed Mode Authentication** (SQL Server и Windows Authentication).
   - Установите пароль для учетной записи `sa` (суперпользователя SQL Server).

3. **Enable TCP/IP Connections**:
   - Откройте **SQL Server Configuration Manager**.
   - Перейдите в раздел `SQL Server Network Configuration > Protocols for MSSQLSERVER`.
   - Включите протокол **TCP/IP**.
   - Перезапустите службу SQL Server.

4. **Allow Firewall Access**:
   - Убедитесь, что порт **1433** (по умолчанию для SQL Server) открыт в вашем брандмауэре.

5. **Create a New Login**:
   - В SQL Server Management Studio создайте нового пользователя:
     ```sql
     CREATE LOGIN my_user WITH PASSWORD = 'my_secure_password';
     ```
   - Дайте ему доступ к базе данных:
     ```sql
     USE my_database;
     CREATE USER my_user FOR LOGIN my_user;
     ALTER ROLE db_owner ADD MEMBER my_user;
     ```

---

## Files in This Folder

- `schema.sql`: Содержит схему базы данных (скрипты создания таблиц).
- `.\Stored Procedures`: Содержит скрипты создания хранимых процедур.

## Setup Instructions

1. **Create and Configure the Database**:
   - Запустите SQL Server Management Studio (SSMS).
   - Создайте базу данных:
     ```sql
     CREATE DATABASE my_database;
     USE my_database;
     ```

2. **Run SQL Scripts**:
   - Импортируйте таблицы:
     ```sql
     :r schema.sql
     ```
   - Добавьте хранимые процедуры:
     ```sql
     :r procedures.sql
     ```

3. **Connect Your Application**:
   - Настройте подключение в вашем приложении с помощью строки подключения:
     ```
     DRIVER={ODBC Driver 17 for SQL Server};
     SERVER=your_server_ip_or_name;
     DATABASE=my_database;
     UID=my_user;
     PWD=my_secure_password;
     ```
---

## Notes
- Убедитесь, что порт **1433** доступен для вашего приложения.
- Если SQL Server работает локально, используйте `localhost` в строке подключения.
- Для удаленного подключения используйте IP-адрес или доменное имя сервера.