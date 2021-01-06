import mysql.connector
import json


# DB Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="battles"
)

sql = db.cursor()


# Query functions
def getActive(active):
    sql.execute("""SELECT {},count({}) AS most_active_count 
                    FROM battles_data
                    GROUP BY {}
                    ORDER BY  COUNT(most_active_count) DESC
                    LIMIT 1;""".format(active, active, active))
    return sql.fetchall()[0][0]


def getOutcome(outcome, where):
    sql.execute("""SELECT {},count({}) AS most_active_count 
                    FROM battles_data
                    WHERE {} = '{}'
                    GROUP BY {};""".format(outcome, outcome, outcome, where, outcome))
    return sql.fetchall()[0][1]


def getBattleTypest():
    sql.execute(
        "SELECT DISTINCT battle_type FROM battles_data WHERE battle_type IS NOT NULL")
    results = sql.fetchall()
    battleTypes = [data[0] for data in results]
    return battleTypes


def getDefenderSize(operation):
    sql.execute("SELECT {}(defender_size) FROM battles_data".format(operation))
    results = sql.fetchall()
    return results[0][0]


#  For APIs

def authUser(username, password):
    sql.execute("SELECT *  FROM users")
    results = sql.fetchall()
    data = [results[0][0], results[0][1]]
    if data[0] == username and data[1] == password:
        return True
    return False


def getList():
    sql.execute("SELECT DISTINCT region FROM battles_data")
    results = sql.fetchall()
    data = [data[0] for data in results]
    return data


def getCount():
    sql.execute("SELECT count(name) FROM battles_data")
    results = sql.fetchall()
    return results[0][0]


def getStats():
    stats = {
        'most_active': {
            'attacker_king': getActive("attacker_king"),
            'defender_king': getActive("defender_king"),
            'region': getActive("region"),
            'name': getActive("name")
        },
        'attacker_outcome': {
            'win': getOutcome("attacker_outcome", "win"),
            'loss': getOutcome("attacker_outcome", "loss")
        },
        'battle_type': getBattleTypest(),
        'defender_size': {
            'average': str(getDefenderSize("AVG")),
            'min': getDefenderSize("MIN"),
            'max': getDefenderSize("MAX")}
    }
    return json.dumps(stats)


def getBattlesByName(name):
    sql.execute(
        "SELECT name FROM battLes_data WHERE (attacker_king = '{}' OR defender_king = '{}')".format(name, name))
    results = sql.fetchall()
    data = [data[0] for data in results]
    return json.dumps(data)


def getBattlesByNameLocation(name, location):
    sql.execute(
        "SELECT name FROM battLes_data WHERE (attacker_king = '{}' OR defender_king = '{}') AND location = '{}'".format(name, name, location))
    results = sql.fetchall()
    data = [data[0] for data in results]
    return json.dumps(data)


def getBattlesByNameType(name, type):
    sql.execute(
        "SELECT name FROM battLes_data WHERE (attacker_king = '{}' OR defender_king = '{}') AND battle_type = '{}'".format(name, name, type))
    results = sql.fetchall()
    data = [data[0] for data in results]
    return json.dumps(data)


def getBattlesByNameLocationType(name, location, type):
    sql.execute(
        "SELECT name FROM battLes_data WHERE (attacker_king = '{}' OR defender_king = '{}') AND location = '{}' AND battle_type = '{}'".format(name, name, location, type))
    results = sql.fetchall()
    data = [data[0] for data in results]
    return json.dumps(data)


def createBattle(battleName):
    sql.execute(
        "SELECT name FROM battLes_data WHERE name = '{}'".format(battleName))
    results = sql.fetchall()
    if len(results) == 0:
        sql.execute(
            "INSERT INTO battLes_data (name) VALUES ('{}')".format(battleName))
        db.commit()
        sql.execute(
            "SELECT name FROM battLes_data WHERE name ='{}'".format(battleName))
        results = sql.fetchall()
        data = [results[0][0]]
        if data[0] == battleName:
            return "{} inserted Successfully".format(battleName)
        else:
            return "Please try again"
    elif results[0][0] == battleName:
        return "Battle Already Exist"


def readBattle(battleName):
    sql.execute(
        "SELECT name FROM battLes_data WHERE name = '{}'".format(battleName))
    results = sql.fetchall()
    if len(results) == 0:
        return "{} not found".format(battleName)
    return results[0][0]


def updateBattle(battleName, newBattleName):
    sql.execute(
        "UPDATE battles_data SET name = '{}' WHERE name = '{}'".format(newBattleName, battleName))
    db.commit()
    sql.execute(
        "SELECT name FROM battLes_data WHERE name = '{}'".format(newBattleName))
    results = sql.fetchall()
    if len(results) == 0:
        return "Please try again"
    return "Update Sucessful"


def deleteBattle(battleName):
    sql.execute(
        "SELECT name FROM battLes_data WHERE name = '{}'".format(battleName))
    results = sql.fetchall()
    if len(results) == 0:
        return "{} not found".format(battleName)
    else:
        sql.execute(
            "DELETE FROM battles_data WHERE name = '{}'".format(battleName))
        db.commit()
        sql.execute(
            "SELECT name FROM battLes_data WHERE name = '{}'".format(battleName))
        results = sql.fetchall()
        if len(results) == 0:
            return "Delete Successful"
        return "Please try again"



