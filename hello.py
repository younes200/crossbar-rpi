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
        def forwardOn():
            self.log.info("forwardOn")
            motors.motor1.setSpeed(SPEED_2V)
            motors.motor2.setSpeed(SPEED_2V)
            
        def forwardOff():
            self.log.info("forwardOff")
            motors.motor1.setSpeed(0)
            motors.motor2.setSpeed(0)

        # REGISTER a procedure for remote calling
        #
        def backwardOn():
            self.log.info("backwardOn")
            motors.motor1.setSpeed(-SPEED_2V)
            motors.motor2.setSpeed(-SPEED_2V)
            
        def backwardOff():
            self.log.info("backwardOff")
            motors.motor1.setSpeed(0)
            motors.motor2.setSpeed(0)
            
        def leftOn():    
            motors.motor2.setSpeed(SPEED_2V)
            
        def leftOff():
            motors.motor2.setSpeed(0)

        def rightOn():    
            motors.motor1.setSpeed(SPEED_2V)
            
        def rightOff():
            motors.motor1.setSpeed(0)
            
        yield self.register(forwardOn, 'com.interactive-object.forwardon')
        yield self.register(forwardOff, 'com.interactive-object.forwardoff')
        yield self.register(backwardOn, 'com.interactive-object.backwardon')
        yield self.register(backwardOff, 'com.interactive-object.backwardoff')

        yield self.register(leftOn, 'com.interactive-object.lefton')
        yield self.register(leftOff, 'com.interactive-object.leftoff')
        yield self.register(rightOn, 'com.interactive-object.righton')
        yield self.register(rightOff, 'com.interactive-object.rightoff')
        
        self.log.info("procedure registered")

