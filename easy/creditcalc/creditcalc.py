import sys
import math


def incorrect_params():
    print('Incorrect parameters')
    quit()


def calc_diff(m):
    return principal / periods + nominal * (principal - principal * (m - 1) / periods)


def calc_annuity():
    return principal * nominal * math.pow(1 + nominal, periods) / (math.pow(1 + nominal, periods) - 1)


def calc_principal():
    return payment * (math.pow(1 + nominal, periods) - 1) / (nominal * math.pow(1 + nominal, periods))


def calc_periods():
    return math.log(payment / (payment - nominal * principal), 1 + nominal)


args = sys.argv

# Initialize program variables with default values.
pay_type = ''
payment = -1
principal = -1
periods = -1
interest = -1

if len(args) < 4:
    incorrect_params()

# Parse command line parameters.
for i in range(1, len(args)):
    param = args[i]

    if param.startswith('--type='):
        # Error check the 'type' option.
        if pay_type != '':
            incorrect_params()
        val = param[param.find('=') + 1:]
        if val == 'annuity' or val == 'diff':
            pay_type = val
        else:
            incorrect_params()
    elif param.startswith('--payment='):
        # Error check the 'payment' argument.
        if payment != -1:
            incorrect_params()
        if pay_type == 'diff':
            incorrect_params()
        val = float(param[param.find('=') + 1:])
        if val < 0:
            incorrect_params()
        payment = val
    elif param.startswith('--principal='):
        # Error check the 'principal' argument.
        if principal != -1:
            incorrect_params()
        val = float(param[param.find('=') + 1:])
        if val < 0:
            incorrect_params()
        principal = val
    elif param.startswith('--periods='):
        # Error check the 'periods' argument.
        if periods != -1:
            incorrect_params()
        val = float(param[param.find('=') + 1:])
        if val < 0:
            incorrect_params()
        periods = math.ceil(val)
    elif param.startswith('--interest='):
        # Error check the 'interest' argument.
        if interest != -1:
            incorrect_params()
        val = float(param[param.find('=') + 1:])
        if val < 0:
            incorrect_params()
        interest = val
    else:
        incorrect_params()

# Ensure that the payment type and interest variables were properly set.
if pay_type == '':
    incorrect_params()
if interest == -1:
    incorrect_params()

# Calculate and store the nominal interest.
nominal = (interest / 100) / 12

if pay_type == 'diff':
    # Handle calculating differentiated payments.
    total = 0
    for i in range(1, periods + 1):
        diff_payment = math.ceil(calc_diff(i))
        total += diff_payment
        print('Month {}: paid out {}'.format(i, diff_payment))
    print('\nOverpayment = {}'.format(total - principal))
elif pay_type == 'annuity':
    # Handle calculating annuity payments, principal, or period count based on the variable which was not given a value.
    if payment == -1:
        payment = math.ceil(calc_annuity())
        print('Your annuity payment = {}!'.format(payment))
        print('Overpayment = {}'.format(payment * periods - principal))
    elif principal == -1:
        principal = math.ceil(calc_principal())
        print('Your credit principal = {}!'.format(principal))
        print('Overpayment = {}'.format(payment * periods - principal))
    elif periods == -1:
        periods = math.ceil(calc_periods())
        years = periods / 12
        if years == 0:
            print('You need {} months to repay this credit!'.format(periods))
        elif periods % 12 == 0:
            print('You need {} years to repay this credit!'.format(int(years)))
        else:
            print('You need {} years and {} months to repay this credit!'.format(years, periods - (years * 12)))
        print('Overpayment = {}'.format(payment * periods - principal))
