###############################################################################
#
# Copyright (C) 2014, Interactive Object.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
###############################################################################

from pololu_drv8835_rpi import motors, MAX_SPEED
from twisted.internet.defer import inlineCallbacks
from twisted.logger import Logger

from autobahn.twisted.util import sleep
from autobahn.twisted.wamp import ApplicationSession
from autobahn.wamp.exception import ApplicationError


class AppSession(ApplicationSession):

    log = Logger()

    @inlineCallbacks
    def onJoin(self, details):

        # SUBSCRIBE to a topic and receive events
        #
        def onhello(msg):
            self.log.info("event for 'onhello' received: {msg}", msg=msg)

        yield self.subscribe(onhello, 'com.interactive-object.onhello')
        self.log.info("subscribed to topic 'onhello'")

        # REGISTER a procedure for remote calling
        #
        def forward():
            self.log.info("forward")
            
        def stop():
            self.log.info("stop")
            
        yield self.register(forward, 'com.interactive-object.forward')
        self.log.info("procedure add2() forward")

