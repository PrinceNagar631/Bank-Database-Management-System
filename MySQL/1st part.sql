-- PHASE 1 : CORE FOUNDATION

DROP DATABASE IF EXISTS Bank_database;
CREATE DATABASE Bank_database;
USE Bank_database;

SET SQL_SAFE_UPDATES = 0;
SET autocommit = 1;

-- ROLE TABLE
CREATE TABLE Role (
    Role_ID INT AUTO_INCREMENT PRIMARY KEY,
    Role_Name VARCHAR(50) NOT NULL UNIQUE,
    Description VARCHAR(255)
);

-- PERMISSION TABLE
CREATE TABLE Permission (
    Permission_ID INT AUTO_INCREMENT PRIMARY KEY,
    Permission_Name VARCHAR(100) NOT NULL UNIQUE,
    Description VARCHAR(255)
);

-- ROLE_PERMISSION TABLE
CREATE TABLE Role_Permission (
    Role_ID INT NOT NULL,
    Permission_ID INT NOT NULL,
    PRIMARY KEY(Role_ID, Permission_ID),
    CONSTRAINT fk_rp_role FOREIGN KEY(Role_ID) REFERENCES Role(Role_ID) ON DELETE CASCADE,
    CONSTRAINT fk_rp_permission FOREIGN KEY(Permission_ID) REFERENCES Permission(Permission_ID) ON DELETE CASCADE
);

-- CUSTOMER TABLE
CREATE TABLE Customer (
    CIF_No BIGINT AUTO_INCREMENT PRIMARY KEY,
    Customer_Type ENUM('Individual','Organization')NOT NULL,
    Customer_Status ENUM('Pending','Active','Frozen','Closed')DEFAULT 'Pending',
    KYC_Status ENUM('Pending','Verified','Rejected')DEFAULT 'Pending',
    Risk_Category ENUM('Low','Medium','High')DEFAULT 'Low',
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone_No CHAR(10) NOT NULL UNIQUE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Updated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CHECK (Phone_No REGEXP '^[0-9]{10}$')
)AUTO_INCREMENT = 100000000;

-- CUSTOMER ADDRESS
CREATE TABLE Customer_Address (
    Address_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    CIF_No BIGINT NOT NULL,
    Address_Type ENUM('Home','Office','Communication')NOT NULL,
    Street VARCHAR(150),
    Town VARCHAR(100),
    District VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100) DEFAULT 'India',
    PIN_Code CHAR(6) NOT NULL,
    CONSTRAINT fk_customer_address FOREIGN KEY(CIF_No) REFERENCES Customer(CIF_No) ON DELETE CASCADE,
    CHECK (PIN_Code REGEXP '^[0-9]{6}$')
);

-- INDIVIDUAL CUSTOMER
CREATE TABLE Individual_Customer (
    CIF_No BIGINT PRIMARY KEY,
    Aadhaar CHAR(12) NOT NULL UNIQUE,
    PAN CHAR(10) NOT NULL UNIQUE,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50),
    Gender ENUM('Male','Female','Other')NOT NULL,
    DOB DATE NOT NULL,
    Occupation VARCHAR(100),
    Annual_Income DECIMAL(18,2),
    CONSTRAINT fk_individual_customer FOREIGN KEY(CIF_No) REFERENCES Customer(CIF_No) ON DELETE CASCADE,
    CHECK (Aadhaar REGEXP '^[0-9]{12}$'),
    CHECK (PAN REGEXP '^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
);

-- ORGANIZATION CUSTOMER
CREATE TABLE Organization_Customer (
    CIF_No BIGINT PRIMARY KEY,
    Organization_Name VARCHAR(150) NOT NULL,
    Registration_No VARCHAR(50) NOT NULL UNIQUE,
    GST_No VARCHAR(20) UNIQUE,
    Industry_Type VARCHAR(100),
    Incorporation_Date DATE,
    CONSTRAINT fk_organization_customer FOREIGN KEY(CIF_No) REFERENCES Customer(CIF_No) ON DELETE CASCADE
);

-- KYC DOCUMENTS
CREATE TABLE KYC_Document (
    Document_ID BIGINT AUTO_INCREMENT UNIQUE,
    CIF_No BIGINT NOT NULL,
    Document_Type ENUM('Aadhaar','PAN','Passport','Driving_License','GST','Incorporation_Certificate')NOT NULL,
    Document_Number VARCHAR(100) NOT NULL,
    Verification_Status ENUM('Pending','Verified','Rejected')DEFAULT 'Pending',
    Uploaded_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_kyc_customer FOREIGN KEY(CIF_No) REFERENCES Customer(CIF_No) ON DELETE CASCADE
);

-- BRANCH TABLE
CREATE TABLE Branch (
    Branch_ID INT AUTO_INCREMENT PRIMARY KEY,
    Branch_Name VARCHAR(100) NOT NULL UNIQUE,
    IFSC_Code CHAR(11) NOT NULL UNIQUE,
    MICR_Code CHAR(9),
    Email VARCHAR(100),
    Contact_Number CHAR(10),
    Street VARCHAR(150),
    Town VARCHAR(100),
    District VARCHAR(100),
    State VARCHAR(100),
    Country VARCHAR(100) DEFAULT 'India',
    PIN_Code CHAR(6),
    Branch_Status ENUM('Active','Inactive')DEFAULT 'Active',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CHECK (PIN_Code REGEXP '^[0-9]{6}$'),
    CHECK (Contact_Number REGEXP '^[0-9]{10}$')
);

-- EMPLOYEE TABLE
CREATE TABLE Employee (
    Employee_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Branch_ID INT NOT NULL,
    First_Name VARCHAR(50) NOT NULL,
    Last_Name VARCHAR(50),
    Email VARCHAR(100) NOT NULL UNIQUE,
    Phone_No CHAR(10) NOT NULL UNIQUE,
    Designation VARCHAR(100) NOT NULL,
    Hire_Date DATE NOT NULL,
    Employee_Status ENUM('Active','Suspended','Resigned')DEFAULT 'Active',
    CONSTRAINT fk_employee_branch FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE RESTRICT,
    CHECK (Phone_No REGEXP '^[0-9]{10}$')
)AUTO_INCREMENT = 500000;

-- EMPLOYEE ROLE
CREATE TABLE Employee_Role (
    Employee_ID BIGINT NOT NULL,
    Role_ID INT NOT NULL,
    Assigned_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(Employee_ID, Role_ID),
    CONSTRAINT fk_er_employee FOREIGN KEY(Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE CASCADE,
    CONSTRAINT fk_er_role FOREIGN KEY(Role_ID) REFERENCES Role(Role_ID) ON DELETE CASCADE
);

-- LOGIN AUTH TABLE
CREATE TABLE Login_Auth (
    User_ID VARCHAR(50) PRIMARY KEY,
    Customer_CIF BIGINT NULL UNIQUE,
    Employee_ID BIGINT NULL UNIQUE,
    Password_Hash VARCHAR(255) NOT NULL,
    PIN_Hash VARCHAR(255),
    Failed_Login_Attempts INT DEFAULT 0,
    Account_Locked_Until DATETIME NULL,
    Last_Login TIMESTAMP NULL,
    MFA_Enabled BOOLEAN DEFAULT FALSE,
    Auth_Status ENUM('Active','Blocked','Disabled')DEFAULT 'Active',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    OTP_Verified TINYINT(1) DEFAULT 0,
    CONSTRAINT fk_login_customer FOREIGN KEY(Customer_CIF) REFERENCES Customer(CIF_No) ON DELETE CASCADE,
    CONSTRAINT fk_login_employee FOREIGN KEY(Employee_ID) REFERENCES Employee(Employee_ID) ON DELETE CASCADE,
    CHECK (
        (Customer_CIF IS NOT NULL AND Employee_ID IS NULL)
        OR
        (Customer_CIF IS NULL AND Employee_ID IS NOT NULL)
    )
);

-- LOGIN SESSION TABLE
CREATE TABLE Login_Session (
    Session_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    User_ID VARCHAR(50) NOT NULL,
    JWT_ID VARCHAR(255) NOT NULL UNIQUE,
    IP_Address VARCHAR(50),
    Device_Info VARCHAR(255),
    Login_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Expiry_Time DATETIME NOT NULL,
    Logout_Time DATETIME NULL,
    Session_Status ENUM('Active','Expired','Logged_Out','Revoked')DEFAULT 'Active',
    CONSTRAINT fk_session_user FOREIGN KEY(User_ID) REFERENCES Login_Auth(User_ID) ON DELETE CASCADE
);

-- LOGIN HISTORY
CREATE TABLE Login_History (
    Login_History_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    User_ID VARCHAR(50) NOT NULL,
    Login_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    IP_Address VARCHAR(50),
    Device_Info VARCHAR(255),
    Login_Status ENUM('Success','Failed')NOT NULL,
    Failure_Reason VARCHAR(255),
    CONSTRAINT fk_login_history_user FOREIGN KEY(User_ID) REFERENCES Login_Auth(User_ID) ON DELETE CASCADE
);

-- OTP STORE
CREATE TABLE OTP_Store (
    OTP_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    User_ID VARCHAR(50) NOT NULL,
    OTP_Hash VARCHAR(255) NOT NULL,
    Purpose ENUM('Login','Transaction','Password_Reset')NOT NULL,
    Generated_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Expires_At DATETIME NOT NULL,
    Is_Used BOOLEAN DEFAULT FALSE,
    CONSTRAINT fk_otp_user FOREIGN KEY(User_ID) REFERENCES Login_Auth(User_ID) ON DELETE CASCADE
);

-- AUDIT LOG
CREATE TABLE Audit_Log (
    Audit_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Table_Name VARCHAR(100) NOT NULL,
    Operation_Type ENUM('INSERT','UPDATE','DELETE')NOT NULL,
    Record_Primary_Key VARCHAR(255),
    Performed_By VARCHAR(50),
    Old_Value JSON,
    New_Value JSON,
    Performed_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- IMPORTANT INDEXES
CREATE INDEX idx_customer_email		ON Customer(Email);
CREATE INDEX idx_customer_phone		ON Customer(Phone_No);
CREATE INDEX idx_employee_branch	ON Employee(Branch_ID);
CREATE INDEX idx_login_customer		ON Login_Auth(Customer_CIF);
CREATE INDEX idx_login_employee		ON Login_Auth(Employee_ID);
CREATE INDEX idx_otp_user			ON OTP_Store(User_ID);
CREATE INDEX idx_audit_table		ON Audit_Log(Table_Name);

-- DEFAULT ROLES
INSERT INTO Role(Role_Name, Description) VALUES
('Admin', 'System Administrator'),
('Branch_Manager', 'Manages Branch'),
('Cashier', 'Handles Cash Transactions'),
('Loan_Officer', 'Handles Loan Processing'),
('Customer', 'Bank Customer');

-- DEFAULT PERMISSIONS
INSERT INTO Permission(Permission_Name, Description) VALUES
('Create_Account', 'Can Create Accounts'),
('Approve_Loan', 'Can Approve Loans'),
('Deposit_Money', 'Can Deposit Money'),
('Withdraw_Money', 'Can Withdraw Money'),
('Transfer_Money', 'Can Transfer Money'),
('View_Audit_Logs', 'Can View Audit Logs');

-- ROLE-PERMISSION MAPPING
INSERT INTO Role_Permission(Role_ID, Permission_ID) VALUES
(1,1),
(1,2),
(1,3),
(1,4),
(1,5),
(1,6),
(2,1),
(2,2),
(3,3),
(3,4),
(5,5);

-- DEFAULT BRANCH
INSERT INTO Branch(Branch_Name, IFSC_Code, MICR_Code, Email, Contact_Number, Street, Town, District, State, PIN_Code)
VALUES('Main Branch','BAND0000001','123456789','mainbranch@bandbank.com','9876543210','Central Road','Indore','Indore','Madhya Pradesh','452001');

-- =========================================================
-- IMPORTANT NOTES
-- =========================================================

-- PASSWORD_Hash:
-- Store bcrypt/argon2 hash ONLY.

-- PIN_Hash:
-- Store hashed transaction PIN only.

-- JWT blacklist/session revocation
-- handled using Login_Session table.

-- Business logic should be in FastAPI,
-- not large SQL triggers.