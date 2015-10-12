__author__ = 'jmrolf'
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
In the interest of simplicity, I left all data about email targets in a simple text file
rather than in a database table since this information is not going to be needed for any aggregation
or other complex data needs.
"""


def add_email_recipients(new_addresses):
    """
    Adds the passed email addresses to the AdminData\email_targets.txt file.
    This functionality is used to update who receives the weekly attendance report emails.

    :param new_addresses: The addresses of the new email targets delimited by commas
    :return: A string informing the consumer what happened
    """
    new_addresses = new_addresses.replace(" ", "")
    new_addresses = new_addresses.split(",")
    new_addresses_lower = []
    for address in new_addresses:
        address = address.lower()
        new_addresses_lower.append(address)
        if "@iastate.edu" not in address and "@gmail.com" not in address:
            raise AttributeError("Targets must be either gmail or iastate targets")

    already_there_array = []
    with open("AdminData/email_targets.txt", "r") as target_file:
        for line in target_file:
            for address in new_addresses_lower:
                if line.strip() == address:
                    already_there_array.append(address)
                    new_addresses_lower.remove(address)

    # Add addresses to the admin file and tell the consumer what addresses were added to the admin file
    result_string = ""
    with open("AdminData/email_targets.txt", "a+") as target_file:
        if len(new_addresses_lower) > 0:
            result_string += ", ".join(new_addresses_lower)+" was/were added to the admin file.\n"
            for new_address in new_addresses_lower:
                target_file.write(new_address+"\n")

    # Tell consumer if any of the addresses were already there
    if len(already_there_array) > 0:
        result_string += ", ".join(already_there_array)+\
                         " was/were not added because the address(es) were already there."
    return result_string


def delete_email_recipients(addresses):
    """
    Removes an email from the AdminData\email_targets.txt file.
    This removes the passed address from the list of email targets for the weekly attendance reports.

    :param addresses: A comma delimited list of emails to be removed from the AdminData\email_targets.txt file.
    :return: A string representing what the function did
    """
    addresses = addresses.replace(" ", "")
    addresses = addresses.split(",")
    addresses_lower = []
    for address in addresses:
        address = address.lower()
        addresses_lower.append(address)

    with open("AdminData\email_targets.txt", "r") as file:
        contents = file.read()

    delete_array = []
    not_in_file_array = []
    for address in addresses_lower:
        if address in contents:
            delete_array.append(address)
        else:
            not_in_file_array.append(address)

    result_string = ""
    if len(delete_array) > 0:
        for delete in delete_array:
            contents = contents.replace(delete, "")
            result_string += delete+" "
        result_string += " was/were deleted from the admin file.\n"
    if len(not_in_file_array) > 0:
        for deleted_not in not_in_file_array:
            result_string += deleted_not
        result_string += " was/were not deleted from the admin file because they were not there"

    new_contents = contents.split("\n")
    contents = ""

    for line in new_contents:
        if line != '' and line != ',':
            contents += line+"\n"
    with open("AdminData\email_targets.txt", "w") as target_file:
        target_file.write(contents)
    return result_string


def get_email_recipients():
    """
    Returns a list of the current email recipients.

    :return: A list of the current email recipients
    """
    targets = []
    with open("AdminData/email_targets.txt", "r") as target_file:
        for line in target_file:
            if line[0] != '#':
                line = line.strip()
                if len(line) != 0:
                    targets.append(line)
    return targets


def email_attendance_report(report):
    """
    Accepts a .csv file as an input (report) and then emails it to the the passed address(es) (receiver_emails)
    :param report: The report to be sent
    :return: True if successful

    !!!WARNING!!!
    This function is completely dependant upon the continued existence of the server with domain name 'smtp.gmail.com'.
    If this server for some reason becomes inaccessible, the function will always throw an error. If possible it
    would be better to move this to a club server or an ISU SMTP server, but at the time of writing no such possibility
    existed.
    """
    sender_email_address = "isumisexec@gmail.com"
    receiver_email_addresses = get_email_recipients()
    subject = "Attendance Report"
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['To'] = ", ".join(receiver_email_addresses)
    msg['From'] = sender_email_address
    msg.preamble = "Attendance Report"

    main_text = MIMEText(
        "Hello MIS Senior Executive(s) and Adviser(s):\n"
        "See attached the attendance report for the most recent meeting of the MIS Club.\n"
        "Best,\n"
        "MIS Exec Technical Team\n\n\n"
        "This is an automated message sent by the MIS Club check in system.\n"
        "The contents of this email should not be shared without the express written consent of the MIS Executive board"
    )
    msg.attach(main_text)

    file = open(report, "r")
    attachment = MIMEText(file.read())
    file.close()

    attachment.add_header("Content-Disposition", "attachment", filename=report.replace("Reports/", ""))
    msg.attach(attachment)

    server_name = 'smtp.gmail.com:587'
    server = smtplib.SMTP(server_name)
    server.ehlo()
    server.starttls()

    username = "isumisexec"
    pw = "irysawjrltckikpq"
    server.login(username, pw)
    server.sendmail(sender_email_address, msg['To'].split(","), msg.as_string())
    server.quit()
