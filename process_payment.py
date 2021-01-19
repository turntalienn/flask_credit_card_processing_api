from datetime import datetime
from flask import Response
from payment_gateway import *


class Validate:
    def __init__(self, credit_card_num, card_holder, exp_date, security_code, amount):
        self.credit_card_num = credit_card_num
        self.card_holder = card_holder
        self.exp_date = exp_date
        self.security_code = security_code
        self.amount = amount

    def validate_card_num(self, credit_card_num):
        """implementing luhn"s algorithm for validating card num
        """
        card_num = list(credit_card_num)
        check_digit = card_num.pop()
        card_num.reverse()
        proc_digits = []

        for index, digit in enumerate(card_num):
            if index % 2 == 0:
                doubled_digit = int(digit) * 2

                if doubled_digit > 9:
                    doubled_digit = doubled_digit - 9

                proc_digits.append(doubled_digit)
            else:
                proc_digits.append(int(digit))

        total = int(check_digit) + sum(proc_digits)
        if total % 10 == 0:
            return True
        else:
            return False

    def validate_data(self):
        """
            in > credit card details
            out > [response] valid or invalid card

        """
        if self.credit_card_num:
            if type(self.credit_card_num) == str:
                resp = self.validate_card_num(self.credit_card_num)
                if not resp:
                    return Response("Bad request", status=400)
            else:
                return Response("Bad request", status=400)
        else:

            return Response("Bad request", status=400)

        if self.card_holder:
            if type(self.card_holder) != str:
                return Response("Bad request", status=400)
        else:
            return Response("Bad request", status=400)

        if self.exp_date:
            if type(self.exp_date) == datetime:
                current_date = datetime.today()
                if self.exp_date < current_date:
                    return Response("Bad request", status=400)
            else:
                return Response("Bad request", status=400)
        else:
            return Response("Bad request", status=400)

        if self.security_code:
            if len(self.security_code) != 3 or type(self.security_code) != str:
                return Response("Bad request", status=400)

        if self.amount:
            if type(self.amount) != float and self.amount >= 0:
                return Response("Bad request", status=400)
        else:
            return Response("Bad request", status=400)


class Payment:
    def __init__(self):
        self.tries = 0

    def process_payment(self, credit_card_num, card_holder, exp_date, security_code, amount):
        """
            in > credit card details
            out > response
        """
        active = True  # To check whether the payment gateway is available
        v = Validate(credit_card_num, card_holder, exp_date, security_code, amount)
        v.validate_data()
        payment = Payment()
        try:
            if amount <= 20:
                if active:  # used to check availability of payment gateway
                    resp = cheap_payment_gateway(credit_card_num, card_holder, exp_date, security_code, amount)
                    payment.tries += 1
                    return resp

            if amount >= 21 or amount <= 500:
                if active:  # used to check availability of payment gateway
                    resp = expensive_payment_gateway(credit_card_num, card_holder, exp_date, security_code, amount)
                    payment.tries += 1
                    return resp
                else:
                    resp = cheap_payment_gateway(credit_card_num, card_holder, exp_date, security_code, amount)
                    payment.tries += 1

            if amount >= 500:
                if active:  # used to check availability of payment gateway
                    while payment.tries <= 3:
                        resp = premium_payment_gateway(credit_card_num, card_holder, exp_date, security_code, amount)
                        payment.tries += 1
                        return resp

        except:
            return Response("Internal Server error", status=500)
