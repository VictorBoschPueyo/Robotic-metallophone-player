from sheet_analyzer import analyze_sheet
from metallophone import Keyboard
from movements import Movement_chain
from arduino_comunication import ArduinoComunication

if __name__ == "__main__":
    img_path = "sheets/himne_alegria.png"
    partiture = analyze_sheet(img_path)

    kb = Keyboard(partiture)
    movements = kb.distribuite_movements()

    moves = Movement_chain(movements)

    #arduino = ArduinoComunication("/dev/ttyUSB0", 9600)

    #arduino.send_full_data(moves.data)

    print("Done")
