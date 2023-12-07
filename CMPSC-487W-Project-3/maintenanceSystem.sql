CREATE DATABASE maintenanceSystem;

CREATE TABLE users(
    username VARCHAR(30) NOT NULL,
    password VARCHAR(30) NOT NULL,
    name VARCHAR(30),
    type CHAR(1), /* Types: Tenant (T), Staff Member (S), Manager (M) */
    PRIMARY KEY (username)
);

CREATE TABLE tenants(
    tenant_ID INT NOT NULL,  
    name VARCHAR(30), 
    phone_number DECIMAL(10,0), 
    email VARCHAR(50),
    check_in_date DATE,
    check_out_date DATE,
    apartment_number INT,
    username VARCHAR(30) NOT NULL,
    PRIMARY KEY(tenant_ID),
    FOREIGN KEY(username) 
        REFERENCES users(username)
        ON DELETE CASCADE
);

CREATE TABLE requests(
     request_ID INT NOT NULL AUTO_INCREMENT, 
     apartment_number INT, 
     problem_area VARCHAR(30), 
     description VARCHAR(255), 
     time_date DATETIME,
     photo VARCHAR(30),
     status VARCHAR(9),
     PRIMARY KEY(request_ID)
);
