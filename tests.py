from unittest import TestCase
from unittest.mock import patch, Mock, ANY

from vk_api.bot_longpoll import VkBotMessageEvent

from bot import Bot


class Test1(TestCase):
    RAW_EVENT = {
        'group_id': 218052091,
        'type': 'message_new',
        'event_id': '692fb369b69ec498cc4a88d905c5a85c01397d6a',
        'v': '5.131',
        'object': {
            'message': {
                'date': 1673176113,
                'from_id': 5189952,
                'id': 83,
                'out': 0,
                'attachments': [],
                'conversation_message_id': 58,
                'fwd_messages': [],
                'important': False,
                'is_hidden': False,
                'peer_id': 5189952,
                'random_id': 0,
                'text': 'hi bot'},
            'client_info': {
                'button_actions':
                    ['text', 'vkpay', 'open_app', 'location', 'open_link', 'callback', 'intent_subscribe',
                     'intent_unsubscribe'],
                'keyboard': True,
                'inline_keyboard': True,
                'carousel': True,
                'lang_id': 0}
        }
    }
    REPLY_MESSAGE = f'Получено сообщение: "{RAW_EVENT["object"]["message"]["text"]}"'

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count  # [obj, obj, ...]
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock
        with patch('bot.VkApi'):
            with patch('bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(obj)
                assert bot.on_event.call_count == count

    def test_on_event(self):
        event = VkBotMessageEvent(raw=self.RAW_EVENT)
        send_mock = Mock()
        with patch('bot.VkApi'):
            with patch('bot.VkBotLongPoll'):
                bot = Bot('', '')
                bot.api = Mock()
                bot.api.messages.send = send_mock
                bot.on_event(event)

        send_mock.assert_called_once_with(
            message=self.REPLY_MESSAGE,
            random_id=ANY,
            peer_id=self.RAW_EVENT['object']['message']['peer_id']
        )

# coverage run --source=bot -m unittest
# coverage report -m
