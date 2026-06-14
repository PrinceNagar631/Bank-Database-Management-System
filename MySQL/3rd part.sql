-- PHASE 3 : LOAN + INTEREST + EMI + AUDIT SYSTEM
-- DATABASE : Band_database
USE Bank_database;

-- LOAN TABLE
CREATE TABLE Loan (
    Loan_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Borrower_CIF BIGINT NOT NULL,
    Branch_ID INT NOT NULL,
    Loan_Type ENUM('Home','Personal','Education','Vehicle','Business')NOT NULL,
    Loan_Status ENUM('Pending','Active','Closed','Defaulted','Rejected')DEFAULT 'Pending',
    Principal_Amount DECIMAL(18,2) NOT NULL,
    Outstanding_Principal DECIMAL(18,2) NOT NULL,
    Interest_Rate DECIMAL(5,2) NOT NULL,
    Penalty_Rate DECIMAL(5,2)DEFAULT 2.00,
    Loan_Term_Months INT NOT NULL,
    EMI_Amount DECIMAL(18,2),
    Total_Paid DECIMAL(18,2)DEFAULT 0.00,
    Start_Date DATE,
    End_Date DATE,
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_loan_customer FOREIGN KEY(Borrower_CIF) REFERENCES Customer(CIF_No) ON DELETE RESTRICT,
    CONSTRAINT fk_loan_branch FOREIGN KEY(Branch_ID) REFERENCES Branch(Branch_ID) ON DELETE RESTRICT
)AUTO_INCREMENT = 3000000000;

-- LOAN INSTALLMENT
CREATE TABLE Loan_Installment (
    Installment_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Loan_ID BIGINT NOT NULL,
    Installment_No INT NOT NULL,
    Due_Date DATE NOT NULL,
    Principal_Component DECIMAL(18,2) NOT NULL,
    Interest_Component DECIMAL(18,2) NOT NULL,
    Penalty_Component DECIMAL(18,2)DEFAULT 0.00,
    Amount_Due DECIMAL(18,2)NOT NULL,
    Amount_Paid DECIMAL(18,2)DEFAULT 0.00,
    Payment_Status ENUM('Pending','Partial','Paid','Overdue') DEFAULT 'Pending',
    Paid_At DATETIME NULL,
    UNIQUE(Loan_ID, Installment_No),
    CONSTRAINT fk_installment_loan FOREIGN KEY(Loan_ID) REFERENCES Loan(Loan_ID) ON DELETE CASCADE
);

-- LOAN PAYMENT
CREATE TABLE Loan_Payment (
    Payment_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Loan_ID BIGINT NOT NULL,
    Installment_ID BIGINT,
    Transaction_ID BIGINT NOT NULL,
    Paid_Amount DECIMAL(18,2) NOT NULL,
    Paid_On TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_lp_loan FOREIGN KEY(Loan_ID) REFERENCES Loan(Loan_ID) ON DELETE CASCADE,
    CONSTRAINT fk_lp_installment FOREIGN KEY(Installment_ID) REFERENCES Loan_Installment(Installment_ID) ON DELETE SET NULL,
    CONSTRAINT fk_lp_transaction FOREIGN KEY(Transaction_ID) REFERENCES Transaction_Master(Transaction_ID) ON DELETE RESTRICT
);

-- LOAN LEDGER
CREATE TABLE Loan_Ledger (
    Ledger_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Loan_ID BIGINT NOT NULL,
    Entry_Type ENUM('Disbursement','EMI_Payment','Interest_Accrual','Penalty','Adjustment') NOT NULL,
    Amount DECIMAL(18,2) NOT NULL,
    Entry_Date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    Remarks VARCHAR(255),
    CONSTRAINT fk_loan_ledger FOREIGN KEY(Loan_ID)REFERENCES Loan(Loan_ID)ON DELETE CASCADE
);

-- INTEREST ACCRUAL
CREATE TABLE Interest_Accrual (
    Accrual_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Account_No BIGINT NOT NULL,
    Accrual_Start_Date DATE NOT NULL,
    Accrual_End_Date DATE NOT NULL,
    Average_Balance DECIMAL(18,2)NOT NULL,
    Interest_Rate DECIMAL(5,2)NOT NULL,
    Interest_Amount DECIMAL(18,2)NOT NULL,
    Posted_Status ENUM('Pending','Posted') DEFAULT 'Pending',
    Posted_At DATETIME NULL,
    CONSTRAINT fk_interest_account FOREIGN KEY(Account_No)REFERENCES Account(Account_No)ON DELETE CASCADE
);

-- CHARGE TABLE
CREATE TABLE Charge_Definition (
    Charge_ID INT AUTO_INCREMENT PRIMARY KEY,
    Charge_Name VARCHAR(100) NOT NULL UNIQUE,
    Charge_Amount DECIMAL(18,2) NOT NULL,
    Charge_Type ENUM('Fixed','Percentage') DEFAULT 'Fixed',
    Applicable_To ENUM('Savings','Current','Loan')
);

-- ACCOUNT CHARGE HISTORY
CREATE TABLE Account_Charge (
    Account_Charge_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Account_No BIGINT NOT NULL,
    Charge_ID INT NOT NULL,
    Transaction_ID BIGINT,
    Charged_Amount DECIMAL(18,2)NOT NULL,
    Charged_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ac_account FOREIGN KEY(Account_No)REFERENCES Account(Account_No)ON DELETE CASCADE,
    CONSTRAINT fk_ac_charge FOREIGN KEY(Charge_ID) REFERENCES Charge_Definition(Charge_ID)ON DELETE RESTRICT,
    CONSTRAINT fk_ac_transaction FOREIGN KEY(Transaction_ID) REFERENCES Transaction_Master(Transaction_ID) ON DELETE SET NULL
);

-- FRAUD MONITORING
CREATE TABLE Fraud_Flag (
    Fraud_ID BIGINT AUTO_INCREMENT PRIMARY KEY,
    Account_No BIGINT,
    Transaction_ID BIGINT,
    Risk_Score DECIMAL(5,2),
    Flag_Type VARCHAR(100),
    Description VARCHAR(255),
    Investigation_Status ENUM('Open','Under_Review','Resolved') DEFAULT 'Open',
    Created_At TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ff_account FOREIGN KEY(Account_No)REFERENCES Account(Account_No)ON DELETE SET NULL,
    CONSTRAINT fk_ff_transaction FOREIGN KEY(Transaction_ID)REFERENCES Transaction_Master(Transaction_ID)ON DELETE SET NULL
);

-- AUDIT TRIGGER : ACCOUNT UPDATE
DELIMITER $$
CREATE TRIGGER trg_account_update_audit
AFTER UPDATE ON Account
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(Table_Name,Operation_Type,Record_Primary_Key,Old_Value,New_Value)
    VALUES(
        'Account',
        'UPDATE',
        OLD.Account_No,
        JSON_OBJECT(
            'Current_Balance',OLD.Current_Balance,
            'Available_Balance',OLD.Available_Balance,
            'Account_Status',OLD.Account_Status
        ),
        JSON_OBJECT(
            'Current_Balance',NEW.Current_Balance,
            'Available_Balance',NEW.Available_Balance,
            'Account_Status',NEW.Account_Status
        )
    );
END$$
DELIMITER ;

-- PREVENT NEGATIVE SAVINGS BALANCE
DELIMITER $$
CREATE TRIGGER trg_prevent_negative_savings
BEFORE UPDATE ON Account
FOR EACH ROW
BEGIN
    DECLARE acc_type VARCHAR(20);
    SELECT Account_Type
    INTO acc_type
    FROM Account
    WHERE Account_No = NEW.Account_No;
    IF acc_type = 'Savings' AND NEW.Current_Balance < 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT ='Savings account balance cannot be negative';
    END IF;
END$$
DELIMITER ;

-- AUTO MARK OVERDUE EMI
DELIMITER $$
CREATE EVENT ev_mark_overdue_installments
ON SCHEDULE
EVERY 1 DAY
DO
BEGIN
    UPDATE Loan_Installment
    SET Payment_Status = 'Overdue' WHERE Due_Date < CURRENT_DATE AND Payment_Status IN ('Pending', 'Partial');
END$$
DELIMITER ;

-- DAILY INTEREST ACCRUAL EVENT
DELIMITER $$
CREATE EVENT ev_calculate_savings_interest
ON SCHEDULE
EVERY 1 MONTH
DO
BEGIN
    INSERT INTO Interest_Accrual(Account_No,Accrual_Start_Date,Accrual_End_Date,Average_Balance,Interest_Rate,Interest_Amount)
    SELECT db.Account_No,MIN(db.Balance_Date),MAX(db.Balance_Date),AVG(db.Closing_Balance),sa.Interest_Rate,(AVG(db.Closing_Balance)*sa.Interest_Rate/100/12)
    FROM Daily_Balance db
    JOIN Savings_Account sa
    ON sa.Account_No = db.Account_No
    GROUP BY db.Account_No;
END$$
DELIMITER ;

-- AUTO POST INTEREST
DELIMITER $$
CREATE EVENT ev_post_interest
ON SCHEDULE
EVERY 1 MONTH
DO
BEGIN
    UPDATE Account a
    JOIN Interest_Accrual ia
    ON a.Account_No = ia.Account_No
    SET
        a.Current_Balance = a.Current_Balance + ia.Interest_Amount,
        a.Available_Balance = a.Available_Balance + ia.Interest_Amount,
        ia.Posted_Status = 'Posted',
        ia.Posted_At = NOW()
    WHERE ia.Posted_Status = 'Pending';
END$$
DELIMITER ;

-- LOAN EMI CALCULATION PROCEDURE
DELIMITER $$
CREATE PROCEDURE Calculate_EMI(
    IN p_loan_id BIGINT
)
BEGIN
    DECLARE p_principal DECIMAL(18,2);
    DECLARE p_rate DECIMAL(10,6);
    DECLARE p_term INT;
    DECLARE emi DECIMAL(18,2);
    SELECT Principal_Amount,Interest_Rate / (12 * 100),Loan_Term_Months
    INTO p_principal, p_rate, p_term
	FROM Loan WHERE Loan_ID = p_loan_id;
    SET emi =(p_principal*p_rate*POW(1 + p_rate, p_term))/(POW(1 + p_rate, p_term) - 1);
    UPDATE Loan
    SET EMI_Amount = emi
    WHERE Loan_ID = p_loan_id;
END$$
DELIMITER ;

-- SAMPLE CHARGES
INSERT INTO Charge_Definition(Charge_Name,Charge_Amount,Charge_Type,Applicable_To)VALUES
('ATM Withdrawal Charge',25.00,'Fixed','Savings'),
('Minimum Balance Penalty',500.00,'Fixed','Savings'),
('Cheque Bounce Penalty',750.00,'Fixed','Current');

-- SAMPLE LOAN
# INSERT INTO Loan(Borrower_CIF,Branch_ID,Loan_Type,Loan_Status,Principal_Amount,Outstanding_Principal,Interest_Rate,Loan_Term_Months,Start_Date,End_Date)VALUES
# (100000000,1,'Personal','Active',500000,500000,10.50,60,CURDATE(),DATE_ADD(CURDATE(), INTERVAL 60 MONTH));

-- CALCULATE EMI
CALL Calculate_EMI(3000000000);

-- IMPORTANT NOTES

-- ALL TRANSFERS:
-- MUST USE FASTAPI TRANSACTION SERVICE.

-- ALWAYS:
-- START TRANSACTION
-- SELECT ... FOR UPDATE
-- COMMIT

-- NEVER:
-- UPDATE BALANCE DIRECTLY
-- FROM FRONTEND/API INPUT.
