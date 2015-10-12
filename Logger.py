__author__ = 'John'
import os
import MIS_Database_Functions


def get_event_log_file(eventID=None):
    """
    This function selects data from the database and uses it to construct a file path and name.
    :return: The string value representing the directory path to the log file
    """

    working_directory = os.getcwd()
    working_directory += "\\Logs\\EventLogs\\"

    connection = MIS_Database_Functions.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT semester_tag FROM Semester WHERE semester_num = (SELECT MAX(semester_num) FROM Semester)")
    file_name = cursor.fetchone()[0]
    if eventID is None:
        cursor.execute("SELECT MAX(eventID) FROM Event")
    else:
        cursor.execute("SELECT eventID FROM Event WHERE eventID = %d" % eventID)
    event_id = cursor.fetchone()[0]
    cursor.execute("SELECT company FROM Event WHERE (eventID = \'" + str(event_id) + "\')")
    company_name = cursor.fetchone()[0]
    file_name += "_ID" + str(event_id) + "_" + company_name
    file_name = file_name.replace(" ", "_")

    log_file = working_directory + file_name
    return log_file


def write_to_log(file_name, to_log):
    """
    <em>APPENDS</em> to the passed file name. Normally just pass the return value from get_log_file() to this function.
    If the file does not exist, it will be created.

    :param file_name: A string representing the directory path to the log file
    :param to_log: The string to be logged to the file. Adds a \n to the passed data to log to be logged
    :return:
    """
    with open(file_name, 'a') as logFile:
        try:
            logFile.write(to_log)
        except IOError as e:
            print(str(e))