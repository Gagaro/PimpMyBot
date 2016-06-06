import json

from utils.commands import Command, get_action_info


def handle_connexion(response, client):
    """
    Activate twitch capabilities and join channel.
    """
    if response.command != '001':
        return

    client.send('CAP REQ :twitch.tv/membership', type='raw')
    client.send('CAP REQ :twitch.tv/commands', type='raw')
    client.send('CAP REQ :twitch.tv/tags', type='raw')
    client.send(None, type='join')
    client.remove_handler(handle_connexion)


def handle_commands(response, client):
    """ handle custom commands """
    if response.command != 'PRIVMSG':
        return
    if response.data['command'] is None:
        return
    try:
        command = Command.get(command=response.data['command'])
    except Command.DoesNotExist:
        return
    for action in command.get_actions():
        info = get_action_info(action)
        parameters = json.loads(action.parameters)
        for parameter in info.get('parameters', []):
            if parameter.name in [parameters.keys()]:
                value = parameters[parameter.name]
                parameters[parameter.name] = parameter.normalize(value)
        info['method'](response=response, client=client, **parameters)
