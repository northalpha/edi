# Dependencies

## rabbitmq

For development docker seemes a good choice:

    sudo docker run -p :5672 -p :15672 -v /scratch/docker-data/rabbitmq:/var/lib/rabbitmq/mnesia f04150b0661e
    sudo docker build github.com/mikaelhg/docker-rabbitmq.git

Note that the exchanges are configured by hand..

Use `mopp`, running on the dell netbook.

## useful debian packages

-   python-pika
-   python-amqplib
-   amqp-tools

# Repository Organization

-   **src:** Tools that only **publish** messages
-   **sink:** Tools that only **consume** messages
-   **proc:** Tools that **consume** and **publish** with some kind of
    processing going on
-   **bot:** Adapter to other protocols like IRC. **publisher** and **consumer**
-   **demo:** Useful stuff for testing, reference, whatever

# Ideas, Todos

## Features

### OPEN User Notifications

-   Im LDAP gibt es eine liste mit wegen einen user zu notifien
    -   IRC nick
    -   jabber id
    -   twitter account (@foo)
    -   email
-   Notifications werden "reliable" zugestellt. Irgendwo kommt die
    notification an
-   Message exchange und consumer sagen nack, wenn nicht zustellbar.
    Z.B. IRC offline
-   Aehlich wie die notify exchange, audio fuer shouts in den subraum
-

### ASSIGNED pizza / essen / f00d     :@hej:c3po:

### DONE scheduled messages     :@irq0:

-   hourly audio messages
-   web gui?
-   clojure + quarz scheduler?

Implementation:
cronjob + amqp-tools + mp3 files

mp3 files found on cube..

### TEST presence: eta login     :@irq0:

Commands: !ul, !eta, !login, !logout
-   cmd exchange consumer/producer
-   store login, eta state somewhere

Implemented:

### OPEN guess commands     :c3po:

-   see `thomas.py`, `pr.py` auf cube

-   aus normalem text informationen gewinnen
-   In etwa "mach mal licht an" -> "cmd bulb on"

### OPEN hubelmeter     :c3po:

### OPEN shutdown/startup

### user authentication

-   irc nick <-> subraum LDAP?
-   ueberhaupt noetig?

1.  ASSIGNED irc bot antwortet nur auf op     :@irq0:

    -   bot: only answer to users having op? (TODO)

### OPEN big red button

-   hardware button loest 'bigredbutton' command aus?

### DONE text to speech command     :@irq0:

-   listen for tts, say, fortune commands
-   text to speech messages
-   put mp3 files in notify exchange with key audio

Actually two implementations. One pico2wave in the EDI repo and one
based on the old acapella-group web scripting.

### DONE irc bot     :@irq0:

-   IRC receive -> msg exchange with key irc.recv.raw
-   msg exchange with key irc.send.raw -> IRC send

### Notify sink

1.  text

    `routing_key=text` messages.

    1.  DONE libnotify sink     :@irq0:

    2.  OPEN text notifications on projector

2.  audio

    `routing_key=audio` messages.

    1.  DONE mplayer sink     :@irq0:

        shell one-liner with amqp-tools

3.  OPEN uri

    `routing_key=uri` messages.

    Idea: Play media URIs in messages. Sinilar to the mplayer listener on cube.

### DONE 433MHz actor     :@irq0:

`act_433mhz` exchange
-   consumer on raspberrypi
-   message payload = commandline arguments to rcswitch tool

### OPEN jabber bot

-   user same msg exchange as irc bot

-   Possible routing keys: "jabber.recv.raw" "jabber.send.raw"

### OPEN mail bot

-   wie jabber bot nur ueber email
-   nuetzlich auch fuer den notify: user service
-   unauthenticated mail?!

### OPEN dmx actor     :c3po:

See `cube:/var/git/c3po/dmx`. DMX is connected to the serial port.

Example code:

    [2014-02-06 13:45:04] less dmx-disable.py

     #!/usr/bin/python

     import sys
     import serial

     ser = serial.Serial('/dev/dmx', 38400, timeout=1)

     ser.write("B1")

     ser.close()

There is also a dmx jsonrpc server:
`cube:/var/git/c3po/jsonrpcdmx`

### ASSIGNED actor service     :@irq0:

currently a simple python script to map things like 'act bulb on' to
messages on the `act_433_mhz` queue

Idealy something with a rule engine:

-   First user logged in: initiate startup sequence.
-   Last user log out initiate

In the basic incarnation:
Map 'act' messages to actors. *act* messages are something a user
can grasp, e.g *act venti on*. actors are something specific having
their own actor exchanges, e.g *act<sub>433</sub><sub>mhz</sub>* where messages contain
the commands for the sender as payload.

### ASSIGNED openhab integration     :@snowball:

### OPEN irc reader

1.  assign voices to each participant

    1.  parameters

        -   speed
        -   pitch
        -   voice: lea, julia, kenny&#x2026;

2.  participants can change voices

## Architecture Changes

### OPEN list, help messages for 'cmd' exchange

Everyone on the cmd exchange should consume list and help messages.

1.  Replies

    -   **help:** If "args" = "$0" : Reply with brief usage and supported commands
    -   **list:** Reply with something like "I exist and my name is"

2.  Destination

        (str/replace (:src msg) #"recv" "send")

### IDEA state change exchange?

Ohne globalen state müssen state veränderungen irgendwie kommuniziert
werden. Beispiel: user loggt sich ein.

Beispiel:

-   user loggt sich ein
-   tts begrüssung triggern
-   rule engine wertet systemzustand aus

Mögliche umsetzung
*st* exchange. User presence manager sendet message mit "userloggedin"
oder so an den exchange.

Ein event->tts consumer generiert tts commands wenn nötig

Die rule engine verändert ihren systemzustand und wertet rules neu aus.
