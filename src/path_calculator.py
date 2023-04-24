from sheet_analyzer import analyze_sheet
from metallophone import Keyboard
from movements import Movement_chain

if __name__ == "__main__":
    img_path = "sheets/himne_alegria_small.png"
    partiture = analyze_sheet(img_path)

    kb = Keyboard(partiture)
    movements = kb.distribuite_movements()

    chain = Movement_chain(movements)
    chain.print_movement_chain()

    print("Done")

 
