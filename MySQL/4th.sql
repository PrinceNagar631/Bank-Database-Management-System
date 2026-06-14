USE bank_database;
INSERT INTO Customer(
    Customer_Type,
    Email,
    Phone_No
)
VALUES(
    'Individual',
    'admin@gmail.com',
    '9876543210'
);
SELECT * FROM Customer;
INSERT INTO Login_Auth(
    User_ID,
    Customer_CIF,
    Password_Hash,
    PIN_Hash
)
VALUES(
    'admin',
    100000000,
    '$2b$12$5rpTCxzfcwSVcS4BH8VVy.AyCiQIW7F/gNKzvUf1ii5psPWaHYdeW',
    '$2b$12$5rpTCxzfcwSVcS4BH8VVy.AyCiQIW7F/gNKzvUf1ii5psPWaHYdeW'
);
SELECT * FROM Login_Auth;



SELECT * FROM Customer;
SELECT * FROM Individual_Customer;
SELECT * FROM Login_Auth;
SHOW CREATE TABLE Account;
SHOW TABLES;
SELECT * FROM Branch;
SHOW CREATE TABLE Savings_Account;
SHOW CREATE TABLE Current_Account;
SHOW CREATE TABLE Nominee;
SHOW CREATE TABLE Branch;
SHOW CREATE TABLE Account_Holder;
# DROP TABLE Current_Account;

SELECT * FROM Account;
SELECT * FROM Account_Holder;
SELECT * FROM Savings_Account;

SHOW CREATE TABLE Transaction_Master;
SHOW CREATE TABLE Transaction_Entry;
SELECT * FROM Transaction_Master;
SELECT * FROM Transaction_Entry;

SHOW CREATE TABLE Customer;
SHOW CREATE TABLE Login_Auth;

SELECT Account_No, Current_Balance
FROM Account;
SELECT *
FROM Transaction_Entry
ORDER BY Entry_ID DESC;


SHOW CREATE TABLE Beneficiary;
SHOW CREATE TABLE OTP_Store;
SHOW CREATE TABLE Login_History;

SELECT * FROM Login_History ORDER BY Login_History_ID DESC;

SHOW CREATE TABLE Login_Session;
SELECT * FROM Login_Session;

SELECT
    Session_ID,
    User_ID,
    Expiry_Time,
    Session_Status
FROM Login_Session;
SELECT COUNT(*)
FROM Login_Session
WHERE User_ID='admin'
AND Session_Status='Active';

SELECT
    Session_ID,
    User_ID,
    Session_Status,
    Expiry_Time
FROM Login_Session
WHERE User_ID='admin';
SELECT COUNT(*)
FROM Login_Session
WHERE User_ID='admin'
AND Session_Status='Active';

SHOW CREATE TABLE Fraud_Flag;
SHOW CREATE TABLE Suspicious_Activity_Log;
SELECT * FROM suspicious_activity_log;
SHOW CREATE TABLE Audit_Log;
SHOW CREATE TABLE Interest_Accrual;
SHOW CREATE TABLE loan;
SHOW CREATE TABLE loan_installment;
SHOW CREATE TABLE loan_ledger;
SHOW CREATE TABLE loan_payment;
SELECT * FROM Branch;