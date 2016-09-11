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

SPEED_2V = MAX_SPEED / 2

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
            motors.motor1.setSpeed(SPEED_2V)
            motors.motor2.setSpeed(SPEED_2V)
            
        def stop():
            self.log.info("stop")
            motors.motor1.setSpeed(0)
            motors.motor2.setSpeed(0)
            
        yield self.register(forward, 'com.interactive-object.forward')
        yield self.register(stop, 'com.interactive-object.stop')
        self.log.info("procedure forward() and stop() registered")

