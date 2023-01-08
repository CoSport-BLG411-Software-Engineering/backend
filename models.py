import sqlite3
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


engine = create_engine('mysql+pymysql://sql7587680:SlJGpZGk54@sql7.freesqldatabase.com:3306/sql7587680', echo=True)
Base = declarative_base(engine)

class User(Base):
    """"""
    __tablename__ = 'userTable'
    
    u_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    chain_id = Column(Integer, ForeignKey("chainTable.chain_ID"))
    username = Column(String)
    password = Column(String)
    
    #----------------------------------------------------------------------
    def __init__(self, u_id, name, surname, age, gender, chain_id, username, password):
        """"""
        self.u_id = u_id
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.chain_id = chain_id
        self.username = username
        self.password = password
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<User -="" '%s':="" '%s'="">" % (self.u_id, self.name,
                                                 self.surname)

class Chain(Base):
    """"""
    __tablename__ = 'chainTable'
    
    c_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    gymnum = Column(Integer)
    numofmembers = Column(Integer)

    #----------------------------------------------------------------------
    def __init__(self, c_id, name, gymnum, numofmembers):
        """"""
        self.c_id = c_id
        self.name = name
        self.gymnum = gymnum
        self.numofmembers = numofmembers
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<User -="" '%s':="" '%s'="">" % (self.c_id, self.name,
                                                 self.name)

class Gym(Base):
    """"""
    __tablename__ = 'gymTable'
    
    gym_id = Column(Integer, primary_key=True, autoincrement=True)
    numofusers = Column(Integer)
    name = Column(String)
    o_time = Column(String)
    c_time = Column(String)
    chain_id = Column(Integer, ForeignKey("chainTable.chain_ID"))
    
    #----------------------------------------------------------------------
    def __init__(self, gym_id, numofusers, name, o_time, c_time, chain_id):
        """"""
        self.gym_id = gym_id
        self.numofusers = numofusers
        self.name = name
        self.o_time = o_time
        self.c_time = c_time
        self.chain_id = chain_id
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<User -="" '%s':="" '%s'="">" % (self.gym_id, self.name,
                                                 self.o_time)

class Manager(Base):
    """"""
    __tablename__ = 'managerTable'
    
    m_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Integer)
    password = Column(String)
    gym_id = Column(Integer, ForeignKey("gymTable.gymID"))
    
    #----------------------------------------------------------------------
    def __init__(self, m_id, username, password, gym_id):
        """"""
        self.m_id = m_id
        self.username = username
        self.password = password
        self.gym_id = gym_id
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<User -="" '%s':="" '%s'="">" % (self.m_id, self.username,
                                                 self.password)

class PT(Base):
    """"""
    __tablename__ = 'personalTrainerTable'
    
    pt_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    surname = Column(String)
    age = Column(Integer)
    gender = Column(String)
    gym_id = Column(Integer, ForeignKey("gymTable.gymID"))
    profession = Column(String)
    
    #----------------------------------------------------------------------
    def __init__(self, pt_id, name, surname, age, gender, gym_id, profession):
        """"""
        self.pt_id = pt_id
        self.name = name
        self.surname = surname
        self.age = age
        self.gender = gender
        self.gym_id = gym_id
        self.profession = profession
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<User -="" '%s':="" '%s'="">" % (self.pt_id, self.name,
                                                 self.surname)

class Facility(Base):
    """"""
    __tablename__ = 'facilityTable'
    
    f_id = Column(Integer, primary_key=True, autoincrement=True)
    facilityType = Column(String)
    gym_id = Column(Integer, ForeignKey("gymTable.gymID"))
    
    #----------------------------------------------------------------------
    def __init__(self, f_id, facilityType, gym_id):
        """"""
        self.f_id = f_id
        self.facilityType = facilityType
        self.gym_id = gym_id
        
    #----------------------------------------------------------------------
    def __repr__(self):
        """"""
        return "<User -="" '%s':="" '%s'="">" % (self.f_id, self.name,
                                                 self.surname)

def loadSession():
    """"""
    metadata = Base.metadata
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def mysqlconnect():
    """"""
    metadata = Base.metadata
    conn = engine.connect()
    return conn
    

def retrieveUsers():
    users = engine.execute("SELECT * FROM userTable").fetchall()
    return users 

def addUser(u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword):
    engine.execute("INSERT INTO userTable (u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword) VALUES (%s, %s, %s, %s, %s, %s, %s)", (u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword))

def retrieveManagers():
    users = engine.execute("SELECT * FROM managerTable").fetchall()
    return users 

def addManager(managerUsername, managerPassword, gymID):
    engine.execute("INSERT INTO managerTable (managerUsername, managerPassword, gymID) VALUES (%s, %s, %s)", (managerUsername, managerPassword, gymID))

def getUserGyms(chain_ID):
    gyms = engine.execute("SELECT gymTable.gymID, gymTable.gymName FROM gymTable INNER JOIN chainTable ON gymTable.chain_ID = chainTable.chain_ID WHERE chainTable.chain_ID =%s", str(chain_ID)).fetchall()
    return gyms

def addActiveUser(user):

    values = engine.execute("SELECT * FROM userTable WHERE userName=%s", user).fetchone()

    for value in values:
        print(value)

    engine.execute("DELETE FROM activeUserTable")
    engine.execute("INSERT INTO activeUserTable VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (str(values[0]), values[1], values[2], str(values[3]), values[4], str(values[5]), values[6], values[7]))
    
def addActiveManager(manager):

    values = engine.execute("SELECT * FROM managerTable WHERE managerUsername= %s", manager).fetchone()
    for value in values:
        print(value)

    engine.execute("DELETE FROM activeManagerTable")
    engine.execute("INSERT INTO activeManagerTable VALUES (%s, %s, %s, %s)", (str(values[0]), values[1], values[2], str(values[3])))

def getActiveUser():
    activeUser = engine.execute("SELECT * FROM activeUserTable").fetchall()
    return activeUser

def getActiveManager():
    activeManager = engine.execute("SELECT * FROM activeManagerTable").fetchall()
    return activeManager

def getGym(gymID):
    selectedGym = engine.execute("SELECT * FROM gymTable WHERE gymID =%s", str(gymID)).fetchone()
    return selectedGym

def getPersonalTrainers(gymID):
    personalTrainers = engine.execute("SELECT * FROM personalTrainerTable WHERE gymID =%s", str(gymID)).fetchall()
    return personalTrainers

def getFacilities(gymID):
    facilities = engine.execute("SELECT * FROM facilityTable WHERE gymID =%s", str(gymID)).fetchall()
    return facilities

def checkSchedule(daySelection, timeSelection, ptSelection, facilityID, userID):
    userValue = engine.execute("SELECT * FROM userScheduleTable WHERE (userID =%s AND scheduleDay=%s AND scheduleTime=%s)",(str(userID), daySelection, timeSelection)).fetchall()

    if userValue:
        print("This interval is taken for user")
    else:
        facilityValue = engine.execute("SELECT * FROM facilityScheduleTable WHERE (facilityID =%s AND scheduleDay=%s AND scheduleTime=%s)",(str(facilityID), daySelection, timeSelection)).fetchall()
        if facilityValue:
            print('facility interval is taken for the user')
        else:
            print(ptSelection)
            ptValue = engine.execute("SELECT * FROM ptScheduleTable WHERE (ptID =%s AND scheduleDay=%s AND scheduleTime=%s)",(str(ptSelection), daySelection, timeSelection)).fetchall()
            if ptValue:
                print("Personal trainer interval is taken")
            else:
                print("you can take this interval ")
                return True
    return False

def addSchedule(daySelection, timeSelection, ptSelection, facilityID, userID):
    engine.execute("INSERT INTO userScheduleTable (userID, scheduleDay, scheduleTime) VALUES (%s, %s, %s)", (str(userID), daySelection, timeSelection)) 

    
    engine.execute("INSERT INTO  facilityScheduleTable VALUES (%s, %s, %s)", (str(facilityID), daySelection, timeSelection)) 

    engine.execute("INSERT INTO  ptScheduleTable VALUES (%s, %s, %s)", (str(ptSelection), daySelection, timeSelection))


def getUserSchedules(userID):
    schedules = engine.execute("SELECT * FROM userScheduleTable WHERE userID=%s", str(userID)).fetchall()
    return schedules


def getGymCurrentTrainer(managerGym):
    numberOfTrainers = engine.execute("SELECT * FROM managerTable WHERE gymID =%s", str(managerGym['gymID'])).fetchall()
    return len(numberOfTrainers)
  

def changeUserProfile(inputData):
    # input data name, surname, age, gender, userName, userPassword
    engine.execute("UPDATE userTable SET u_name=%s, u_surname=%s, u_age=%s, u_gender=%s, userName=%s, userPassword=%s WHERE userID=%s", (inputData[1],inputData[2],str(inputData[3]),inputData[4],inputData[5],inputData[6],str(inputData[0])))
    print(inputData[5])
    addActiveUser(inputData[5])
    
def changeManagerProfile(inputData):
    # input data name, surname, age, gender, userName, userPassword
    engine.execute("UPDATE managerTable SET managerUsername=%s, managerPassword=%s, gymID=%s WHERE managerID=%s", (inputData[1],inputData[2],str(inputData[3]), str(inputData[0])))
    addActiveManager(inputData[1])

"""class User():

    def __init__(self, userID, u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword, active = True):
        self.userID = userID
        self.u_name = u_name
        self.u_surname = u_surname
        self.u_age = u_age
        self.u_gender = u_gender
        self.chain_ID = chain_ID
        self.userName = userName
        self.userPassword = userPassword
        self.active = active
        self.authenticated = False

    def isAuthenticated(self):
        return self.authenticated
        #return true if user is authenticated, provided credentials

    def isActive():
        return True
        #return true if user is activte and authenticated

    def isAnnonymous(self):
        return False
        #return true if annon, actual user return false

    def getUserName(self):
        return self.userName
   """
    