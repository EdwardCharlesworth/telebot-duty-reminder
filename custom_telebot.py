from telebot import TeleBot


class CustomTeleBot(TeleBot):

    @staticmethod
    def _build_handler_dict(handler, **filters):
        """
        Builds a dictionary for a handler
        :param handler:
        :param filters:
        :return:
        """
        chat_id = filters.pop('chat_id', None)

        if chat_id is None:
            return TeleBot._build_handler_dict(handler, **filters)

        return {
            'function': handler,
            'filters': filters,
            'chat_id': chat_id,
        }

    def callback_query_handler(self, func, **kwargs):
        """
        Callback request handler decorator
        :param func:
        :param kwargs:
        :return:
        """
        chat_id = kwargs['chat_id']

        def decorator(handler):
            handler_dict = self._build_handler_dict(handler, func=func, **kwargs)
            self.delete_callback_query_handlers(chat_id)
            self.add_callback_query_handler(handler_dict)
            return handler

        return decorator

    def delete_callback_query_handlers(self, chat_id):
        for callback_query_handler in self.callback_query_handlers:
            if callback_query_handler['chat_id'] == chat_id:
                self.callback_query_handlers.remove(callback_query_handler)