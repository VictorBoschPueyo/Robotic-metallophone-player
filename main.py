import cv2
import sys
import time

from src.partiture_std import partiure_std
from src.sheet_analyzer import analyze_sheet
from src.metallophone import Keyboard
from src.movements import Movement_chain
from src.arduino_comunication import ArduinoComunication
from src.camera import take_picture



if __name__ == '__main__':
    # Deal with arguments
    sheet = None
    display = False
    paralelize = False
    mode = "bulk"
    reference = False 

    if len(sys.argv) > 2:
        opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
        args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
        all = sys.argv[1:]

        ############# Arguments #############
        # -s: sheet
        # -d: display graphs
        # -p: paralelize
        # -mode: mode (streaming/bulk)
        # -r: reference image
        #####################################

        if "-s" in opts:
            sheet = "sheets/" + all[all.index("-s") + 1]
 
        if "-d" in opts:
            display = True

        if "-p" in opts:
            paralelize = True

        if "-mode" in opts:
            mode = all[all.index("-mode") + 1]

        if "-r" in opts:
            reference = True

    print("Arguments:")
    print("--Sheet: \t", sheet)
    print("--Display: \t", display)
    print("--Paralelize: \t", paralelize)
    print("--Mode: \t", mode)
    print("--Reference: \t", reference)
    print("----------------------\n")

    ##################
    ## MAIN PROGRAM ##
    ##################
    start = time.time()

    # Take picture
    if sheet is None:
        take_picture()
        sheet = "sheets/img.jpg"
        
    # Read sheet
    img = cv2.imread(sheet)

    if reference:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        # Standardize the sheet
        img = partiure_std(img)

    # Analyze the sheet
    partiture = analyze_sheet(img, img, display, paralelize)

    # Get the movements
    kb = Keyboard(partiture)
    movements = kb.distribuite_movements(display)

    # Distribuite the movements
    moves = Movement_chain(movements)


    print("Algorithm time: ", time.time() - start)

    # Send the data to the arduino
    arduino = ArduinoComunication("/dev/ttyUSB0", 9600)

    if mode == "streaming":
        arduino.send_move_by_move(moves.data)
    else:
        arduino.send_full_data(moves.data)



