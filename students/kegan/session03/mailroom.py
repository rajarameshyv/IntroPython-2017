#!/usr/bin/env python3

"""
Kathryn Egan

This program manages donors and their donations for
Miuvenile Care, a charity organizaiton for disadvantaged
kittens.
"""


DONORS = {
    'Benedict Cumberbatch': [200000.0],
    'Elon Musk': [10000.0, 150000.0, 100000.0],
    'Dad': [20.0, 5.0],
    'Donald Trump': [2.81],
    'Billy Neighbor': [.54, .01, .25]}

COLUMN_WIDTHS = [0] * 4


def main():
    """ Module that drives main menu."""
    options = {
        '1': {
            'prompt': 'Send a Thank You',
            'function': print_thank_you},
        '2': {
            'prompt': 'Create a Report',
            'function': print_report},
        '3': {
            'prompt': 'Write Thank Yous',
            'function': write_thank_yous},
        '4': {
            'prompt': 'Quit',
            'function': exit_program}}
    while True:
        print('Please choose from the following options:')
        prompt = '\n'.join(['{} {}'.format(
            num, option['prompt']) for num, option in options.items()])
        answer = safe_input(prompt + '\n>')
        if answer in options:
            options[answer]['function']()


def safe_input(prompt):
    try:
        answer = input(prompt)
    except (KeyboardInterrupt, EOFError):
        return '4'  # returns the option that quits the program
    return answer


def exit_program():
    """ Exits program."""
    from sys import exit
    print()
    print('Exiting...')
    exit()


def print_thank_you():
    """ Prompts user for donor name and amount and prints thank
    you note to the console. Donation amount must be numerical."""
    while True:
        donor = input(
            'Who donated? (Enter LIST to see current list of donors)\n>')
        if not donor:
            continue
        if donor.upper() != 'LIST':
            break
        print()
        print('Current donors:')
        print('\n'.join(sorted(DONORS)))
        print()
    donor = ' '.join(donor.split()).title()
    donation = get_donation()
    DONORS.setdefault(donor, []).append(donation)
    thankyou = get_thank_you(donor, [donation])
    print(horizontal_line(80))
    print(thankyou)
    print(horizontal_line(80))


def get_donation():
    """ Prompts user for and returns donation amount.
    Will passive aggressively make a thank you for a
    zero-dollar amount.
    Returns:
        float : amount donated"""
    while True:
        donation = input('How much was donated?\n>')
        try:
            donation = float(donation.strip('$'))
            return donation
        except ValueError:
            print('{} is not a valid amount.'.format(donation))
            print('Please try again.')


def horizontal_line(length):
    """ Returns a horizontal line of given length.
    Args:
        length (int) : length of horizontal line
    Returns:
        str : horizontal line
    """
    return '-' * length


def get_thank_you(donor, donations):
    """ Returns a thank you message for the donor based
    off given donation if any, otherwise all donations
    in database.
    Args:
        donor (str) : name of donor
        donation (None or float) : specified donation
    Returns:
        str : thank you message for donor
    """
    total = sum(donations)
    num = len(donations)
    # build up elements of thank you message
    substrings = {
        'donor': donor,
        's': 's' if num > 1 else '',
        'and': ' and ' if num > 1 else '',
        'first': ', '.join([
            dollar(d) for d in donations[:-1]]),
        'rest': dollar(donations[-1]),
        'totalling': '' if num < 1 else ', totalling {}${},'.format(
            'an incredible ' if total > 500 else '', dollar(total))}
    message = \
        'Dear {donor},\nThank you for your generous gift{s} of ' +\
        '{first}{and}{rest}. Your donation{s}{totalling} will ' +\
        'go towards feeding homeless kittens in Seattle. ' +\
        'From the bottom of our hearts, we at Miuvenile Care thank you.\n\n' +\
        'Regards,\nBungelina Bigglesnorf\nChairwoman, Miuvenile Care'
    message = message.format(**substrings)
    return message


def dollar(amount):
    """ Returns amount in dollar format. Removes trailing
    .00s to create a clean amount.
    Args:
        amount (float) : dollar amount to format
    Returns:
        str : dollar amount as a string
    """
    return '${:,.2f}'.format(amount).replace('.00', '')


def print_report():
    """ Prints a report showing donors and donation data to console."""
    headers = ('Donor Name', 'Total Given', 'Num Gifts', 'Average Gift')
    update_widths(headers)
    data = []
    # obtain data and determine ideal column lengths before making report
    for donor in sorted(DONORS, key=by_donation, reverse=True):
        donations = DONORS[donor]
        line = [donor, sum(donations), len(donations), average(donations)]
        update_widths(line)
        data.append(line)
    report = []
    report.append(stringify(headers, '| '))
    line_width = sum(COLUMN_WIDTHS) + len(COLUMN_WIDTHS) * 2 + 1
    report.append(horizontal_line(line_width))
    for row in data:
        report.append(stringify(row, ' '))
    print('\n' + '\n'.join(report) + '\n')


def update_widths(line):
    """ Updates minimum column widths based on
    the length of items (as strings) in given line.
    Args:
        line (list) : list of values
    """
    for index in range(len(line)):
        item = line[index]
        # dollar amounts are slightly longer in final report
        if type(item) is float:
            item = '{:,.2f}'.format(item)
        item = str(item)
        if len(item) > COLUMN_WIDTHS[index]:
            COLUMN_WIDTHS[index] = len(item)


def write_thank_yous():
    """ Writes thank yous to all donors in individual
    files in a ThankYous folder in the program's cwd."""
    import os
    print('Writing new thank yous to all donors...')
    for donor in DONORS:
        thankyou = get_thank_you(donor, DONORS[donor])
        if not os.path.exists('ThankYous'):
            os.mkdir('ThankYous')
        with open(os.path.join('ThankYous', donor + '.txt'), 'w') as f:
            f.write(thankyou)
    print('Thank yous written to\n{}'.format(
        os.path.join(os.getcwd(), 'ThankYous')))


def by_donation(donor):
    """ Returns the sum of the donations for given donor.
    Args:
        donor (str) : donor name
    Returns:
        float : sum of all donations for given donor
    """
    return sum(DONORS[donor])


def average(donations):
    """ Returns average of given donations rounded to 2 decimals.
    Args:
        donations (list of floats) : list of donations
    Returns:
        float : average of donations
    """
    avg = sum(donations) / len(donations)
    return round(avg, 2)


def stringify(row, separator):
    """ Returns given row as a string. Formats values based
    on type.
    Args:
        row (list of str) : list of items in row
        separator (str) : separator for columns
    Returns:
        str : row as a string
    """
    line = []
    for value, width in zip(row, COLUMN_WIDTHS):
        # monetary values get WS inserted between $ and number
        if type(value) is float:
            value = '{:,.2f}'.format(value)
            value = '${}{} '.format(' ' * (width - len(str(value))), value)
        # numbers have leading WS with one extra WS in front and back
        elif type(value) is int:
            value = ' {}{} '.format(' ' * (width - len(str(value))), value)
        # names having trailing WS with one extra WS
        else:  # str format
            value = '{}{} '.format(value, ' ' * (width - len(value)))
        line.append(value)
    return separator.join(line).strip()


if __name__ == '__main__':
    main()
