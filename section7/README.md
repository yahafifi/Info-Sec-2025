# 🧪 MySQL Access Control Lab – Command Summary

## 🗂️ 1. Create Database and Table

```sql
-- Login to MySQL

mysql -u root -p --socket=/opt/lampp/var/mysql/mysql.sock

-- Create a new database
CREATE DATABASE company;
USE company;

-- Create a sample table
CREATE TABLE employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50),
    salary DECIMAL(10,2),
    department VARCHAR(50)
);
```

---

## 🧾 2. Insert Sample Data

```sql
INSERT INTO employees (name, salary, department) VALUES
('Ali', 10000, 'HR'),
('Mona', 12000, 'IT'),
('Kareem', 9000, 'Finance');
```

---

## 👤 3. Create Users

```sql
CREATE USER 'employee1'@'localhost' IDENTIFIED BY 'pass123';
CREATE USER 'manager1'@'localhost' IDENTIFIED BY 'admin123';
```

---

## 🔐 4. Grant Permissions

```sql
-- Grant limited SELECT to employee1
GRANT SELECT (name, department) ON company.employees TO 'employee1'@'localhost';

-- Grant full access to manager1
GRANT SELECT, INSERT, UPDATE, DELETE ON company.employees TO 'manager1'@'localhost';
```

---

## 🧪 5. Test User Permissions

```bash
# Login as employee1
mysql -u employee1 -p
```

```sql
-- Allowed
USE company;
SELECT name, department FROM employees;

-- Denied (should throw error)
UPDATE employees SET salary = 20000 WHERE name = 'Ali';
```

---

## 🚫 6. Revoke Permissions

```sql
REVOKE INSERT ON company.employees FROM 'manager1'@'localhost';
```

---

## 📝 7. View Current Privileges

```sql
SHOW GRANTS FOR 'employee1'@'localhost';
SHOW GRANTS FOR 'manager1'@'localhost';
```

---

## 📌 8. Drop User (Optional Cleanup)

```sql
DROP USER 'employee1'@'localhost';
DROP USER 'manager1'@'localhost';
```
