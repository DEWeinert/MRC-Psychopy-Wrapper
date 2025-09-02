'''
This wrapper allows to use the MRC eyetracking software for the MRC Hi-Speed Camera in Psychopy via the MRC_Eyetracking.dll.
It also adds some additional basic functions: calibrate(), start_recording(), stop_recording() and send_message(), though all but calibrate() are essentially renamings of existing MRC functions (which are also still callable)
To import this wrapper ensure that the MRCEyetracking.dll is stored in the "DLL_1_5_3" folder within the same directory of the experiment (or adjust the dll_path variable accordingly)
Use a code-component at the start of the experiment like this:
    import os
    from mrc_eyetracker import MRCEyeTracking
    eyetracker = MRCEyeTracking(dll_path)
    dll_path = os.path.abspath("DLL_1_5_3/MRC_Eyetracking.dll")
    
Then all further calls of the functions can be made via e.g. eyetracker.eye_connect() or eyetracker.calibrate(win = win). All functions work with units set to pixel only and need adjustment otherwise as the software measures in pixel.

Tested for Psychopy v. 2024.1.5
Created by Daniel Weinert https://github.com/DEWeinert https://www.researchgate.net/profile/Daniel-Weinert
'''
import ctypes
from ctypes import c_int, c_double, c_char_p, POINTER, byref, Structure,c_bool
import psychopy
from psychopy import visual, core, event, colors,hardware
from psychopy.hardware import keyboard
from psychopy.hardware import DeviceManager


class EyeEvent(Structure):
    _fields_ = [
        ("eye", c_int),
        ("event_type", c_int),
        ("timestamp", c_double),
        ("event_text", ctypes.c_char * 256),
        ("param1", c_double),
        ("param2", c_double),
        ("param3", c_double),
        ("param4", c_double),
        ("param5", c_double),
    ]

class MRCEyeTracking:
    
    def __init__(self, dll_path="MRC_Eyetracking.dll"):
        self.deviceManager = DeviceManager
        if self.deviceManager.getDevice('MRC_keyboard') is None:
            self.MRC_keyboard = self.deviceManager.addDevice(
                deviceClass='keyboard',
                deviceName='MRC_keyboard',
            )
        else:
            self.MRC_keyboard = self.deviceManager.getDevice('MRC_keyboard')
            
        
        self.lib = ctypes.WinDLL(dll_path)

        self.lib.eye_connect.argtypes = [c_char_p, c_int]
        self.lib.eye_connect.restype = c_bool

        self.lib.eye_disconnect.argtypes = []
        self.lib.eye_disconnect.restype = c_bool

        self.lib.eye_get_calibration_point.argtypes = [POINTER(c_double)]
        self.lib.eye_get_calibration_point.restype = None

        self.lib.eye_get_calibstate.argtypes = [POINTER(c_double)]
        self.lib.eye_get_calibstate.restype = None

        self.lib.eye_get_events_count.argtypes = [POINTER(c_int)]
        self.lib.eye_get_events_count.restype = None

        self.lib.eye_get_gaze.argtypes = [POINTER(c_double)]
        self.lib.eye_get_gaze.restype = None

        self.lib.eye_get_last_error.argtypes = []
        self.lib.eye_get_last_error.restype = c_char_p

        self.lib.eye_get_parameter.argtypes = [c_char_p, POINTER(c_double)]
        self.lib.eye_get_parameter.restype = c_bool

        self.lib.eye_get_pupil_size.argtypes = [POINTER(c_double)]
        self.lib.eye_get_pupil_size.restype = None

        self.lib.eye_get_status.argtypes = [POINTER(c_int)]
        self.lib.eye_get_status.restype = c_bool

        self.lib.eye_get_timestamp.argtypes = [POINTER(c_double)]
        self.lib.eye_get_timestamp.restype = None

        self.lib.eye_get_version.argtypes = []
        self.lib.eye_get_version.restype = c_char_p

        self.lib.eye_select_camera.argtypes = [c_int]
        self.lib.eye_select_camera.restype = c_bool

        self.lib.eye_set_display_offset.argtypes = [c_int, c_int]
        self.lib.eye_set_display_offset.restype = c_bool

        self.lib.eye_set_display_parameter.argtypes = [c_int, c_int, c_int, c_double]
        self.lib.eye_set_display_parameter.restype = c_bool

        self.lib.eye_set_displaymode.argtypes = [c_int, c_int]
        self.lib.eye_set_displaymode.restype = c_bool

        self.lib.eye_set_parameter.argtypes = [c_char_p, c_char_p]
        self.lib.eye_set_parameter.restype = c_bool

        self.lib.eye_set_software_event.argtypes = [c_char_p]
        self.lib.eye_set_software_event.restype = c_int

        self.lib.eye_start_calibrate.argtypes = [c_int]
        self.lib.eye_start_calibrate.restype = c_bool

        self.lib.eye_start_stream.argtypes = [c_int]
        self.lib.eye_start_stream.restype = c_bool

        self.lib.eye_start_video_recording.argtypes = []
        self.lib.eye_start_video_recording.restype = c_bool

        self.lib.eye_stop_calibration.argtypes = []
        self.lib.eye_stop_calibration.restype = c_bool

        self.lib.eye_stop_stream.argtypes = []
        self.lib.eye_stop_stream.restype = c_bool

        self.lib.eye_stop_video_recording.argtypes = []
        self.lib.eye_stop_video_recording.restype = c_bool

        self.lib.eye_get_events_matlab.argtypes = [POINTER(c_int)]
        self.lib.eye_get_events_matlab.restype = POINTER(EyeEvent)

    def eye_connect(self, ip: str, port: int) -> int:
        return self.lib.eye_connect(ip.encode('utf-8'), port)

    def eye_disconnect(self) -> int:
        return self.lib.eye_disconnect()

    def eye_get_calibration_point(self):
        data = (c_double * 3)()
        self.lib.eye_get_calibration_point(data)
        return list(data)

    def eye_get_calibstate(self):
        data = (c_double * 2)()
        self.lib.eye_get_calibstate(data)
        return list(data)

    def eye_get_events(self, count: int):
        c_count = c_int(count)
        events = []
        for _ in range(count):
            ptr = self.lib.eye_get_events_matlab(byref(c_count))
            if ptr:
                evt = ptr.contents
                events.append({
                    "eye": evt.eye,
                    "event_type": evt.event_type,
                    "timestamp": evt.timestamp,
                    "event_text": evt.event_text.decode('utf-8'),
                    "param1": evt.param1,
                    "param2": evt.param2,
                    "param3": evt.param3,
                    "param4": evt.param4,
                    "param5": evt.param5,
                })
        return events

    def eye_get_events_count(self) -> int:
        count = c_int(-1)
        self.lib.eye_get_events_count(byref(count))
        return count.value

    def eye_get_gaze(self):
        data = (c_double * 5)()
        self.lib.eye_get_gaze(data)
        return list(data)

    def eye_get_last_error(self) -> str:
        return self.lib.eye_get_last_error().decode('utf-8')

    def eye_get_parameter(self, name: str):
        val = c_double(0.0)
        result = self.lib.eye_get_parameter(name.encode('utf-8'), byref(val))
        return result, val.value

    def eye_get_pupil_size(self):
        data = (c_double * 4)()
        self.lib.eye_get_pupil_size(data)
        return list(data)

    def eye_get_status(self) -> bool:
        status = c_int(-1)
        self.lib.eye_get_status(byref(status))
        return status.value

    def eye_get_timestamp(self) -> float:
        ts = c_double(-1)
        self.lib.eye_get_timestamp(byref(ts))
        return ts.value

    def eye_get_version(self) -> str:
        return self.lib.eye_get_version().decode('utf-8')

    def eye_select_camera(self, eye: int) -> bool:
        return self.lib.eye_select_camera(eye)

    def eye_set_display_offset(self, width_offset: int, height_offset: int) -> bool:
        return self.lib.eye_set_display_offset(width_offset, height_offset)

    def eye_set_display_parameter(self, width: int, height: int, distance: int, pixelsize: float) -> bool:
        return self.lib.eye_set_display_parameter(width, height, distance, pixelsize)

    def eye_set_displaymode(self, width: int, height: int) -> bool:
        print(width,height)
        return self.lib.eye_set_displaymode(width, height)

    def eye_set_parameter(self, name: str, value: str) -> bool:
        return self.lib.eye_set_parameter(name.encode('utf-8'), value.encode('utf-8'))

    def eye_set_software_event(self, value: str) -> bool:
        event_bytes = value.encode('ascii')+b'\x00'
        return self.lib.eye_set_software_event(event_bytes)

    def eye_start_calibrate(self, points: int) -> bool:
        return self.lib.eye_start_calibrate(points)

    def eye_start_stream(self, parameter: int) -> bool:
        return self.lib.eye_start_stream(parameter)

    def eye_start_video_recording(self) -> bool:
        return self.lib.eye_start_video_recording()

    def eye_stop_calibration(self) -> bool:
        return self.lib.eye_stop_calibration()

    def eye_stop_stream(self) -> bool:
        return self.lib.eye_stop_stream()

    def eye_stop_video_recording(self) -> bool:
        return self.lib.eye_stop_video_recording()
        
    #From here on are additional functions created by D.E. Weinert
    
    
    def connect(self, ip = "localhost"):
        self.eye_connect(ip, 5257)
        version = self.eye_get_version()
        print(f"MRC Eye Tracker Version: {version}")
        
    
    def calibrate(self, win, calibration_points = int(9),screen_width = int(1920),screen_height = int(1080),distance_to_screen = int(130), pixel_size = float(0.333),dot_color = [1,1,1], dot_size = float(20), flipped = True):
        #Please set screen_width and height as well as distance to screen and pixel size
        #Calibration is made for a quadratic window equal to the full height of the screen and positioned in the center of the screen. Adjust vertical_goesse and x_displace if nessecary for a not quadratic fixation
        if self.eye_get_status()!= -1:             
            repeat_Text = visual.TextStim(win=win, name='introText', text='Calibration Completed \n    To recalibrate press 5 \n To continue press SPACE', 
                        font='Arial', pos=[0, 0], height=3, wrapWidth=30, ori=0, color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', flipHoriz=flipped, depth=-1.0);
            calibration_Text = visual.TextStim(win=win, name='introText', text='Eyetracker Calibration \n    Focus your sight onto the white dots \n To start press  SPACE \n To abort at any time press Q', 
                        font='Arial', pos=[0, 0], height=3, wrapWidth=30, ori=0, color='white', colorSpace='rgb', opacity=1, languageStyle='LTR', flipHoriz=flipped, depth=-1.0);
            calibration = True
            repeat_calibration = False
            self.win = win
            screen_width = int(screen_width)
            screen_height = int(screen_height)
            tracking_groesse = int(screen_height)
            vertical_groesse = int(tracking_groesse) #if the presentation window region of interest is not quadratic, adjust the x-coordinate here
            x_displace = int(((screen_width-vertical_groesse)/2)-8) #the -8 represent the number of pixels of the windows window vertical border.
            y_displace = int(-30) #the -30 ensure that the top part of the windows window are not interfering with localisation. Adjust depending on the thickness of your windows top-bars or if using a different operating system
            dot_color = dot_color
            dot_size = float(dot_size)
            self.eye_set_display_parameter(vertical_groesse, tracking_groesse, distance_to_screen, pixel_size)  # width, height, distance, pixel size
            self.eye_set_display_offset(x_displace, y_displace) #this variable places the presentation window of the software and defines the area in which recording takes place
            print(x_displace,y_displace)
            if self.eye_get_status() != 2:
                calibration_message = True
            self.MRC_keyboard.clearEvents()
            while calibration_message
                cancel_key = self.MRC_keyboard.getKeys(keyList = ["q","escape"], waitRelease = False)
                continue_key = self.MRC_keyboard.getKeys(keyList = ["space"], waitRelease = False)
                if cancel_key: 
                    calibration = False
                    calibration_message = False
                    break
                if continue_key:
                    print("starting calibration")
                    calibration_message = False
                calibration_Text.draw()
                win.flip()
            while calibration:
                calibration_running = False
                print(self.eye_get_status())
                if self.eye_get_status() != 2 or repeat_calibration:
                    self.eye_start_stream(0)
                    self.eye_start_calibrate(calibration_points)
                    calibration_running = True
                    repeat_calibration = False

                point = [0,0,0]
                self.MRC_keyboard.clearEvents()

                while calibration_running == True:
                    cancel_key = self.MRC_keyboard.getKeys(keyList = ["q","escape"], waitRelease = False)
                    if cancel_key: 
                        print("Calibration aborted")
                        self.eye_stop_calibration()
                        self.eye_stop_stream()
                        calibration = False
                        break
                    if self.eye_get_status() == 2:
                        print("calibration done")
                        self.eye_stop_calibration()
                        calibration_running = False
                        self.eye_stop_stream()
                    point = self.eye_get_calibration_point()
                    stimulus = visual.Circle(win=win, radius=dot_size / 2, fillColor=dot_color, lineColor=dot_color, pos=(point[1]-tracking_groesse/2, tracking_groesse/2-point[2]))
                    stimulus.draw()
                    win.flip()
                if self.eye_get_status() == 2:
                    self.MRC_keyboard.clearEvents()
                    repeat_message = True
                    while repeat_message and not repeat_calibration:
                        cancel_key = self.MRC_keyboard.getKeys(keyList = ["q","escape", "space"], waitRelease = False)
                        repeat_key = self.MRC_keyboard.getKeys(keyList = ["5"], waitRelease = False)
                        if cancel_key: 
                            self.eye_stop_calibration()
                            self.eye_stop_stream()
                            calibration = False
                            repeat_message = False
                            break
                        if repeat_key:
                            print("repeating calibration")
                            repeat_calibration = True
                        repeat_Text.draw()
                        win.flip()                                      
        else:
            print("error. Eyetracker not connected?")
    def start_recording(self):
        self.eye_set_parameter('eye_save_tracking', 'true')
    def stop_recording(self): 
        self.eye_set_parameter('eye_save_tracking', 'false')
    def send_message(self, msg):
        self.eye_set_software_event(msg)

