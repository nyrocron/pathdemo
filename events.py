# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""events.py: event management"""

import pygame


class EventError(Exception):
    pass


class EventManager(object):
    _event_code_counter = pygame.NUMEVENTS

    def __init__(self):
        self._subscriptions = {}
        self._user_subscriptions = {}

    def subscribe(self, event_type, callback):
        if event_type < pygame.NUMEVENTS:
            subscription_dict = self._subscriptions
        else:
            subscription_dict = self._user_subscriptions

        if not event_type in subscription_dict:
            subscription_dict[event_type] = set()
        subscription_dict[event_type].add(callback)

    def unsubscribe(self, event_type, callback):
        if event_type < pygame.NUMEVENTS:
            subscription_dict = self._subscriptions
        else:
            subscription_dict = self._user_subscriptions

        subscription_dict[event_type].remove(callback)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self._handle_user_event(event)

            try:
                for f in self._subscriptions[event.type]:
                    f(event)
            except KeyError:
                pass

    @staticmethod
    def post(code, **kwargs):
        if 'code' in kwargs:
            raise EventError("user events may not define a code attribute")

        kwargs['code'] = code
        pygame.event.post(pygame.event.Event(pygame.USEREVENT, kwargs))

    @staticmethod
    def new_event_code():
        EventManager._event_code_counter += 1
        return EventManager._event_code_counter

    def _handle_user_event(self, event):
        try:
            for f in self._user_subscriptions[event.code]:
                f(event)
        except KeyError:
            pass