import PySimpleGUI as sg
import serial
import serial.tools.list_ports
import time

Com_Dict = {}
port_list = list(serial.tools.list_ports.comports())
port_list_name = []
if len(port_list) > 0:
    for each_port in port_list:
      port_list_name.append(each_port[0])

# 发动机转速 Engine Speed                   r/min
# 发动机油耗 Fuel Flow Rate                 L/h
# 排气口气压 Manifold Air Pressure          hPa
# 润滑油油压 Oil Pressure,Absolute          hPa
# 润滑油温度 Oil Temperature                K
# 冷却液温度 Coolant Temperature            K

# 气缸1温度  EGT Cylinder 1                 K
# 气缸2温度  EGT Cylinder 2                 K
# 气缸3温度  EGT Cylinder 3                 K
# 气缸4温度  EGT Cylinder 4                 K
# 排气口气温 Manifold Air Temperature       K
# 发动机环温 Engine Ambient Temperature     K

# 油门位置   Throttle Position              %
# 发动机环压 Engine Ambient Pressure        hPa

# ECU总线电压 ECU Bus Voltage               V
# 润滑油补偿油压 Oil Pressure Compensated   hPa

sg.theme('BluePurple')

layout = [[
            sg.Text('发动机转速:', size=(10,1)), sg.Text(size=(10,1), key='-SPEED-'),
            sg.Text('发动机油耗:', size=(10,1)), sg.Text(size=(10,1), key='-FLOW-'),
            sg.Text('发动机环温:', size=(10,1)), sg.Text(size=(10,1), key='-EAT-'),
            sg.Text('发动机环压:', size=(10,1)), sg.Text(size=(10,1), key='-EAP-')
          ],
          [
            sg.Text('润滑油油压:', size=(10,1)), sg.Text(size=(10,1), key='-OP-'),
            sg.Text('润滑油温度:', size=(10,1)), sg.Text(size=(10,1), key='-OT-'),
            sg.Text('补偿油压:', size=(10,1)), sg.Text(size=(10,1), key='-OPC-'),
            sg.Text('冷却液温度:', size=(10,1)), sg.Text(size=(10,1), key='-CT-')
          ],
          [
            sg.Text('气缸1温度:', size=(10,1)), sg.Text(size=(10,1), key='-EGTC1-'),
            sg.Text('气缸2温度:', size=(10,1)), sg.Text(size=(10,1), key='-EGTC2-'),
            sg.Text('气缸3温度:', size=(10,1)), sg.Text(size=(10,1), key='-EGTC3-'),
            sg.Text('气缸4温度:', size=(10,1)), sg.Text(size=(10,1), key='-EGTC4-')
          ],
          [
            sg.Text('油门位置:', size=(10,1)), sg.Text(size=(10,1), key='-THR-'),
            sg.Text('排气口气温:', size=(10,1)), sg.Text(size=(10,1), key='-MAT-'),
            sg.Text('排气口气压:', size=(10,1)), sg.Text(size=(10,1), key='-MAP-'),
            sg.Text('ECU电压:', size=(10,1)), sg.Text(size=(10,1), key='-EBV-')
          ],
          [sg.OptionMenu(port_list_name, key='PORT'), sg.Button('Open')],
          [sg.Button('Exit')]]

window = sg.Window('发动机监控仪', layout)

val = 1
ser = None
input_data = []
while True:  # Event Loop
  event, values = window.read(timeout=1)
  #print(event, values)
  if event == sg.WIN_CLOSED or event == 'Exit':
    if ser != None and ser.is_open:
      ser.close()
    break

  if event == 'Open':
    if ser != None and ser.is_open:
      window.Element('Open').Update('Open')
      ser.close()
      ser = None
    else:
      ser = serial.Serial(values['PORT'], 115200)
      if ser != None and ser.is_open:
        window.Element('Open').Update('Close')

  if ser != None and ser.is_open:
    s = ser.read()
    if len(s) == 1:
      input_data.append(s)
    if len(input_data) == 9:
      input_data.clear()

  if val % 50 == 0 and ser != None and ser.is_open:
    resule = ser.write("Hello from Pyserial\n".encode("utf-8"))

  str_line = str(val) + " r/min"
  window['-SPEED-'].update(str_line)
  str_line = str(val) + " L/h"
  window['-FLOW-'].update(str_line)
  str_line = str(val) + " K"
  window['-EAT-'].update(str_line)
  str_line = str(val) + " hPa"
  window['-EAP-'].update(str_line)

  str_line = str(val) + " hPa"
  window['-OP-'].update(str_line)
  str_line = str(val) + " K"
  window['-OT-'].update(str_line)
  str_line = str(val) + " hPa"
  window['-OPC-'].update(str_line)
  str_line = str(val) + " K"
  window['-CT-'].update(str_line)

  str_line = str(val) + " K"
  window['-EGTC1-'].update(str_line)
  str_line = str(val) + " K"
  window['-EGTC2-'].update(str_line)
  str_line = str(val) + " K"
  window['-EGTC3-'].update(str_line)
  str_line = str(val) + " K"
  window['-EGTC4-'].update(str_line)

  str_line = str(val) + " %"
  window['-THR-'].update(str_line)
  str_line = str(val) + " K"
  window['-MAT-'].update(str_line)
  str_line = str(val) + " hPa"
  window['-MAP-'].update(str_line)
  str_line = str(val) + " V"
  window['-EBV-'].update(str_line)

  val += 1
  time.sleep(0.01)

window.close()
