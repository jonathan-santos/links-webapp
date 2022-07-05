from os import environ

bind = f'0.0.0.0:{environ["PORT"]}'
workers = 4
