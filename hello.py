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
    _voice = "slt"
    _flite = "/usr/bin/flite"

    @inlineCallbacks
    def onJoin(self, details):

        # SUBSCRIBE to a topic and receive events
        #
        def onhello(msg):
            self.log.info("event for 'onhello' received: {msg}", msg=msg)

        yield self.subscribe(onhello, 'com.interactive-object.iot.onhello')
        self.log.info("subscribed to topic 'onhello'")

        # becomes true when currently speaking
        self._is_busy = False

        # register methods on this object for remote calling via WAMP
        for proc in [self.say, self.is_busy]:
            uri = u'com.interactive-object.iot.speechsynth.{}'.format(proc.__name__)
            yield self.register(proc, uri)
            self.log.msg("SpeechSynthAdapter registered procedure {}".format(uri))

        # signal we are done with initializing our component
        self.publish('com.interactive-object.iot.speechsynth.on_ready')
        self.log.msg("SpeechSynthAdapter ready.")
        
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
            
        yield self.register(forwardOn, 'com.interactive-object.iot.forwardon')
        yield self.register(forwardOff, 'com.interactive-object.iot.forwardoff')
        yield self.register(backwardOn, 'com.interactive-object.iot.backwardon')
        yield self.register(backwardOff, 'com.interactive-object.iot.backwardoff')

        yield self.register(leftOn, 'com.interactive-object.iot.lefton')
        yield self.register(leftOff, 'com.interactive-object.iot.leftoff')
        yield self.register(rightOn, 'com.interactive-object.iot.righton')
        yield self.register(rightOff, 'com.interactive-object.iot.rightoff')
        
        self.log.info("procedure registered")

    @inlineCallbacks
    def say(self, text):
        """
        Speak text.
        """
        if self._is_busy:
            raise Exception("already talking")
        else:
            # mark TTS engine as busy and publish event
            self._is_busy = True
            self.publish('com.interactive-object.iot.speechsynth.on_speech_start', text)

            # start TTS
            yield getProcessOutput(self._flite, ['-voice', self._voice, '-t', text])

            # mark TTS engine as free and publish event
            self._is_busy = False
            self.publish('com.interactive-object.iot.speechsynth.on_speech_end')

    def is_busy(self):
        """
        Check if TTS engine is currently busy speaking.
        """
        return self._is_busy
        
