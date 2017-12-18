ARDUINO_DIR  = /usr/share/arduino
BOARD_TAG    = uno
ARDUINO_PORT = /dev/ttyACM0

include /usr/share/arduino/Arduino.mk

HOST=$(shell hostname)

ifeq ($(HOST), raspberrypi1)
    CPPFLAGS += -DRPI_1
endif
ifeq ($(HOST), raspberrypi2)
    CPPFLAGS += -DRPI_2
endif
