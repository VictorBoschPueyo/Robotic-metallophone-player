import cv2
import sys
import time

from src.partiture_std import partiure_std
from src.sheet_analyzer import analyze_sheet
from src.metallophone import Keyboard
from src.movements import Movement_chain
from src.arduino_comunication import ArduinoComunication



if __name__ == '__main__':
    # Deal with arguments
    if len(sys.argv) > 2:
        opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
        args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
        all = sys.argv[1:]

        ############# Arguments #############
        # -s: sheet
        # -d: display graphs
        # -p: paralelize
        # -mode: mode (streaming/bulk)
        #####################################

        if "-s" in opts:
            sheet = "sheets/" + all[all.index("-s") + 1]
        else:
            sheet = "sheets/foto_himne_alegria.jpg"

        if "-d" in opts:
            display = True
        else:
            display = False

        if "-p" in opts:
            paralelize = True
        else:
            paralelize = False

        if "-mode" in opts:
            mode = all[all.index("-mode") + 1]
        else:
            mode = "bulk"

    print("Arguments:")
    print("--Sheet: ", sheet)
    print("--Display: ", display)
    print("--Paralelize: ", paralelize)
    print("--Mode: ", mode)

    ##################
    ## MAIN PROGRAM ##
    ##################
    start = time.time()
    # Read sheet
    img = cv2.imread(sheet)

    # Standardize the sheet
    img_std = partiure_std(img)

    # Analyze the sheet
    partiture = analyze_sheet(img_std, img, display)

    # Get the movements
    kb = Keyboard(partiture)
    movements = kb.distribuite_movements(display)

    # Distribuite the movements
    moves = Movement_chain(movements)


    # Send the data to the arduino
    '''arduino = ArduinoComunication("/dev/ttyUSB0", 9600)

    if mode == "streaming":
        arduino.send_move_by_move(moves.data)
    else:
        arduino.send_full_data(moves.data)'''

    print("Time: ", time.time() - start)



