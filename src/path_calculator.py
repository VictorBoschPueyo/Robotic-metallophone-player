from sheet_analyzer import analyze_sheet
from metallophone import Key, Keyboard

if __name__ == "__main__":
    img_path = "sheets/himne_alegria.png"
    partiture = analyze_sheet(img_path)

    kb = Keyboard(partiture)
    kb.print_keyboard()

    print("Done")
