import cv2
import sys
import time

from src.sheet_analyzer import analyze_sheet
from src.metallophone import Keyboard
from src.movements import Movement_chain
from src.arduino_comunication import ArduinoComunication



if __name__ == '__main__':
    # Deal with arguments
    sheet = None
    display = False
    paralelize = False
    mode = "bulk"
    reference = False 

    if len(sys.argv) > 1:
        opts = [opt for opt in sys.argv[1:] if opt.startswith("-")]
        args = [arg for arg in sys.argv[1:] if not arg.startswith("-")]
        all = sys.argv[1:]

        ############# Arguments #############
        # -s: sheet
        # -d: display graphs
        # -p: paralelize
        # -mode: mode (streaming/bulk)
        # -r: reference image
        # -h/-help: explain options
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

        if ("-h" in opts) or ("-help" in opts):
            print("Arguments available:")
            print("\t -s [sheet_name]:\t specify local sheet in the project to play (this option does not take a picture with the camera). [default = disabled]")
            print("\t -d:\t\t\t show intermediate results and processes calculations. [default = disabled]")
            print("\t -p:\t\t\t paralelizes analyze process (this option shows less information if combined with 'display'). [default = disabled]")
            print("\t -mode [bulk/streaming]: choose between a bulk transfer of data to the arduino or a streaming one. [default = bulk]")
            print("\t -r:\t\t\t disables the standardization of the image. Used when a specified sheet is given. [defualt = disabled]")
            print("\n")
            exit()


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

    # Take picture
    if sheet is None:
        from src.camera import take_picture
        print("Taking picture...")
        take_picture()
        sheet = "photo_sheet.jpg"
        print("Picture taken!")
        
    # Read sheet
    img = cv2.imread(sheet)

    if reference:
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        from src.partiture_std import partiure_std
        # Standardize the sheet
        img_gray = partiure_std(img)
        img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)

    start = time.time()

    # Analyze the sheet
    partiture = analyze_sheet(img_gray, img, display, paralelize)
    
    # Get the movements
    print("Distributing movements...")
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



