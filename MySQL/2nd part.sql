-- PHASE 2 : ACCOUNT + TRANSACTION + LEDGER SYSTEM

USE Bank_database;

-- ACCOUNT TABLE
CREATE TABLE Account (
    Account_No BIGINT AUTO_INCREMENT PRIMARY KEY,
    Branch_ID INT NOT NULL,
    Account_Type ENUM('Savings','Current')NOT NULL,
    Account_Status ENUM('Pending','Active','Frozen','Dormant','Closed')DEFAULT 'Pending',
    Currency_Code CHAR(3) DEFAULT 'INR',
    Current_Balance DECIMAL(18,2) DEFAULT 0.00,
    Available_Balance DECIMAL(18,2) DEFAULT 0.00,
    Open_Date DATE NOT NULL,
    Close_Date DATE NULL,
    Last_Transaction_At DATETIME NULL,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_account_branch FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE RESTRICT
)
AUTO_INCREMENT = 2000000000;

-- SAVINGS ACCOUNT
CREATE TABLE Savings_Account (
    Account_No BIGINT PRIMARY KEY,
    Interest_Rate DECIMAL(5,2) NOT NULL DEFAULT 4.00,
    Minimum_Balance DECIMAL(18,2) DEFAULT 1000.00,
    Withdrawal_Limit_Per_Day DECIMAL(18,2) DEFAULT 50000.00,
    Interest_Calculation ENUM('Daily_Product')DEFAULT 'Daily_Product',
    Last_Interest_Credit_Date DATE NULL,
    CONSTRAINT fk_savings_account FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE CASCADE
);

-- CURRENT 
CREATE TABLE Current_Account (
    Account_No BIGINT NOT NULL,
    Overdraft_Limit DECIMAL(18,2) NOT NULL DEFAULT 100000.00,
    Monthly_Charge DECIMAL(18,2) DEFAULT 250.00,
    Minimum_Balance DECIMAL(18,2) DEFAULT 10000.00,

    PRIMARY KEY (Account_No),

    CONSTRAINT fk_current_account
        FOREIGN KEY (Account_No)
        REFERENCES Account(Account_No)
        ON DELETE CASCADE
);

-- ACCOUNT HOLDER
-- SUPPORTS JOINT ACCOUNTS
CREATE TABLE Account_Holder (
    Account_No BIGINT NOT NULL,
    CIF_No BIGINT NOT NULL,
    Holder_Type ENUM('Primary','Secondary','Guardian','Authorized_Signatory')NOT NULL,
    Ownership_Percentage DECIMAL(5,2) DEFAULT 100.00,
    Added_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY(Account_No, CIF_No),
    CONSTRAINT fk_ah_account FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE CASCADE,
    CONSTRAINT fk_ah_customer FOREIGN KEY(CIF_No) REFERENCES Customer(CIF_No) ON DELETE CASCADE
);

-- NOMINEE TABLE
CREATE TABLE Nominee (
    Nominee_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Account_No BIGINT NOT NULL,
    Nominee_Name VARCHAR(100) NOT NULL,
    Relationship VARCHAR(50),
    DOB DATE,
    Phone_No CHAR(10),
    Share_Percentage DECIMAL(5,2) DEFAULT 100.00,
    CONSTRAINT fk_nominee_account FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE CASCADE
);

-- BENEFICIARY 
CREATE TABLE Beneficiary (
    Beneficiary_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Owner_CIF BIGINT NOT NULL,
    Nickname VARCHAR(100),
    Beneficiary_Name VARCHAR(100) NOT NULL,
    Beneficiary_Account_No BIGINT NOT NULL,
    Beneficiary_IFSC CHAR(11) NOT NULL,
    Beneficiary_Type ENUM('Internal','External')DEFAULT 'Internal',
    Status ENUM('Pending','Active','Blocked')DEFAULT 'Pending',
    Added_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_beneficiary_owner FOREIGN KEY(Owner_CIF) REFERENCES Customer(CIF_No) ON DELETE CASCADE
);

-- TRANSACTION MASTER
CREATE TABLE Transaction_Master (
    Transaction_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Transaction_Type ENUM('Deposit','Withdrawal','Transfer','Interest_Credit','Charge_Debit','Refund')NOT NULL,
    Transaction_Status ENUM('Pending','Success','Failed','Reversed')DEFAULT 'Pending',
    Initiated_By_User VARCHAR(50),
    Reference_Number VARCHAR(100) NOT NULL UNIQUE,
    Remarks VARCHAR(255),
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Completed_At DATETIME NULL,
    CONSTRAINT fk_tm_user FOREIGN KEY(Initiated_By_User) REFERENCES Login_Auth(User_ID) ON DELETE SET NULL
);

-- TRANSACTION ENTRY
-- DOUBLE ENTRY ACCOUNTING
CREATE TABLE Transaction_Entry (
    Entry_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Transaction_ID BIGINT NOT NULL,
    Account_No BIGINT NOT NULL,
    Entry_Type ENUM('Debit','Credit')NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    Balance_After DECIMAL(18,2) NOT NULL,
    Entry_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_te_transaction FOREIGN KEY(Transaction_ID) REFERENCES Transaction_Master(Transaction_ID) ON DELETE CASCADE,
    CONSTRAINT fk_te_account FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE RESTRICT
);

-- DAILY BALANCE
-- USED FOR INTEREST CALCULATION
CREATE TABLE Daily_Balance (
    Account_No BIGINT NOT NULL,
    Balance_Date DATE NOT NULL,
    Closing_Balance DECIMAL(18,2) NOT NULL,
    PRIMARY KEY(Account_No, Balance_Date),
    CONSTRAINT fk_daily_balance_account FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE CASCADE
);

-- ACCOUNT LIMITS
CREATE TABLE Account_Limit (
    Account_No BIGINT PRIMARY KEY,
    Daily_Transfer_Limit DECIMAL(18,2) DEFAULT 100000.00,
    Daily_Withdrawal_Limit DECIMAL(18,2) DEFAULT 50000.00,
    Per_Transaction_Limit DECIMAL(18,2) DEFAULT 25000.00,
    CONSTRAINT fk_account_limit FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE CASCADE
);

-- SUSPICIOUS ACTIVITY LOG
CREATE TABLE Suspicious_Activity_Log (
    Log_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Account_No BIGINT,
    Transaction_ID BIGINT,
    Activity_Type VARCHAR(100),
    Risk_Level ENUM('Low','Medium','High'),
    Description VARCHAR(255),
    Logged_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sal_account FOREIGN KEY(Account_No) REFERENCES Account(Account_No) ON DELETE SET NULL,
    CONSTRAINT fk_sal_transaction FOREIGN KEY(Transaction_ID) REFERENCES Transaction_Master(Transaction_ID) ON DELETE SET NULL
);

-- IMPORTANT INDEXES
CREATE INDEX idx_account_branch			ON Account(Branch_ID);
CREATE INDEX idx_account_status			ON Account(Account_Status);
CREATE INDEX idx_ah_customer			ON Account_Holder(CIF_No);
CREATE INDEX idx_tm_reference			ON Transaction_Master(Reference_Number);
CREATE INDEX idx_tm_created				ON Transaction_Master(Created_At);
CREATE INDEX idx_te_account				ON Transaction_Entry(Account_No);
CREATE INDEX idx_te_transaction			ON Transaction_Entry(Transaction_ID);
CREATE INDEX idx_daily_balance_date		ON Daily_Balance(Balance_Date);

-- IMPORTANT VALIDATION TRIGGERS
DELIMITER $$
CREATE TRIGGER trg_check_positive_transaction_amount
BEFORE INSERT ON Transaction_Entry
FOR EACH ROW
BEGIN
    IF NEW.Amount <= 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Transaction amount must be greater than zero';
    END IF;
END$$
DELIMITER ;

DELIMITER $$
CREATE TRIGGER trg_prevent_closed_account_transaction
BEFORE INSERT ON Transaction_Entry
FOR EACH ROW
BEGIN
    DECLARE acc_status VARCHAR(20);
    SELECT Account_Status INTO acc_status FROM Account WHERE Account_No = NEW.Account_No;
    IF acc_status IN ('Closed', 'Frozen') THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT='Transactions not allowed on closed/frozen account';
    END IF;
END$$
DELIMITER ;

-- DAILY BALANCE EVENT
-- RUNS EVERY DAY
SET GLOBAL event_scheduler = ON;

DELIMITER $$
CREATE EVENT ev_store_daily_balance
ON SCHEDULE
EVERY 1 DAY
STARTS CURRENT_DATE + INTERVAL 1 DAY
DO
BEGIN
    INSERT INTO Daily_Balance(
        Account_No,
        Balance_Date,
        Closing_Balance
    )
    SELECT
        Account_No,
        CURRENT_DATE,
        Current_Balance
    FROM Account
    WHERE Account_Status = 'Active';
END$$
DELIMITER ;

-- SAMPLE CUSTOMERS
# INSERT INTO Customer(Customer_Type,Customer_Status,KYC_Status,Email,Phone_No)VALUES
# ('Individual','Active','Verified','rahul@gmail.com','9876543211'),
# ('Individual','Active','Verified','priya@gmail.com','9876543212');

-- INDIVIDUAL CUSTOMER DETAILS
# INSERT INTO Individual_Customer(CIF_No,Aadhaar,PAN,First_Name,Last_Name,Gender,DOB,Occupation,Annual_Income)VALUES
# (100000000,'123456789012','ABCDE1234F','Rahul','Sharma','Male','2000-05-10','Engineer',800000),
# (100000001,'123456789013','PQRSX5678K','Priya','Verma','Female','2001-08-20','Teacher',600000);

-- SAMPLE ACCOUNTS
# INSERT INTO Account(Branch_ID,Account_Type,Account_Status,Current_Balance,Available_Balance,Open_Date)VALUES
# (1,'Savings','Active',50000.00,50000.00,CURDATE()),
# (1,'Savings','Active',75000.00,75000.00,CURDATE());

-- SAVINGS ACCOUNT DETAILS
# INSERT INTO Savings_Account(Account_No)VALUES
# (2000000000),
# (2000000001);

-- ACCOUNT HOLDERS
# INSERT INTO Account_Holder(Account_No,CIF_No,Holder_Type,Ownership_Percentage)VALUES
# (2000000000,100000000,'Primary',100.00),
# (2000000001,100000001,'Primary',100.00);

-- SAMPLE LOGIN USERS
-- HASHES WILL COME FROM FASTAPI
# INSERT INTO Login_Auth(User_ID,Customer_CIF,Password_Hash,PIN_Hash,Auth_Status)VALUES
# ('rahul_user',100000000,'$2b$12$samplehash','$2b$12$samplepinhash','Active'),
# ('priya_user',100000001,'$2b$12$samplehash','$2b$12$samplepinhash','Active');

-- IMPORTANT NOTES
-- ALL MONEY OPERATIONS:
-- MUST HAPPEN THROUGH FASTAPI SERVICE LAYER.

-- ALWAYS USE:
-- START TRANSACTION
-- SELECT ... FOR UPDATE
-- COMMIT

-- NEVER UPDATE BALANCE DIRECTLY
-- FROM FRONTEND.