from os import getlogin
from tkinter import EventType
from tkinter.constants import OFF
import PySimpleGUI as sg
import pyperclip
from PySimpleGUI.PySimpleGUI import OFFICIAL_PYSIMPLEGUI_BUTTON_COLOR, WIN_CLOSED, ColorChooserButton, ObjToStringSingleObj, Window, main

# App theme
sg.theme('Dark Brown')

# Main variables
Rows = 0
Column = 0
color_storage = 'clor'
code_list = []
new_line = '\n'
final_code = 'Your code will be displayed here..'
demo_code_list = []
reset = False


# To generate button name and keys
def fun(row,col):
    if row == 0:
        return col
    else:
        return (Column*row)+col

# LED number gennerator
def led_number(arguss):
    fresh = (new_line.join(arguss))
    return fresh

# Demo code generator
def generate_demo_code():

    code = (f'''#include <FastLED.h>
#define NUM_LEDS 25
#define DATA_PIN 3
#define CLOCK_PIN 13

CRGB leds[NUM_LEDS];

void setup() {{ 

    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}}

void loop() {{ 

{led_number(demo_code_list)}

}}''')
    return code

# Code generator
def generate_code():

    code = (f'''#include <FastLED.h>
#define NUM_LEDS 25
#define DATA_PIN 3
#define CLOCK_PIN 13

CRGB leds[NUM_LEDS];

void setup() {{ 

    FastLED.addLeds<NEOPIXEL, DATA_PIN>(leds, NUM_LEDS);
}}

void loop() {{ 

{led_number(code_list)}

}}''')
    return code


# Start screen layout
pop_layout = [[[sg.Text('Number of Rows')], [sg.Input(key='-rownum-')]],
                [[sg.Text('Number of Colums')], [sg.Input(key='-colnum-')]],
                [[sg.Text('LED Type')], [sg.Input(key='-ledtype-')]],
                [[sg.Text('one')], [sg.Input()]],
                [[sg.Text('one')], [sg.Input()]],
                [[sg.Text('one')], [sg.Input()]],
                [[sg.Button('OK')]]  ]
pop_window = sg.Window('Color picker', pop_layout)

# Popup color chooser window layout
layout_popup = [[sg.Input('#xxxxxx', key='_COLOR_', size=(10,1)), sg.ColorChooserButton('Choose Color', target='_COLOR_')], [sg.Button('OK'), sg.Button('cancel')]]
window_popup = sg.Window('Color picker', layout_popup)



# Popup for variable collection
def popup_dialoue():
    global Rows,Column
    while True:
        event, values = pop_window.read()
        if event == WIN_CLOSED:
            break
        if event == 'OK':
            rozz = int(values['-rownum-'])
            colz = int(values['-colnum-'])
            Rows = rozz
            Column = colz
            led = values['-ledtype-']
            print (Rows, Column, led)
            for led in range (Rows*Column):
                code_list.append((f'leds[{led}] = CRGB::red;'))
            for led in range (Rows*Column):
                demo_code_list.append((f'leds[{led}] = CRGB::black;'))
            pop_window.close()
            main_window(rozz, colz)



# Main window
def main_window(Rows, Column):
    global code_list, final_code, reset
    # Main window layout
    matrix_layout = [[[sg.Button(f'{fun(row,col)}', key=f'{fun(row,col)}', button_color='black', size=(1,1), pad=0) for col in range (Column)] for row in range (Rows)], 
    [sg.Checkbox('Sequential'), sg.Text('Delay:'), sg.Input(size = (10,1))],
    [sg.Button('Generate Code'), sg.Button('Reset')]]
    code_layout = [[sg.MLine(f'{final_code}', key='-CODE-', size =(50,20))],
                    [sg.Button('Copy code', key='-copy_btn-')], [sg.Button('Update', key='-update_btn-')]]
    # layout = [[matrix_layout],[code_layout]]
    matrix_window = sg.Window('Matrix', matrix_layout)
    while True:
        event, values = matrix_window.read()
        # matrix_window.refresh()
        print (event,values)
        if event == WIN_CLOSED:
            break
        else:
            for i in range (Rows*Column):
                if event == f'{i}':
                    color_value = sg.popup_get_text('enter color')
                    code_list[i] = f'leds[{i}] = CRGB::{color_value};'
                    print (code_list[i])
                    matrix_window.Element(f'{i}').Update(button_color=color_value)
                    
                elif event == 'Reset':
                    matrix_window.Element(f'{i}').Update(button_color='Black')
                    reset = True
                    #final_code = generate_demo_code()
                    # final_code = demo_code
                    # for i in range (Rows*Column):
                    #code_list.append((f'leds[{i}] = CRGB::Black;'))

                elif event == 'Generate Code':
                    if reset == True:
                        reset = False
                        final_code = generate_demo_code()
                    else:final_code = generate_code()
                    code_wind()
                    break
                    # code_window['-CODE-'].update(final_code)

# Code window
def code_wind():
    global final_code
    # Code window layout
    code_layout = [[sg.MLine(f'{final_code}', key='-CODE-', size =(50,20))],
                    [sg.Button('Copy code')]]
    code_window = sg.Window('Code', code_layout)
    # code_window['-CODE-'].update(final_code)
    while True:
        event, values = code_window.read(timeout=400)
        if event == WIN_CLOSED:
            break
        else:
            if event == 'Copy code':
                pyperclip.copy(final_code)
            else: code_window.refresh()
    code_window.close()


popup_dialoue()