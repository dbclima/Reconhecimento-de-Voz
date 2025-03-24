from .mic_selection import MicUi
from .menu import Menu

if __name__ == "__main__":
    mic_ui = MicUi()
    mic_ui.mainloop()
    

    app = Menu(mic_ui.index)
    app.mainloop()