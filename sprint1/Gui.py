'''
Ryan Phillips 
UMKC CS 449 Sprint 1 GUI
Language: Python
GUI Framework: TKinter
sprint0_gui.py
'''
import tkinter as tk
from tkinter import ttk

# currently just the same from sprint 0 will update tommorw to account for new backend game code

'''
For now this is just a basic GUI to mock how to SOS game GUI will look
There is no state handeling in this yet
'''
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Setup Main App Config
        self.title('SOS Game')

        # default to half user screen size and allow resizing and sacling to an adjustable window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{int(screen_width * 0.5)}x{int(screen_height * 0.5)}')
        self.resizable(1, 1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # configure styles
        self.bg_color = "#181818"
        self.board_cell_size = 60
        self.board_line_width = 3
        self.turn_text = ("X's turn to move", "O's turn to move")

        self.style = ttk.Style(self)
        self.style.configure('TLabel', font=('Helvetica', 22))
        self.style.configure('TEntry', font=('Helvetica', 32))
        self.style.configure('Heading.TLabel', background=self.bg_color, foreground="white", font=('Helvetica', 32))
        self.style.configure('FooterInfo.TLabel', background=self.bg_color, foreground="white", font=('Helvetica', 16))
        self.style.configure("TRadiobutton", font=('Helvetica', 16, 'bold'), foreground='white', background=self.bg_color)
        self.style.configure("TCheckbutton", font=('Helvetica', 16, 'bold'), foreground='white', background=self.bg_color)

        # main parent frame
        self.mainframe = ttk.Frame(self, style="TFrame")
        self.mainframe.grid(column=0, row=0, sticky="nsew")
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=0)
        self.mainframe.columnconfigure(0, weight=1)

        # header frame
        self.header_frame = tk.Frame(self.mainframe, bg=self.bg_color, bd=1, height=100)
        self.header_frame.grid(column=0, row=0, sticky="nsew")
        self.header_frame.pack_propagate(False)

        self.heading = ttk.Label(self.header_frame, text='SOS Game', style='Heading.TLabel').pack(pady=10)

        # main content game frame
        self.main_content_frame = tk.Frame(self.mainframe)
        self.main_content_frame.grid(row=1, column=0, sticky="nsew", pady=6)
        self.main_content_frame.rowconfigure(0, weight=1)
        self.main_content_frame.columnconfigure([0, 1 ,2], weight=1, uniform="cols")

        # left side game frame
        self.leftside_frame = tk.Frame(self.main_content_frame, bg=self.bg_color, bd=1)
        self.leftside_frame.grid(column=0, row=0, sticky="nsew")

        self.checkbox_value = tk.BooleanVar()
        self.checkbox = ttk.Checkbutton(self.leftside_frame, text="Check Button", variable=self.checkbox_value, takefocus=0)
        self.checkbox.grid(column=0, row=0, sticky="w")

        self.radio_button_frame = ttk.Frame(self.leftside_frame)
        self.radio_button_frame.grid(row=1, column=0, sticky="w")
        self.radio_button_text = ttk.Label(self.radio_button_frame, text="Radio Buttons ", style="FooterInfo.TLabel", relief="solid")
        self.radio_button_text.grid(column=0, row=1, sticky="w")
        self.radio_button_selected = tk.StringVar()
        self.radio_button1 = ttk.Radiobutton(self.radio_button_frame, text='1', value='1', variable=self.radio_button_selected, takefocus=0, style="TRadiobutton")
        self.radio_button1.grid(column=1, row=1, sticky="w")
        self.radio_button2 = ttk.Radiobutton(self.radio_button_frame, text='2', value='2', variable=self.radio_button_selected, takefocus=0, style="TRadiobutton")
        self.radio_button2.grid(column=2, row=1, sticky="w")
        self.radio_button3 = ttk.Radiobutton(self.radio_button_frame, text='3', value='3', variable=self.radio_button_selected, takefocus=0, style="TRadiobutton")
        self.radio_button3.grid(column=3, row=1, sticky="w")

        self.reset_button = tk.Button(self.leftside_frame, text="Reset Game Button", command=self.reset_board, background=self.bg_color, foreground="White", relief="flat")
        self.reset_button.grid(row=2, column=0, sticky="w")

        # center game frame / main board frame
        self.middle_frame = tk.Frame(self.main_content_frame, bg=self.bg_color, bd=1)
        self.middle_frame.grid(column=1, row=0, sticky="nsew")

        # right side game frame
        self.rightside_frame = tk.Frame(self.main_content_frame, bg=self.bg_color, bd=1)
        self.rightside_frame.grid(column=2, row=0, sticky="nsew")


        # footer frame
        self.footer_frame = tk.Frame(self.mainframe, bg=self.bg_color, bd=1, height=75)
        self.footer_frame.grid(column=0, row=2, sticky="nsew")
        self.footer_frame.pack_propagate(False)

        self.footer_info = ttk.Label(self.footer_frame, text="Ryan Phillips\nUMKC CS 449\nSprint 0 GUI", style="FooterInfo.TLabel")
        self.footer_info.grid(row=0, column=0)

        # TODO: Adjust board size from this entry value
        self.board_size = tk.IntVar(value=5)
        #self.board_size_entry = ttk.Entry(
        #    self.mainframe, textvariable=self.board_size, style="TEntry", font=self.style.lookup("TEntry", "font"))
        
        board_size = self.get_total_board_draw_size()
        self.board_canvas = tk.Canvas(self.middle_frame, width=board_size, height=board_size, bg=self.bg_color, highlightthickness=0)
        self.board_canvas.pack()
        #self.board_canvas.grid(row=0, column=0)
        self.board_canvas.bind("<Button-1>", self.on_board_cell_click)
        
        self.status = ttk.Label(self.rightside_frame, text=self.turn_text[0], font=("Segoe UI", 12), style="FooterInfo.TLabel")
        self.status.grid(row=4, column=0, sticky="w", padx=8, pady=(6, 10))
        
        self.reset_board()
        
        # on game window adjustment
        self.bind("<Configure>", self.on_configure)

    def get_total_board_draw_size(self):
        return self.board_cell_size * self.board_size.get()

    def reset_board(self):
        self.status.config(text=self.turn_text[0])
        self.draw_board()

    def on_board_cell_click(self, event):
        print(f"CLicked on board cell {event}")
        pass
    
    # Draw the board lines on the canavs
    def draw_board(self):
        self.board_canvas.delete("all")

        total_board_draw_size = self.get_total_board_draw_size()
        
        # Vertical lines
        for i in range(1, self.board_size.get()):
            x = i * self.board_cell_size
            self.board_canvas.create_line(x, 0, x, total_board_draw_size, width=self.board_line_width, fill="White")
        # Horizontal lines
        for i in range(1, self.board_size.get()):
            y = i * self.board_cell_size
            self.board_canvas.create_line(0, y, total_board_draw_size, y, width=self.board_line_width, fill="White")

    def on_configure(self, event):
        print(f"on_configure {event}")
        pass

# run main app loop
#if __name__ == "__main__":
    #app = App()
    #app.mainloop()