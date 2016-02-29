from __future__ import absolute_import, unicode_literals

import unittest

from irc.parser import Response

FULL_RESPONSE_PRIVMSG = (
    '@color=#0D4200;display-name=TWITCH_UserNaME;user-type= '
    ':twitch_username!twitch_username@twitch_username.tmi.twitch.tv '
    'PRIVMSG #channel :!test Kappa Keepo Kappa'
)


class TestParser(unittest.TestCase):
    def test_tags(self):
        response = Response(FULL_RESPONSE_PRIVMSG)
        self.assertDictEqual(
            response.tags,
            {
                'color': '#0D4200',
                'display-name': 'TWITCH_UserNaME',
                'user-type': ''
            }
        )

    def test_response_from(self):
        response = Response(FULL_RESPONSE_PRIVMSG)
        self.assertEqual(
            response.response_from,
            'twitch_username!twitch_username@twitch_username.tmi.twitch.tv'
        )

    def test_command(self):
        response = Response(FULL_RESPONSE_PRIVMSG)
        self.assertEqual(
            response.command,
            'PRIVMSG'
        )
        
    def test_parameters(self):
        response = Response(FULL_RESPONSE_PRIVMSG)
        self.assertEqual(
            response.parameters,
            '#channel :!test Kappa Keepo Kappa'
        )
        
    def test_privmsg_data(self):
        response = Response(FULL_RESPONSE_PRIVMSG)
        self.assertDictEqual(
            response.data,
            {
                'target': '#channel',
                'message': '!test Kappa Keepo Kappa',
                'command': 'test',
            }
        )
