#import sqlite3
from flask import Flask, render_template, redirect, url_for, request
import models as dbHandler



app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug = True)

@app.route('/')
def homePage():
    session = dbHandler.loadSession()
    session.close()

    return redirect(url_for('userLogin'))


@app.route('/')
def render_page_web():
    print("select customer or manager ")
    return redirect(url_for('userLogin'))


@app.route('/web/userLogin', methods=['GET', 'POST'])
def userLogin():
    error = None
    if request.method == 'POST':
        userName = request.form['userName']
        userPassword = request.form['userPassword']

        users = dbHandler.retrieveUsers()

        for user in users:
            if user['userName'] == userName and user['userPassword'] == userPassword:
                
                activeUser = user['userName']

                dbHandler.addActiveUser(activeUser)

                return redirect(url_for('userMainScreen'))


        print("you couldn't logged in username or password is wrong!")
            
    return render_template('login.html', error=error)

@app.route('/web/userSignup', methods=['GET', 'POST'])
def userSignup():
    if request.method == 'POST' and 'userName' in request.form and 'userPassword' in request.form:
        userName = request.form['userName']
        userPassword = request.form['userPassword']
        chain_ID = request.form['chain_ID']

        users = dbHandler.retrieveUsers()

        session = dbHandler.loadSession()
        account = session.execute('SELECT * FROM userTable WHERE userName = "' + userName + '"' ).fetchone()
        session.commit()
        session.close()

        if account:
                print("Account already exists !")
        else:
            dbHandler.addUser("none", "none", 0, "none", chain_ID, userName, userPassword) # adding user
            print("User has added")

        return redirect(url_for('userLogin'))

    return render_template('userSignup.html')

@app.route('/web/managerLogin', methods=['GET', 'POST'])
def managerLogin():
    error = None
    if request.method == 'POST':
        managerUsername = request.form['managerUsername']
        managerPassword = request.form['managerPassword']

        managers = dbHandler.retrieveManagers()

        for manager in managers:
            if manager['managerUsername'] == managerUsername and manager['managerPassword'] == managerPassword:
                
                activeManager = manager['managerUsername']

                dbHandler.addActiveManager(activeManager)

                return redirect(url_for('managerMainScreen'))


        print("you couldn't logged in username or password is wrong!")
            
    return render_template('managerLogin.html', error=error)

@app.route('/web/managerSignup', methods=['GET', 'POST'])
def managerSignup():#updated
    if request.method == 'POST' and 'managerUsername' in request.form and 'managerPassword' in request.form:
        managerUsername = request.form['managerUsername']
        managerPassword = request.form['managerPassword']
        gym_ID = request.form['gym_ID']

        managers = dbHandler.retrieveManagers()

        session = dbHandler.loadSession()
        account = session.execute('SELECT * FROM managerTable WHERE managerUsername = "' + managerUsername + '"' ).fetchone()
        session.commit()
        session.close()
        
        print("lets add manager")

        if account:
                print("Account already exists !")
        else:
            dbHandler.addManager(managerUsername, managerPassword, gym_ID) # adding manager
            print("Manager has added")

        return redirect(url_for('managerLogin'))

    return render_template('managerSignup.html')

@app.route('/web/userMainScreen', methods=['GET', 'POST'])
def userMainScreen():

    if request.method == 'POST':
        inputData = list(request.form.values())
        gymName = inputData[0]
        return redirect(url_for('userSelectGymPage', gymName=gymName))
        
    activeUsers = dbHandler.getActiveUser()

    for user in activeUsers:
        activeUser = user
    
    userGyms = dbHandler.getUserGyms(activeUser['chain_ID'])
    
    return render_template('userMainScreen.html', userGyms=userGyms)

@app.route('/web/managerMainScreen', methods=['GET', 'POST'])
def managerMainScreen():

    activeManagers = dbHandler.getActiveManager()

    for manager in activeManagers:
        activeManager = manager
    
    managerGym = dbHandler.getGym(activeManager['gymID'])
    
    #currentUser = dbHandler.getGymCurrentUser(managerGym)
    currentTrainer = dbHandler.getGymCurrentTrainer(managerGym)
    
    return render_template('managerMainScreen.html', currentTrainer=currentTrainer)

@app.route('/web/userSelectGymPage', methods=['GET', 'POST'])
def userSelectGymPage():
    gymID = request.args['gymName']
    
    selectedGym = dbHandler.getGym(gymID)
    activeUsers = dbHandler.getActiveUser()

    for user in activeUsers:
        activeUser = user
    
    if request.method=='POST':
        inputData = list(request.form.values())

        checkSchedule = dbHandler.checkSchedule(inputData[0], inputData[1], inputData[2], inputData[3]
        , activeUser['userID'])

        if checkSchedule:
            dbHandler.addSchedule(inputData[0], inputData[1], inputData[2], inputData[3]
            , activeUser['userID'])
            
            return redirect(url_for('userSchedules'))
        else:
            return redirect(url_for('userMainScreen'))
        

    facilities = dbHandler.getFacilities(selectedGym['gymID'])
    personalTrainers = dbHandler.getPersonalTrainers(selectedGym['gymID'])

    return render_template('userSelectGymPage.html', personalTrainers=personalTrainers, facilities=facilities)

@app.route('/web/userProfile', methods=['GET', 'POST'])
def userProfile():

    activeUsers = dbHandler.getActiveUser() #getting active user

    for user in activeUsers:
        activeUser = user

    if request.method == 'POST':
        inputData = request.form.getlist('activeUserFeatures')

        dbHandler.changeUserProfile(inputData)

        return redirect(url_for('userProfile'))

    return render_template('userProfilePage.html', activeUser=activeUser)        

@app.route('/web/managerProfile', methods=['GET', 'POST'])
def managerProfile():

    activeManagers = dbHandler.getActiveManager() #getting active user

    for manager in activeManagers:
        activeManager = manager

    if request.method == 'POST':
        inputData = request.form.getlist('activeManagerFeatures')

        dbHandler.changeManagerProfile(inputData)

        return redirect(url_for('managerProfile'))

    return render_template('managerProfilePage.html', activeManager=activeManager)        


@app.route('/web/userSchedules', methods=['GET', 'POST'])
def userSchedules():
    
    activeUsers = dbHandler.getActiveUser()

    for user in activeUsers:
        activeUser = user
    
    schedules = dbHandler.getUserSchedules(activeUser['userID'])

    if request.method == 'POST':
        inputData = request.form.getlist('scheduleDeletion')
        print(inputData)

        for input in inputData:
            dbHandler.deleteSchedule(activeUser['userID'], int(input) - 1, )
            

        return redirect(url_for('userSchedules'))


    return render_template('userSchedules.html', schedules=schedules)
