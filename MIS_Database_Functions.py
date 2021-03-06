__author__ = 'John'
import sqlite3
import datetime
import os
import Info_IaState_Scraper
import Logger

# Set this to true when doing testing to avoid altering permanent data.
DEBUG = False


def get_connection():
    if not DEBUG:
        return sqlite3.connect('SOMMS_DB.sqlite')
    else:
        return sqlite3.connect('Test.sqlite')


def get_copy_connection():
    return sqlite3.connect('MIS_CheckIn_copy.sqlite')

###########################################
#        Event Based Functions            #
###########################################


def create_event(company, topic, date):
    """
    Creates an event with the given company, topic, and date. All input values
    should be strings of characters. An eventID is generated by selecting the maximum
    id from the database and adding one to it.

    :param company: The company name e.g. WalMart
    :param topic: The topic for the event. If none is known pass 'unknown'
    :param date: The date for the event. Pass in the format 'DD/MMM/YYYY'.
                SQLite does not have a dedicated date format so this is very important.
    :return: A list with two entries, the first of which indicates whether or not the transaction worked, the second
            of which is either the event ID of the event created or the error that was encountered.

            example:
            create_event("Cargil", "Being terrible at everything", "12/APR/2015")
            returns => [True, <event_id>]

            create_event("Fake", "Fake", "12/12/2015")
            returns => [False, "Please enter in the correct format..."]
    """
    result_set = []

    if len(date) != 11:
        result_set.append(False)
        result_set.append("Please enter the date in this format:\nDD/MMM/YYYY, aka 01/APR/2015")
        return result_set

    if not company.strip():
        result_set.append(False)
        result_set.append("Please enter a company name")
        return result_set

    if not topic.strip():
        result_set.append(False)
        result_set.append("Please enter a topic title, N/A if none")
        return result_set

    connection = get_connection()
    cursor = connection.cursor()
    data = cursor.execute('SELECT MAX(eventID) FROM Event')
    event_id = data.fetchone()[0]
    other_data = cursor.execute('SELECT semester_tag FROM Semester WHERE semester_num'
                                ' = (SELECT MAX(semester_num) FROM Semester)')
    semester_tag = other_data.fetchone()[0]
    if event_id is None:
        event_id = 0
    else:
        event_id += 1
    sql_string = "INSERT INTO Event VALUES(%s, '%s', '%s', '%s', '%s')" % (event_id, semester_tag, company, topic, date)
    try:
        cursor.execute(sql_string)
    except sqlite3.IntegrityError as e:
        result_set.append(False)
        result_set.append(str(e))
        return result_set
    except Exception as e:
        result_set.append(False)
        result_set.append(str(e))
        return result_set
    connection.commit()
    result_set.append(True)
    result_set.append(event_id)
    return result_set


def delete_event(event_id):
    """
    Deletes an event based on a given eventID
    :param event_id: The event id of the event to be deleted
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Event WHERE eventID ="+str(event_id)
    Logger.write_to_log("Logs\EventCreation", sql_string+"\n")
    try:
        cursor.execute(sql_string)
    except sqlite3.IntegrityError as e:
        Logger.write_to_log("Logs\EventCreation", str(e))
    except Exception as e:
        Logger.write_to_log("Logs\EventCreation", str(e))
    connection.commit()


def get_most_recent_event_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(eventID) FROM Event")
    try:
        return cursor.fetchone()[0]
    except TypeError:
        return None


def get_event_data(eventid):
    conn = get_connection()
    cursor = conn.cursor()
    sql_string = "SELECT * FROM Event WHERE eventID = %d" % eventid
    cursor.execute(sql_string)
    try:
        data = cursor.fetchone()
        pretty_data = {'eventID': data[0], 'semester': data[1], 'company': data[2], 'topic': data[3], 'date': data[4]}
        return pretty_data
    except TypeError:
        return None

###########################################
#        Member Based Functions           #
###########################################


def create_member(net_id, name, major, classification, dues_paid):
    """
    Creates a member instance in the Member table.

    :param net_id: The new member's net id
    :return: void
    """
    #if ' ' in net_id or '@' in net_id:
    #    raise Exception('Only enter the first portion of the net id => jmrolf@iastate.edu - jmrolf')
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql_string = "INSERT INTO Member VALUES ('%s', '%s', '%s', '%s', '%s', %s)" % \
            (net_id, net_id+"@iastate.edu", major, classification, name, str(dues_paid))
        cursor.execute(sql_string)
    except sqlite3.IntegrityError:
        pass
    except sqlite3.DatabaseError:
        pass
    except IOError:
        pass
    finally:
        conn.commit()


def set_major(net_id, major):
    """
    Sets the major attribute for the given net id in the member table.

    :param net_id: The net id of the user whose major is to be set
    :param major: The string value to be set
    :return: None
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET major='"+major+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_email(net_id, email):
    """
    Sets the email field in the Member table for the given net id.

    :param net_id: The net id of the user whose email is being set
    :param email: The string value that the email is to be set to
    :return: None
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET email='"+email+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_name(net_id, name):
    """
    Sets the name field in the Member table for hte given net id.

    :param net_id: The net id of hte user whose email is being set
    :param name: The string value representing the users name
    :return: None
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET name='"+name+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def set_classification(net_id, classification):
    """
    Sets the classification for the given net id to the passed classification string
    :param net_id: The net id of the user whose classification is to be set
    :param classification: The string literal of hte classification
    :return: None
    """
    if classification not in ('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate'):
        raise AttributeError("Classification must be in ('Freshman', 'Sophomore', 'Junior', 'Senior', 'Graduate')")
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "UPDATE Member SET classification='"+classification+"' WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def delete_member(net_id):
    """
    Deletes the member with the given net_id

    :param net_id: The net id of the member to be deleted
    :return: None
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Member WHERE netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()


def check_member(net_id):
    """
    Gets database data about a particular net_id and returns it in a dictionary format
    :param net_id: The net id whose data is to be selected
    :return: A dictionary containing all the data about the net_id parameter
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "SELECT * FROM Member WHERE netID ='"+str(net_id)+"'"
    cursor.execute(sql_string)
    member = cursor.fetchone()
    if not member is None:
        pretty_data = {}
        pretty_data['netid'] = member[0]
        pretty_data['email'] = member[1]
        pretty_data['major'] = member[2]
        pretty_data['classification'] = member[3]
        pretty_data['name'] = member[4]
        pretty_data['dues_paid'] = member[5]
        return pretty_data
    else:
        return None


def update_payment(net_id, semesters_paid_for):
    """
    Updates a member with net id <<net_id>>'s payment status from its previous value to <<semesters_paid_for>>
    :param net_id: The net id of the member whose status you want to update
    :param semesters_paid_for: the number of semesters the user has paid for
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Member SET dues_paid = %d WHERE netID = '%s'" % (semesters_paid_for, net_id))
    conn.commit()


def get_attendance_data(net_id, semester_tag):
    """
    Gets attendance data for the member whose net id is <<net_id>> for the semester that has the semester tag
    <<semester_tag>>. This can be used to check if the member has used his/her trial meeting, how many meetings a
    member has attended, and whether or not the member has paid dues.
    :param net_id: The net id of the member to gather attendance data on
    :param semester_tag: The semester tag of the semester from which to gather attendance data
    :return: A dictionary consisting of the number of meetings attended, the member's net id,
        and the member's dues status. If the member has not attended any meetings in the given semester,
        returns None.
    """
    conn = get_connection()
    cursor = conn.cursor()
    select_string = "SELECT COUNT(*), Ticket.NetID, Member.dues_paid FROM Event " \
                    "JOIN Ticket ON Event.eventID = Ticket.eventID " \
                    "JOIN Member ON Ticket.netID = Member.netID " \
                    "WHERE Ticket.netID = '%s' AND Event.Semester = '%s' " \
                    "GROUP BY Ticket.NetID " \
                    % (net_id, semester_tag)
    cursor.execute(select_string)
    ugly_data = cursor.fetchone()
    if ugly_data is not None:
        pretty_data = {'meetings_attended': ugly_data[0], 'member': ugly_data[1], 'dues': ugly_data[2]}
        return pretty_data
    else:
        return None

###########################################
#        Ticket Based Functions           #
###########################################


def create_ticket(event_id, net_id):
    """
    Creates a ticket with the given event_id and net_id

    :param event_id: The event id for the new ticket
    :param net_id: The net_id for the new ticket
    :return: void
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "INSERT INTO Ticket VALUES("+str(event_id)+", '"+net_id+"')"
    try:
        cursor.execute(sql_string)
        Logger.write_to_log(Logger.get_event_log_file(), sql_string+"\n")
    except sqlite3.IntegrityError:  # Maybe change these passes to log write. Not sure how to handle them.
        pass
    except sqlite3.DatabaseError:
        pass
    finally:
        connection.commit()


def delete_ticket(event_id, net_id):
    """
    Deletes the ticket with the given event_id and net_id

    :param event_id:
    :param net_id:
    :return:
    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "DELETE FROM Ticket WHERE eventID="+str(event_id)+" AND netID='"+net_id+"'"
    cursor.execute(sql_string)
    connection.commit()

###########################################
#          SEMESTER FUNCTIONS             #
###########################################


def run_end_of_semester():
    """
    This function updates the database to ensure that the members semesters paid is
    decremented by one. Run this function once per semester at the END of the semester.

    Running this prematurely may result in members appearing to be unpaid when they are
    in fact paid.

    If a members semester paid (dues_paid) value ever falls below 0 they will be deleted from
    the database.
    :return: None

    """
    connection = get_connection()
    cursor = connection.cursor()
    sql_string = "SELECT semester_tag FROM Semester WHERE semester_num = (SELECT MAX(semester_num) FROM Semester)"
    cursor.execute(sql_string)
    filename = cursor.fetchone()[0]
    sql_string = "SELECT netID FROM MEMBER"
    cursor.execute(sql_string)
    entries = cursor.fetchall()
    for entry in entries:
        #example string:
        #UPDATE Member SET dues_paid = (SELECT dues_paid FROM Member WHERE netID = 'jmrolf')-1
        #WHERE netID = 'jmrolf'
        sql_update_string = "UPDATE Member SET dues_paid = (SELECT dues_paid FROM Member WHERE netID = '"+str(entry[0])\
                            + "')-1 WHERE netID = '" + str(entry[0])+"'"
        Logger.write_to_log("Logs\\EndOfSemesterLogs\\"+str(filename), sql_update_string+"\n")
        try:
            cursor.execute(sql_update_string)
        except sqlite3.IntegrityError as e:
            Logger.write_to_log("Logs\\EndOfSemesterLogs\\"+str(filename), str(e)+"\n\n")
        except sqlite3.DatabaseError as e:
            Logger.write_to_log("Logs\\EndOfSemesterLogs\\"+str(filename), str(e)+"\n\n")
    connection.commit()


def create_semester(semester_tag, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    # Probably looks scary, but all that does is select the max semester number from the db so that it can
    # create the new semester with the next available number. The TypeError should only fire at the very
    # first semester creation when there were no previous semester numbers.
    try:
        sem_num = cursor.execute("SELECT semester_num FROM Semester "
                                 "WHERE semester_num = (SELECT MAX(semester_num) FROM Semester)").fetchone()[0] + 1
    except TypeError:
        sem_num = 0
    cursor.execute("INSERT INTO Semester VALUES(%s, '%s', '%s', '%s')" % (sem_num, semester_tag, start_date, end_date))
    conn.commit()


def get_most_recent_semester_tag():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        return cursor.execute("SELECT semester_tag FROM SEMESTER "
                              "WHERE semester_num = (SELECT MAX(semester_num) FROM SEMESTER)").fetchone()[0]
    except TypeError:
        return None

######################################################
#           Multi-Workstation and Aggregate          #
#                      Functions                     #
######################################################


def get_data_for_sync():
    """
    This function gets a dictionary object with the following form:
    name = {
            "members" : ["INSERT INTO Members....","INSERT INTO Members..."],
            "tickets" : ["INSERT INTO Ticket....", "INSERT INTO Ticket...."]
            "payments" :["UPDATE MEMBER SET dues_paid =...", "UPDATE MEMBER SET dues_paid = ..."]
           }
    This function allows you to make sure that you are getting back the data you expect, before you pass it
    on to the sync_dbs() function which actually executes the SQL commands stored in the dictionary. The data is
    stored in a JSON like style due to my familiarity with MongoDB

    I deliberately separated these two functions so that when testing you can dig into the dictionary objects to make
    sure you are getting what you expect.

    When I originally coded this (although you are welcome to change it if you prefer) the main database
    was called MIS.CheckIn.sqlite3 and the copy of the database from the other workstation(s) running the system
    should be renamed MIS.CheckIn_copy.sqlite3 and then synced one at a time with the main database. If you want to
    change this naming convention just go up to the top of this file and change the string value in the get_connection()
    and get_copy_connection() functions to whatever you like. Just remember that even though SQL is NOT case sensitive,
    Python is. For a detailed explanation of how this method works see the Visio diagrams associated with the system.

    :return: dictionary("results" :[], "members" : [], "payments" : [])
    """
    connection = get_connection()
    cursor = connection.cursor()

    copy_connection = get_copy_connection()
    copy_cursor = copy_connection.cursor()

    cursor.execute('SELECT * FROM Member')
    main_member_entries = cursor.fetchall()

    copy_cursor.execute('SELECT * FROM Member')
    copy_member_entries = copy_cursor.fetchall()

    results = []
    payments = []
    for copy_entry in copy_member_entries:
        results.append(copy_entry)
        for main_entry in main_member_entries:
            if copy_entry[0] == main_entry[0]:
                results.remove(copy_entry)
                if copy_entry[5] > main_entry[5]:
                    payments.append("UPDATE MEMBER SET dues_paid = "+str(max(copy_entry[5], main_entry[5])) +
                                    " WHERE netID='" + str(main_entry[0]) + "'")


    data = {"members": [], "tickets": [], "payments": payments}
    # 1)members is the array of entirely new members to be synced
    # 2)tickets is the array of tickets to be synced
    # 3)payments is an array of update commands for members who
    #         made payments
    #
    # The dictionary is then to be passed to the sync function
    # to execute the stored SQL commands

    for var in results:
        sql_string = "INSERT INTO Member VALUES(\'"+var[0]+"\', \'"+var[1]+"\', \'"+var[2]+"\', \'"+var[3]+"\', \'" + \
                     var[4]+"\', "+str(var[5])+");"
        data["members"].append(sql_string)

    cursor.execute('SELECT * FROM Ticket WHERE eventID = (SELECT MAX(eventID) FROM Event)')
    copy_cursor.execute('SELECT * FROM Ticket WHERE eventID = (SELECT MAX(eventID) FROM Event)')
    main_ticket_entries = cursor.fetchall()
    copy_ticket_entries = copy_cursor.fetchall()
    results = []
    for copy_entry in copy_ticket_entries:
        results.append(copy_entry)
        for main_entry in main_ticket_entries:
            if copy_entry[1] == main_entry[1]:
                results.remove(copy_entry)

    for var in results:
        sql_string = "INSERT INTO Ticket VALUES("+str(var[0])+", \'"+var[1]+"\');"
        data["tickets"].append(sql_string)
    connection.commit()
    copy_connection.commit()
    return data


def sync_dbs(data):
    """
    Syncs the data from the SQLite shards. Pass in the return value from get_data_for_sync() to this
    function to complete the process of syncing the data.
    :param data: The data to be synced
    :return: None
    """
    connection = get_connection()
    cursor = connection.cursor()
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), "STARTING LOG\n")

    for var in data["members"]:
        try:
            cursor.execute(var)
            Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), var+"\n")
        except Exception as e:
            Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), str(e)+"\n")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()),
                        "----------------------------------------------------------------------------------------")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()),
                        "----------------------------------------------------------------------------------------")
    for var in data["tickets"]:
        try:
            cursor.execute(var)
            Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), var+"\n")
        except Exception as e:
            Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), str(e)+"\n")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()),
                        "----------------------------------------------------------------------------------------")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()),
                        "----------------------------------------------------------------------------------------")
    for var in data["payments"]:
        try:
            cursor.execute(var)
            Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), var+"\n")
        except Exception as e:
            Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), str(e)+"\n")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()),
                        "----------------------------------------------------------------------------------------")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()),
                        "----------------------------------------------------------------------------------------")
    Logger.write_to_log("Logs\DataSyncs\DATA_SYNC"+str(datetime.date.today()), "END LOG\n")


def get_most_recent_event_date():
    """
    Returns a string representation of the most recent event date in the database.
    Replaces '/' characters with '-' characters to make file opening easier. (e.g. OS reads a '/' as a directory)
    :return: A string representation of the most recent event's date.
    """
    connection = get_connection()
    cursor = connection.cursor()
    date = cursor.execute("SELECT Event_Date FROM Event WHERE EventID = (SELECT MAX(EventID) FROM Event)")
    try:
        date = date.fetchone()[0]
        date = str(date).replace("/", "-")
        # OS reads the / as requesting a new directory, have to change to another char
        return date
    except TypeError:  # This should only happen if the Event Table is empty
        return None


def generate_csv_report():
    """
    Creates a .csv attendance report. Places the file in the reports directory.
    This file was, at the time of writing, sent to Dr. Scheibe for evaluation.

    :return: returns the generated files relative path
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Member.email, Member.name, Member.classification, Member.major "
                   "FROM Member JOIN Ticket ON Ticket.netID = Member.netID "
                   "WHERE Ticket.eventID = (SELECT MAX(eventID) FROM Ticket)")
    data = cursor.fetchall()

    date = get_most_recent_event_date()
    file_path = os.getcwd() + "\\Reports\\"+date+"_Attendance_Report.csv"
    with open(file_path, "w") as report_file:
        report_file.write("\""+date+"\",\n")
        for record in data:
            for datum in record:
                report_file.write("\""+datum+"\""+",")   # If you don't surround each datum with " "'s
                                                         # Excel reads the name as two different data points
            report_file.write("\n")
    return report_file.name


def generate_csv_report_alt(eventid):
    """
    Creates a .csv attendance report. Places the file in the reports directory.
    This file was, at the time of writing, sent to Dr. Scheibe for evaluation.

    :return: returns the generated files relative path
    """
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT Member.email, Member.name, Member.classification, Member.major "
                   "FROM Member JOIN Ticket ON Ticket.netID = Member.netID "
                   "WHERE Ticket.eventID = %d" % eventid)
    data = cursor.fetchall()

    date = cursor.execute("SELECT event_date FROM Event WHERE eventID = %d" % eventid).fetchone()[0].replace('/', '_')
    file_path = os.getcwd() + "\\Reports\\"+date+"_Attendance_Report.csv"
    with open(file_path, "w") as report_file:
        report_file.write("\""+date+"\",\n")
        for record in data:
            for datum in record:
                report_file.write("\""+datum+"\""+",")   # If you don't surround each datum with " "'s
                                                         # Excel reads the name as two different data points
            report_file.write("\n")
    return report_file.name


def get_event_aggregates(event_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT event.company, event.Event_Date,COUNT(*) "
                   "FROM Event "
                   "JOIN Ticket ON ticket.eventID = Event.EventID "
                   "GROUP BY Ticket.eventID "
                   "HAVING Ticket.eventID = %d" % event_id)

    ugly_data = cursor.fetchone()
    try:
        pretty_return_data = {'company': ugly_data[0],
                              'date': ugly_data[1],
                              'count': ugly_data[2]}
    except TypeError as e:
        pretty_return_data = {'company': 'NO DATA',
                              'date': 'NO DATA',
                              'count': '0',
                              'error': e}
    return pretty_return_data


def get_event_classification_aggregates(event_id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT classification, COUNT(*) "
                   "FROM Member "
                   "JOIN Ticket ON Ticket.netID = Member.netID "
                   "GROUP BY Member.classification, Ticket.eventID "
                   "HAVING Ticket.eventID = %d" % event_id)
    data = cursor.fetchall()
    pretty_return_data = {}
    for datum in data:  # This for loop translates the tuple into a dictionary
        pretty_return_data[datum[0]] = datum[1]
    return pretty_return_data


def get_event_major_aggregates(previous):
    connection = get_connection()
    cursor = connection.cursor()
    if previous:
        cursor.execute("SELECT Member.major, COUNT(*) "
                       "FROM Member "
                       "JOIN Ticket ON Ticket.netID = Member.netID "
                       "GROUP BY Member.major, Ticket.eventID "
                       "HAVING Ticket.eventID = (SELECT MAX(EventID) FROM Event) ")
    else:
        cursor.execute("SELECT Member.major, COUNT(*) "
                       "FROM Member "
                       "JOIN Ticket ON Ticket.netID = Member.netID "
                       "GROUP BY Member.major, Ticket.eventID "
                       "HAVING Ticket.eventID = (SELECT MAX(EventID) FROM Event) - 1")
    data = cursor.fetchall()
    pretty_data = {}
    try:
        for datum in data:
            pretty_data[datum[0]] = datum[1]
        return pretty_data
    except TypeError:
        return None


####################################################
#             CONFIGURATION FUNCTIONS              #
####################################################


def select_config_info(key):
    """
    Selects a value from the configuration table. This behaves more like
    a key-value NoSQL solution, but in order to avoid introducing a dependency
    on another database technology this has been set up using a traditional SQL database.
    If at some point this is changed, I recommend using Parse as it is very lightweight and only provides
    the features that would be used in this
    :param key: The key from the key-value pair.
    :return: The value from the key-value pair
    """
    conn = get_connection()
    cursor = conn.cursor()
    data = cursor.execute("SELECT value FROM config_info WHERE key='%s'" % key)
    try:
        data = data.fetchone()[0]
        return data
    except TypeError:
        return None