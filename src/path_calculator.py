from sheet_analyzer import analyze_sheet
from metallophone import Keyboard

if __name__ == "__main__":
    img_path = "sheets/himne_alegria_small.png"
    partiture = analyze_sheet(img_path)

    kb = Keyboard(partiture)
    movements = kb.distribuite_movements()

    print("Done")
