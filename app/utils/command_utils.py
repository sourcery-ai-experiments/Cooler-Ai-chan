# app/utils/command_utils.py
from discord.ext import commands
from app.config import Config


def modify_command_name(name):
    """ Modify the command name based on the environment """
    return f'test_{name}' if Config.ENVIROMENT == 'development' else name

def custom_command(*args, **kwargs):
    """ Custom command decorator that modifies the command name based on the environment """
    def decorator(func):
        kwargs['name'] = modify_command_name(kwargs.get('name', func.__name__))
        return commands.command(*args, **kwargs)(func)
    return decorator
