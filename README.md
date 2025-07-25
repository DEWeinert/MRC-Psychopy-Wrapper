# MRC-Psychopy-Wrapper
This Wrapper allows to use the MRC Eyetracking software for MRCHiSpeed-MRI Eyetracking cameras with Psychopy. Tested for Psychopy 2024.1.5.

The wrapper also adds some additional basic functions: calibrate(), start_recording(), stop_recording() and send_message(), though all but calibrate() are essentially renamings of existing MRC functions (which are also still callable).

Import instruction:
To import this wrapper ensure that the MRCEyetracking.dll is stored in the "DLL_1_5_3" folder within the same directory of the experiment (or adjust the dll_path variable accordingly) and place the mrc_eyetracker.py in the same folder as the experiment (or adjust the from line in the code component)
Use a code-component at the start of the experiment like this:
    import os
    from mrc_eyetracker import MRCEyeTracking
    eyetracker = MRCEyeTracking(dll_path)
    dll_path = os.path.abspath("DLL_1_5_3/MRC_Eyetracking.dll")
    
Then all further calls of the functions can be made via e.g. eyetracker.eye_connect() or eyetracker.calibrate(win = win). All functions work with units set to pixel only and need adjustment otherwise as the software measures in pixel.

Tested for Psychopy v. 2024.1.5
Created by Daniel Weinert https://github.com/DEWeinert https://www.researchgate.net/profile/Daniel-Weinert
