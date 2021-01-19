from flask import Response


def premium_payment_gateway(self, *kwargs):
    return Response("OK", status=200)


def expensive_payment_gateway(self, *kwargs):
    return Response("OK", status=200)


def cheap_payment_gateway(self, *kwargs):
    return Response("OK", status=200)
