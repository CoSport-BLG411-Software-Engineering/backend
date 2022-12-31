import sqlite3
from sqlalchemy import create_engine, ForeignKey, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

"""def loadSession():
    session = sqlite3.sessionect('database.db')
    session.row_factory = sqlite3.Row
    return session"""

engine = create_engine(r'sqlite:///database.db', echo=True)
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

    
    

def retrieveUsers():
    session = loadSession()
    users = session.execute("SELECT * FROM userTable").fetchall()
    session.close()

    return users 

def addUser(u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword):
    session = loadSession()
    session.execute('INSERT INTO userTable '
    ' (u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword) VALUES ('
        + '"' + u_name + '" , '
        + '"' + u_surname + '" , '
        + '' + str(u_age) + ', '
        + '"' + u_gender + '" , '
        + str(chain_ID) + ', '
        + '"' + userName + '" , '
        + '"' + userPassword + '") ')
    session.commit()
    session.close()

def retrieveManagers():
    session = loadSession()
    users = session.execute("SELECT * FROM managerTable").fetchall()
    session.close()

    return users 

def addManager(managerUsername, managerPassword, gymID):
    session = loadSession()
    print("adding manager ")
    session.execute('INSERT INTO managerTable '
    ' (managerUsername, managerPassword, gymID) VALUES ('
        + '"' + managerUsername + '" , '
        + '"' + managerPassword + '" ,' 
        + str(gymID) + ')')
    session.commit()
    session.close()

def getUserGyms(chain_ID):
    session = loadSession()
    gyms = session.execute(" SELECT gymTable.gymID, gymTable.gymName"
            " FROM gymTable" 
            " INNER JOIN chainTable"
            " ON gymTable.chain_ID = chainTable.chain_ID"
            " WHERE chainTable.chain_ID = " + str(chain_ID)).fetchall()

    session.commit()
    session.close()

    return gyms

def addActiveUser(user):
    session = loadSession()

    values = session.execute('SELECT * FROM userTable WHERE userName= "' + user + '"').fetchone()
    session.commit()

    for value in values:
        print(value)

    session.execute('DELETE FROM activeUserTable').fetchall()
    session.commit()

    session.execute('INSERT INTO activeUserTable VALUES ('
        + str(values[0]) + ', '
        + '"' + values[1] + '" , '
        + '"' + values[2] + '" , '
        + str(values[3]) + ', '
        + '"' + values[4] + '" , '
        + str(values[5]) + ', '
        + '"' + values[6] + '" , '
        + '"' + values[7]  + '")' )
        
    session.commit()
    session.close()

def addActiveManager(manager):
    session = loadSession()

    values = session.execute('SELECT * FROM managerTable WHERE managerUsername= "' + manager + '"').fetchone()
    session.commit()

    for value in values:
        print(value)

    session.execute('DELETE FROM activeManagerTable').fetchall()
    session.commit()

    session.execute('INSERT INTO activeManagerTable VALUES ('
        + str(values[0]) + ', '
        + '"' + values[1] + '" , '
        + '"' + values[2] + '" , '
        + str(values[3]) + ')')
        
    session.commit()
    session.close()

def getActiveUser():
    session = loadSession()
    activeUser = session.execute('SELECT * FROM activeUserTable').fetchall()
    session.commit()
    session.close()

    return activeUser

def getActiveManager():
    session = loadSession()
    activeManager = session.execute('SELECT * FROM activeManagerTable').fetchall()
    session.commit()
    session.close()

    return activeManager

def getGym(gymID):
    session = loadSession()
    selectedGym = session.execute('SELECT * FROM gymTable WHERE gymID =' + str(gymID)).fetchone()
    session.commit()
    session.close()

    return selectedGym

def getPersonalTrainers(gymID):
    session = loadSession()
    personalTrainers = session.execute('SELECT * FROM personalTrainerTable WHERE gymID = ' + str(gymID)).fetchall()
    session.commit()
    session.close()

    return personalTrainers

def getFacilities(gymID):
    session = loadSession()
    facilities = session.execute('SELECT * FROM facilityTable WHERE gymID = ' + str(gymID)).fetchall()
    session.commit()
    session.close()

    return facilities

def checkSchedule(daySelection, timeSelection, ptSelection, facilityID, userID):
    session = loadSession()
    userValue = session.execute('SELECT * FROM userScheduleTable WHERE (userID = ' + str(userID) 
    + ' AND scheduleDay= "' + daySelection + '" AND scheduleTime= "' + timeSelection + '")' ).fetchall()
    session.commit()

    if userValue:
        print("This interval is taken for user")
    else:
        facilityValue = session.execute('SELECT * FROM facilityScheduleTable WHERE (facilityID = ' + str(facilityID)
        + ' AND scheduleDay= "' + daySelection + '" AND scheduleTime= "' + timeSelection + '")' ).fetchall()
        session.commit()
        
        if facilityValue:
            print('facility interval is taken for the user')
        else:
            print(ptSelection)
            ptValue = session.execute('SELECT * FROM ptScheduleTable WHERE (ptID = ' + str(ptSelection)
            + ' AND scheduleDay= "' + daySelection + '" AND scheduleTime= "' + timeSelection + '")' ).fetchall()
            session.commit()

            if ptValue:
                print("Personal trainer interval is taken")
            else:
                print("you can take this interval ")
                return True
    
    session.close()
    return False

def addSchedule(daySelection, timeSelection, ptSelection, facilityID, userID):
    session = loadSession()
    session.execute('INSERT INTO userScheduleTable (userID, scheduleDay, scheduleTime) VALUES (' 
    + str(userID) + ', "' + daySelection
    + '", "' + timeSelection + '" )') 
    session.commit()

    
    session.execute('INSERT INTO  facilityScheduleTable VALUES (' + str(facilityID) + ', "' + daySelection
    + '", "' + timeSelection + '")') 
    session.commit()

    
    session.execute('INSERT INTO  ptScheduleTable VALUES (' + str(ptSelection) + ', "' + daySelection
    + '", "' + timeSelection + '")') 
    session.commit()

    session.close()

def getUserSchedules(userID):

    session = loadSession()
    schedules = session.execute('SELECT * FROM userScheduleTable WHERE userID= ' + str(userID)).fetchall()
    session.commit()
    session.close()

    return schedules

#def getGymCurrentUser(managerGym):
    #session=loadSession()
    


def getGymCurrentTrainer(managerGym):
    session = loadSession()
    numberOfTrainers = session.execute('SELECT * FROM managerTable WHERE gymID = ' + str(managerGym['gymID'])).fetchall()
    session.commit()
    session.close()

    return len(numberOfTrainers)
  
def changeUserProfile(inputData):
    # input data name, surname, age, gender, userName, userPassword
    session = loadSession()
    session.execute('UPDATE userTable SET u_name="' + inputData[1]
    + '", u_surname="' + inputData[2]
    + '", u_age=' + str(inputData[3])
    + ', u_gender="' + inputData[4] 
    + '", userName="' + inputData[5] 
    + '", userPassword="' + inputData[6]
    + '" WHERE userID=' + str(inputData[0]) )

    session.commit()
    session.close()

    print(inputData[5])
    addActiveUser(inputData[5])
    
def changeManagerProfile(inputData):
    # input data name, surname, age, gender, userName, userPassword
    session = loadSession()
    session.execute('UPDATE managerTable SET managerUsername="' + inputData[1]
    + '", managerPassword="' + inputData[2]
    + '", gymID=' + str(inputData[3])
    + ' WHERE managerID=' + str(inputData[0]) )

    session.commit()
    session.close()

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
    