import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def retrieveUsers():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM userTable").fetchall()
    conn.close()

    return users 

def addUser(u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword):
    conn = get_db_connection()
    conn.execute('INSERT INTO userTable '
    ' (u_name, u_surname, u_age, u_gender, chain_ID, userName, userPassword) VALUES ('
        + '"' + u_name + '" , '
        + '"' + u_surname + '" , '
        + '' + str(u_age) + ', '
        + '"' + u_gender + '" , '
        + str(chain_ID) + ', '
        + '"' + userName + '" , '
        + '"' + userPassword + '") ')
    conn.commit()
    conn.close()

def retrieveManagers():
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM managerTable").fetchall()
    conn.close()

    return users 

def addManager(managerUsername, managerPassword, gymID):
    conn = get_db_connection()
    print("adding manager ")
    conn.execute('INSERT INTO managerTable '
    ' (managerUsername, managerPassword, gymID) VALUES ('
        + '"' + managerUsername + '" , '
        + '"' + managerPassword + '" ,' 
        + str(gymID) + ')')
    conn.commit()
    conn.close()

def getUserGyms(chain_ID):
    conn = get_db_connection()
    gyms = conn.execute(" SELECT gymTable.gymID, gymTable.gymName"
            " FROM gymTable" 
            " INNER JOIN chainTable"
            " ON gymTable.chain_ID = chainTable.chain_ID"
            " WHERE chainTable.chain_ID = " + str(chain_ID)).fetchall()

    conn.commit()
    conn.close()

    return gyms

def addActiveUser(user):
    conn = get_db_connection()

    values = conn.execute('SELECT * FROM userTable WHERE userName= "' + user + '"').fetchone()
    conn.commit()

    for value in values:
        print(value)

    conn.execute('DELETE FROM activeUserTable').fetchall()
    conn.commit()

    conn.execute('INSERT INTO activeUserTable VALUES ('
        + str(values[0]) + ', '
        + '"' + values[1] + '" , '
        + '"' + values[2] + '" , '
        + str(values[3]) + ', '
        + '"' + values[4] + '" , '
        + str(values[5]) + ', '
        + '"' + values[6] + '" , '
        + '"' + values[7]  + '")' )
        
    conn.commit()
    conn.close()

def addActiveManager(manager):
    conn = get_db_connection()

    values = conn.execute('SELECT * FROM managerTable WHERE managerUsername= "' + manager + '"').fetchone()
    conn.commit()

    for value in values:
        print(value)

    conn.execute('DELETE FROM activeManagerTable').fetchall()
    conn.commit()

    conn.execute('INSERT INTO activeManagerTable VALUES ('
        + str(values[0]) + ', '
        + '"' + values[1] + '" , '
        + '"' + values[2] + '" , '
        + str(values[3]) + ')')
        
    conn.commit()
    conn.close()

def getActiveUser():
    conn = get_db_connection()
    activeUser = conn.execute('SELECT * FROM activeUserTable').fetchall()
    conn.commit()
    conn.close()

    return activeUser

def getActiveManager():
    conn = get_db_connection()
    activeManager = conn.execute('SELECT * FROM activeManagerTable').fetchall()
    conn.commit()
    conn.close()

    return activeManager

def getGym(gymID):
    conn = get_db_connection()
    selectedGym = conn.execute('SELECT * FROM gymTable WHERE gymID =' + str(gymID)).fetchone()
    conn.commit()
    conn.close()

    return selectedGym

def getPersonalTrainers(gymID):
    conn = get_db_connection()
    personalTrainers = conn.execute('SELECT * FROM personalTrainerTable WHERE gymID = ' + str(gymID)).fetchall()
    conn.commit()
    conn.close()

    return personalTrainers

def getFacilities(gymID):
    conn = get_db_connection()
    facilities = conn.execute('SELECT * FROM facilityTable WHERE gymID = ' + str(gymID)).fetchall()
    conn.commit()
    conn.close()

    return facilities

def checkSchedule(daySelection, timeSelection, ptSelection, facilityID, userID):
    conn = get_db_connection()
    userValue = conn.execute('SELECT * FROM userScheduleTable WHERE (userID = ' + str(userID) 
    + ' AND scheduleDay= "' + daySelection + '" AND scheduleTime= "' + timeSelection + '")' ).fetchall()
    conn.commit()

    if userValue:
        print("This interval is taken for user")
    else:
        facilityValue = conn.execute('SELECT * FROM facilityScheduleTable WHERE (facilityID = ' + str(facilityID)
        + ' AND scheduleDay= "' + daySelection + '" AND scheduleTime= "' + timeSelection + '")' ).fetchall()
        conn.commit()
        
        if facilityValue:
            print('facility interval is taken for the user')
        else:
            print(ptSelection)
            ptValue = conn.execute('SELECT * FROM ptScheduleTable WHERE (ptID = ' + str(ptSelection)
            + ' AND scheduleDay= "' + daySelection + '" AND scheduleTime= "' + timeSelection + '")' ).fetchall()
            conn.commit()

            if ptValue:
                print("Personal trainer interval is taken")
            else:
                print("you can take this interval ")
                return True
    
    conn.close()
    return False

def addSchedule(daySelection, timeSelection, ptSelection, facilityID, userID):
    conn = get_db_connection()
    conn.execute('INSERT INTO userScheduleTable (userID, scheduleDay, scheduleTime) VALUES (' 
    + str(userID) + ', "' + daySelection
    + '", "' + timeSelection + '" )') 
    conn.commit()

    
    conn.execute('INSERT INTO  facilityScheduleTable VALUES (' + str(facilityID) + ', "' + daySelection
    + '", "' + timeSelection + '")') 
    conn.commit()

    
    conn.execute('INSERT INTO  ptScheduleTable VALUES (' + str(ptSelection) + ', "' + daySelection
    + '", "' + timeSelection + '")') 
    conn.commit()

    conn.close()

def getUserSchedules(userID):

    conn = get_db_connection()
    schedules = conn.execute('SELECT * FROM userScheduleTable WHERE userID= ' + str(userID)).fetchall()
    conn.commit()
    conn.close()

    return schedules

#def getGymCurrentUser(managerGym):
    #conn=get_db_connection()
    


def getGymCurrentTrainer(managerGym):
    conn = get_db_connection()
    numberOfTrainers = conn.execute('SELECT * FROM managerTable WHERE gymID = ' + str(managerGym['gymID'])).fetchall()
    conn.commit()
    conn.close()

    return len(numberOfTrainers)
  
def changeUserProfile(inputData):
    # input data name, surname, age, gender, userName, userPassword
    conn = get_db_connection()
    conn.execute('UPDATE userTable SET u_name="' + inputData[1]
    + '", u_surname="' + inputData[2]
    + '", u_age=' + str(inputData[3])
    + ', u_gender="' + inputData[4] 
    + '", userName="' + inputData[5] 
    + '", userPassword="' + inputData[6]
    + '" WHERE userID=' + str(inputData[0]) )

    conn.commit()
    conn.close()

    print(inputData[5])
    addActiveUser(inputData[5])
    
def changeManagerProfile(inputData):
    # input data name, surname, age, gender, userName, userPassword
    conn = get_db_connection()
    conn.execute('UPDATE managerTable SET managerUsername="' + inputData[1]
    + '", managerPassword="' + inputData[2]
    + '", gymID=' + str(inputData[3])
    + ' WHERE managerID=' + str(inputData[0]) )

    conn.commit()
    conn.close()

    addActiveManager(inputData[1])

class User():

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
   
    