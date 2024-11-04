# Define the images

define a = Character("Arisu")
define custom_center = Position(xalign=0.5, yalign=0.5)

image bg room = "room_background.png"
image button_normal = "item_idle.png"
image button_hovered = "item_hover.png"
image door_closed = "item_idle.png"
image door_open = "item_hover.png"
image item1 = "item_idle.png"
image item1h = "item_hover.png"
image item2 = "item_idle.png"
image item2h = "item_hover.png"
image item3 = "item_idle.png"
image item3h = "item_hover.png"
image arrow_right = "arrow_right.png"
image minimap = "minimap.png"
image you = "you.png"

image arisu_normal = "arisu_normal.png"
image arisu_mad = "arisu_mad.png"


# Define inventory as a list of dictionaries, each holding item information
default inventory = []
default selected_item = None

init python:
    # Function to add a new item to the inventory
    def add_item(name, description):
        # Check if item already exists, update if it does
        for item in inventory:
            if item['name'] == name:
                item['description'] = description
                return
        # If item doesn't exist, add it to the inventory
        inventory.append({'name': name, 'description': description})
    # remove item from inventory
    def remove_item(name):
        for item in inventory:
            if item['name'] == name:
                inventory.remove(item)
                return


    # Function to update item description
    def update_item_description(name, new_description):
        for item in inventory:
            if item['name'] == name:
                item['description'] = new_description
                return
                
# Define the variables to track state
default observed_object = False
default door_opened = False
default item1_clicked = False
default item2_clicked = False
default item3_clicked = False

# Start label
label start:
    #mở đầu
    scene black with fade
    window hide

    $ ui.clear()

    show text "Butterfly, is a beautiful creature, isn't it?" at truecenter with fade
    pause 2

    hide text with fade
    pause 1

    show text "But it is cruel sometime..." at truecenter with dissolve
    pause 2

    hide text with fade
    pause 1

    #vô màn
    $ add_item("Talisman 1", "A talisman representing your lives left. If you run out, you die.")
    $ add_item("Talisman 2", "A talisman representing your lives left. If you run out, you die.")
    $ add_item("Talisman 3", "A talisman representing your lives left. If you run out, you die.")
    
    scene bg room

    show arisu_normal at custom_center

    a "Hi! I'm Takamine Arisu."
    a "Let travel together shall we?"

    show arisu_mad at custom_center

    a "What?! You don't want to?"
    a "I'll kick your ass off."

    scene bg room with dissolve

    "Run!"


    show minimap:
     zoom 0.7
     xpos 1400
     ypos 0
 
    show you:
     zoom 0.3
     xpos 1500
     ypos 60
    # Display the room with interactive objects
    call screen room_screen

    
    return

# Define the room screen with interactive buttons
screen room_screen():
    # ImageButton for observing an object
    imagebutton:
        idle "button_normal"
        hover "button_hovered"
        xpos 900 ypos 400
        action [Function(observe_object), Show("room_screen")]

    # ImageButton for item1
    imagebutton:
        idle "item1"
        hover "item1h"
        xpos 300 ypos 600
        action [SetVariable("item1_clicked", True), Function(check_puzzle), Show("room_screen")]

    # ImageButton for item2
    imagebutton:
        idle "item2"
        hover "item2h"
        xpos 500 ypos 400
        action [SetVariable("item2_clicked", True), Function(check_puzzle), Show("room_screen")]

    # ImageButton for item3
    imagebutton:
        idle "item3"
        hover "item3h"
        xpos 650 ypos 750
        action [SetVariable("item3_clicked", True), Function(uplife), Show("room_screen")]

    # ImageButton for the arrow to the next room, only visible when the door is opened
    if door_opened:
        imagebutton:
            idle "arrow_right"
            hover "arrow_right"
            xpos 1600 ypos 400
            action [Jump("next_room")]

# Function to observe an object
init python:
    def observe_object():
        if not observed_object:
            renpy.call_in_new_context("observe_first_time")
        else:
            renpy.call_in_new_context("observe_again")

# Define labels for dialogue
label observe_first_time:
    $ observed_object = True
    "You see a strange plant."
    return

label observe_again:
    "You've already observed this plant. (Description changing ability)"
    return

# Check if the puzzle is solved
init python:
    def check_puzzle():
        if item1_clicked and item2_clicked:
            renpy.call_in_new_context("open_door")
        else:
            renpy.call_in_new_context("door_still_closed")

init python:
    def uplife():
        renpy.call_in_new_context("up_life")

# Define labels for door states
label open_door:
    $ door_opened = True
    show key with dissolve:
     yalign 0.2
     xalign 0.5
    $ add_item("Key", "A key to the locked door.")
    $ add_entry ("You found a key.")
    $ add_entry ("You unlocked the door.")
    "You found a Key. You try it on the door. The door is now open!"
    hide key with dissolve
    $ remove_item("Key")
    $ remove_item("Code")
    return

label up_life:
    show talisman with dissolve:
     yalign 0.2
     xalign 0.5
    "You found a talisman."
    $ add_entry("You found a talisman.")
    $ add_item("Talisman 4", "A talisman representing your lives left. If you run out, you die.")
    "Life increased."
    hide talisman with dissolve
    return

label door_still_closed:
    show code with dissolve:
     yalign 0.2
     xalign 0.5
    $ add_item("Code", "A code to the locked door. It needs a key as well.")
    $ add_entry("You found a code for the door, but it's still locked.")
    "You collect a Code. The door is still closed. Maybe it needs something else?"
    hide code with dissolve
    return
label next_room:
 scene room_background with fade
 show minimap:
     zoom 0.7
     xpos 1400
     ypos 0
 "Welcome to the next room."
 show you:
     zoom 0.3
     xpos 1700
     ypos 60
 call screen next_room_screen
 
# Define the next room screen
screen next_room_screen():
    # You can add the background and interactive elements for the next room here
     # ImageButton for item1
    imagebutton:
        idle "item1"
        hover "item1h"
        xpos 1200 ypos 300
        action [Jump("timed_choice")]

label timed_choice:
 show mask with dissolve:
     yalign 0.2
     xalign 0.5
 "You find a weird object. It looks dangerous."
 hide mask with dissolve
 call screen timed_choice

screen timed_choice:

    # Set the timer for 5 seconds
    timer 5.0 action [Hide("timed_choice"), Jump("Uhoh")]

    # Display the choice menu
    vbox:
        align (0.5, 0.5)
        spacing 10

        text "What will you do?"

        # Visual representation of the timer
        frame:
            xmaximum 300
            ymaximum 20
            has hbox

            # Background for the bar
            bar:
                value 1.0
                range 1.0
                xmaximum 300
                ymaximum 20
                # Animate the width of the bar
                at countdown_bar

        # Choice 1
        textbutton "Put it down carefully" action [Hide("timed_choice"), Jump("option_1")]

        # Choice 2
        textbutton "Throw it out the window" action [Hide("timed_choice"), Jump("option_2")]

# Define the countdown bar transform
transform countdown_bar:
    linear 5.0 xzoom 0.0

label Uhoh:
    "Wait - What's happening?!"
    scene black with fade
    "It exploded."
    $ remove_item("Talisman 4")
    "One of your talisman shatter."
    

# Define the outcomes of the choices
label option_1:
    "You put it down carefully. Nothing happens."
    return

label option_2:
    "You throw it out the window. Soon after, it explodes."
    return