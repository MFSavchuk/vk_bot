#!/usr/bin/env python3
import random
import logging
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

try:
    import settings
except ImportError:
    exit('Do copy settings.py.default settings.py and set token')

group_id = 218052091

log = logging.getLogger("bot")


def configure_logging():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(levelname)s %(message)s'))
    stream_handler.setLevel(logging.DEBUG)
    log.addHandler(stream_handler)

    file_handler = logging.FileHandler('bot.log', mode='a', encoding='UTF-8', delay=False)
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s', datefmt='%d-%m-%Y %H:%M:%S'))
    file_handler.setLevel(logging.DEBUG)
    log.addHandler(file_handler)

    log.setLevel(logging.DEBUG)


class Bot:
    """
    Echo bot для vk.com.

    Use python3.8
    """

    def __init__(self, group_id, token):
        """

        :param group_id: group id группы vk
        :param token: секретный токен
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.api = self.vk.get_api()
        self.long_poller = VkBotLongPoll(self.vk, self.group_id)

    def run(self):
        """Запуск бота"""
        for event in self.long_poller.listen():
            try:
                self.on_event(event)
            except Exception:
                log.exception("Ошибка в обработке события")

    def on_event(self, event):
        """
        Отправляет сообщение назад, если сообщение текстовое

        :param event: VkBotMessageEvent object
        :return: None
        """
        if event.type == VkBotEventType.MESSAGE_NEW:
            log.debug("Отправляем сообщение назад")
            reply_message = f'Получено сообщение: "{event.object.message["text"]}"'
            self.api.messages.send(message=reply_message,
                                   random_id=random.randint(0, 2 ** 20),
                                   peer_id=event.object.message['peer_id']
                                   )
        else:
            log.info("Мы пока не умеем обрабатывать события данного типа %s", event.type)


if __name__ == '__main__':
    configure_logging()
    bot = Bot(settings.GROUP_ID, settings.TOKEN)
    bot.run()
