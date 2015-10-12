__author__ = 'John'

import Logger


def get_financial_results(event_id):
    """
    Gathers information from the log files and returns the a dictionary containing the relevant payment information.
    This function was implemented as part of an ongoing process to improve the MIS clubs financial controls.

    :param event_id: The id of the event to be queried
    :return: A dictionary object containing information about the payments made at the event with event id <<event_id>>
    """
    file_name = Logger.get_event_log_file(event_id)
    with open(file_name, "r") as log_file:
        contents = log_file.read()
        contents = contents.split('\n')
        try:
            while True:
                contents.remove('')
        except ValueError:
            pass
        total_payments = 0
        dollars_collected = 0
        previous_update = 0
        uncollected_revenue = 0
        shirt_sales = 0
        for line in contents:
            if "payment made" in line.lower():
                words = line.split(" ")
                try:
                    sems_paid_for = int(words[4])
                except ValueError:
                    sems_paid_for = int(words[3])

                if sems_paid_for == 1:
                    dollars_collected += 15
                    previous_update = 15
                elif sems_paid_for == 2:
                    dollars_collected += 20
                    previous_update = 20
                else:
                    raise ValueError("Something went wrong reading the log File. Impossible number of semesters paid "
                                     "for, or  number of semesters not logged.")
                total_payments += 1
            elif line == "Payment above NOT collected":
                dollars_collected -= previous_update
                uncollected_revenue += previous_update

    result_set = {'revenue': {'num': total_payments, 'dues': dollars_collected, 'shirts': shirt_sales},
                  'expenses': {'uncollected': uncollected_revenue}}
get_financial_results(18)