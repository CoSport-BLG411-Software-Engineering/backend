DROP TABLE IF EXISTS activeUserTable;

CREATE TABLE activeUserTable (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    u_name VARCHAR(30),
    u_surname VARCHAR(30),
    u_age INTEGER,
    u_gender VARCHAR(10),
    chain_ID INTEGER,
    userName VARCHAR(20) UNIQUE,
    userPassword VARCHAR(30)
);

DROP TABLE IF EXISTS chainTable;

CREATE TABLE chainTable (
    chain_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    chainName VARCHAR(30),
    gymNum INTEGER UNIQUE,
    numberOfMembers INTEGER
);

DROP TABLE IF EXISTS gymTable;

CREATE TABLE gymTable (
    gymID INTEGER PRIMARY KEY,
    gymName VARCHAR(30),
    numberOfUser INTEGER,
    openingTime VARCHAR(20),
    closingTime VARCHAR(20),
    chain_ID INTEGER,

    FOREIGN KEY (chain_ID) REFERENCES chainTable(chain_ID)
);

DROP TABLE IF EXISTS userTable;

CREATE TABLE userTable (
    userID INTEGER PRIMARY KEY AUTOINCREMENT,
    u_name VARCHAR(30),
    u_surname VARCHAR(30),
    u_age INTEGER,
    u_gender VARCHAR(10),
    chain_ID INTEGER,
    userName VARCHAR(20) UNIQUE,
    userPassword VARCHAR(30),

    FOREIGN KEY(chain_ID) REFERENCES chainTable(chain_ID)
);

DROP TABLE IF EXISTS managerTable;

CREATE TABLE managerTable (
    managerID INTEGER PRIMARY KEY AUTOINCREMENT,
    managerUsername VARCHAR(30),
    managerPassword VARCHAR(30),
    gymID INTEGER,

    FOREIGN KEY (gymID) REFERENCES gymTable(gymID)
);

DROP TABLE IF EXISTS activeManagerTable;

CREATE TABLE activeManagerTable (
    managerID INTEGER PRIMARY KEY AUTOINCREMENT,
    managerUsername VARCHAR(30),
    managerPassword VARCHAR(30),
    gymID INTEGER
);

DROP TABLE IF EXISTS personalTrainerTable;

CREATE TABLE personalTrainerTable (
    ptID INTEGER PRIMARY KEY AUTOINCREMENT,
    ptName VARCHAR(30),
    ptSurname VARCHAR(30),
    ptAge INTEGER,
    ptGender VARCHAR(10),
    gymID INTEGER,
    ptProfession VARCHAR(30),

    FOREIGN KEY (gymID) REFERENCES gymTable(gymID)
);


DROP TABLE IF EXISTS facilityTable;

CREATE TABLE facilityTable (
    facilityID INTEGER PRIMARY KEY AUTOINCREMENT,
    facilityType VARCHAR(30),
    gymID INTEGER NOT NULL,

    FOREIGN KEY (gymID) REFERENCES gymTable(gymID)
);

DROP TABLE IF EXISTS ptScheduleTable;

CREATE TABLE ptScheduleTable (
    ptID INTEGER,
    scheduleDay VARCHAR(7),
    scheduleTime VARCHAR(10),
    PRIMARY KEY(ptID, scheduleDay, scheduleTime),
    
    FOREIGN KEY (ptID) REFERENCES personalTrainerTable(ptID)
);

DROP TABLE IF EXISTS facilityScheduleTable;

CREATE TABLE facilityScheduleTable (
    facilityID INTEGER,
    scheduleDay VARCHAR(7),
    scheduleTime VARCHAR(10),
    PRIMARY KEY(facilityID, scheduleDay, scheduleTime),
    FOREIGN KEY (facilityID) REFERENCES facilityTable(facilityID)
);

DROP TABLE IF EXISTS userScheduleTable;

CREATE TABLE userScheduleTable (
    userID INTEGER,
    boolPt BOOLEAN,
    scheduleDay VARCHAR(7),
    scheduleTime VARCHAR(10),
   
    PRIMARY KEY(userID, scheduleDay, scheduleTime),
    FOREIGN KEY (userID) REFERENCES userTable(userID)
);