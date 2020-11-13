import configparser
import json


def response_handler(code, msg):
    return {
        'statusCode': code,
        'body': json.dumps(msg)
    }


def get_config_factor():
    """ parses the config.ini and returns the factor """
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        return float(config["PARAMETERS"]["FACTOR"])
    except Exception as e:
        return response_handler(500, str(e))


def validate_and_calculate(request_body):
    """ Validates whether the request is in required format and calculates the serviceability
        valid frequency values:- "yearly, monthly and fortnightly"
    """

    monthly_income = 0.0
    monthly_expense = 0.0

    config_factor = get_config_factor()
    if not isinstance(config_factor, float):
        return config_factor

    if not all(key in request_body for key in ("incomes", "expenses")):
        return response_handler(400, "request is not valid, incomes and expenses key values should be present")

    for key in request_body:
        if key == "incomes":
            for income in request_body[key]:
                if len(income) !=  2:
                    return response_handler(400, "income values should be of type [income, frequency]")

                try:
                    income_value = float(income[0])
                except Exception as e:
                    return response_handler(400, "{} should be of type float".format(income[0]))

                if income[1] not in ["fortnightly", "monthly", "yearly"]:
                    return response_handler(400, "frequency should be of type fortnightly, monthly or yearly")

                if income[1] == "fortnightly":
                    monthly_income += income_value * 2.0
                elif income[1] == "monthly":
                    monthly_income += income_value
                else:
                    monthly_income += income_value/12.0
        elif key == "expenses":
            for expense in request_body[key]:
                try:
                    expense_value = float(expense)
                except Exception as e:
                    return response_handler(400, "{} should be of type float".format(expense))
                monthly_expense += expense_value

    return response_handler(200, config_factor * (monthly_income - monthly_expense))


def handler(event, context):
    """
        Calculates serviceability of an application from event.body content

        Args:
            event['body']:
                {
                    incomes: [[income value, frequency]],
                    expenses: [mortgage, creditcard bill]
                }
        Returns:
            (monthly income - monthly expenses) * factor
    """
    try:
        json_content = json.loads(event['body'])
    except Exception as e:
        return response_handler(400, "Request body in not a valid json")

    return validate_and_calculate(json_content)

