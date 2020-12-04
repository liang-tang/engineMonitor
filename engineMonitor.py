import PySimpleGUI as sg
import serial
import serial.tools.list_ports
import time

# layout = [[sg.Text('My one-shot window.')],
#          [sg.InputText(key='-IN-')],
#          [sg.Text('Row 2'), sg.Checkbox('box 1', sg.OK())],
#          [sg.Submit(), sg.Cancel()]]

# window = sg.Window('Window Title', layout)

# event, values = window.read()
# window.close()

# text_input = values['-IN-']
# sg.popup('You entered', text_input)

Com_Dict = {}
port_list = list(serial.tools.list_ports.comports())
# for port in port_list:
#     sg.Print(port, do_not_reroute_stdout=False)

sg.theme('BluePurple')

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Text('发动机功率:'), sg.Text(size=(15,1), key='-POWER-'),
          sg.Text('发动机转速:'), sg.Text(size=(15,1), key='-RPM-'),
          sg.Text('发动机温度:'), sg.Text(size=(15,1), key='-TEMP-')],
          [sg.Input(key='-IN-')],
          [sg.Combo(port_list)],
          [sg.Combo(['11', '22', '33'])],
          [sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 1))],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('发动机监控仪', layout)

val = 1
while True:  # Event Loop
    event, values = window.read(timeout=1)
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Show':
        # Update the "output" text element to be the value of "input" element
        window['-OUTPUT-'].update(values['-IN-'])

    str_line = str(val) + " ℃"
    window['-TEMP-'].update(str_line)
    str_line = str(val) + " W"
    window['-POWER-'].update(str_line)
    str_line = str(val) + " RPM"
    window['-RPM-'].update(str_line)
    val += 1
    time.sleep(0.01)

window.close()
