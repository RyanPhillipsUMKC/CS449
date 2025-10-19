'''
Ryan Phillips 
UMKC CS 449 Sprint 2 GUI
Language: Python
GUI Framework: TKinter
sprint0_gui.py
'''
import tkinter as tk
from tkinter import ttk

from Board import *

# GameCellUIParameters
# We map from the UI canvas element board cell to these parametrs so we can check game state and other ui utility things
# i wish we had structs fo things like this
# could just use a tuple bit i want named vars
class GameCellUIParameters(object):
    def __init__(self):
        self.row = -1
        self.col = -1
        self.text_canvas_index = -1


# Provides a gui in Tkinter to play the SOS game on
# initilaizes the game within class
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # Setup Main App Config
        self.title('SOS Game')

        # default to half user screen size and allow resizing and scaling to an adjustable window
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{int(screen_width * 0.5)}x{int(screen_height * 0.5)}')
        self.resizable(1, 1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # configure styles
        self.bg_color = "#181818"
        self.default_board_cell_size = 60
        self.default_board_dims = 5
        self.board_line_width = 3

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure('TLabel', relief="flat", borderwidth=0, font=('Helvetica', 22))
        self.style.configure('TEntry', font=('Helvetica', 16), fieldbackground=self.bg_color, background=self.bg_color, foreground="white", insertcolor="white", justify="left")
        self.style.configure('Heading.TLabel', relief="flat", borderwidth=0, background=self.bg_color, foreground="white", font=('Helvetica', 32))
        self.style.configure('FooterInfo.TLabel', relief="flat", borderwidth=0, background=self.bg_color, foreground="white", font=('Helvetica', 16))
        self.style.configure("TRadiobutton", relief="flat", borderwidth=0, font=('Helvetica', 16, 'bold'), foreground='white', background=self.bg_color)
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

        self.heading = ttk.Label(self.header_frame, text='SOS Game', style='Heading.TLabel').pack(pady=20)

        # main content game frame
        self.main_content_frame = tk.Frame(self.mainframe)
        self.main_content_frame.grid(row=1, column=0, sticky="nsew", pady=6)
        self.main_content_frame.rowconfigure(0, weight=1)
        self.main_content_frame.columnconfigure([0, 1 ,2], weight=1, uniform="cols")
        # remove focus
        self.mainframe.bind_all("<Button-1>", lambda event: event.widget.focus_set())

        # left side game config frame
        self.leftside_frame = tk.Frame(self.main_content_frame, bg=self.bg_color, bd=1, relief="flat")
        self.leftside_frame.grid(column=0, row=0, sticky="nsew")

        self.game_config_text = ttk.Label(self.leftside_frame, text="Game Configuration", style="FooterInfo.TLabel", relief="flat")
        self.game_config_text.grid(row=0, column=0, sticky="w", pady=15)

        # Board size config
        self.board_size_config_frame = ttk.Frame(self.leftside_frame, relief="flat", borderwidth=0)
        self.board_size_config_frame.grid(row=1, column=0, sticky="w", pady=5)
        self.board_size_config_text = ttk.Label(self.board_size_config_frame, text="Board size: ", style="FooterInfo.TLabel", relief="flat")
        self.board_size_config_text.grid(column=0, row=0, sticky="nsw")
        self.board_size_config_selection_x = tk.IntVar(value=self.default_board_dims)
        self.board_size_config_entry_x = ttk.Entry(self.board_size_config_frame, textvariable=self.board_size_config_selection_x, style="TEntry", width=5)
        self.board_size_config_entry_x.grid(column=1, row=0, sticky="w")
        self.board_size_config_text_seperator = ttk.Label(self.board_size_config_frame, text="x", style="FooterInfo.TLabel", relief="flat")
        self.board_size_config_text_seperator.grid(column=2, row=0, sticky="nsw")
        self.board_size_config_selection_y = tk.IntVar(value=self.default_board_dims)
        self.board_size_config_entry_y = ttk.Entry(self.board_size_config_frame, textvariable=self.board_size_config_selection_y, style="TEntry", width=5)
        self.board_size_config_entry_y.grid(column=3, row=0, sticky="w")

        # Game mode config
        self.game_mode_config_frame = ttk.Frame(self.leftside_frame, relief="flat", borderwidth=0)
        self.game_mode_config_frame.grid(row=2, column=0, sticky="w", pady=5)
        self.game_mode_config_text = ttk.Label(self.game_mode_config_frame, text="Game Mode: ", style="FooterInfo.TLabel", relief="flat")
        self.game_mode_config_text.grid(column=0, row=1, sticky="nsw")
        self.game_mode_config_selection = tk.StringVar(self.game_mode_config_frame, "1")
        self.game_mode_config_button_simple_game = ttk.Radiobutton(self.game_mode_config_frame, text='Simple', value='1', variable=self.game_mode_config_selection, takefocus=0, style="TRadiobutton")
        self.game_mode_config_button_simple_game.grid(column=1, row=1, sticky="w")
        self.game_mode_config_button_general_game = ttk.Radiobutton(self.game_mode_config_frame, text='General', value='2', variable=self.game_mode_config_selection, takefocus=0, style="TRadiobutton")
        self.game_mode_config_button_general_game.grid(column=2, row=1, sticky="w")

        # Red Player Current Config
        self.red_player_config_frame = ttk.Frame(self.leftside_frame, relief="flat", borderwidth=0)
        self.red_player_config_frame.grid(row=3, column=0, sticky="w", pady=5)
        self.red_player_config_text = ttk.Label(self.red_player_config_frame, text="Red Player: ", style="FooterInfo.TLabel", relief="flat")
        self.red_player_config_text.grid(column=0, row=1, sticky="nsw")
        self.red_player_config_selection = tk.StringVar(self.red_player_config_frame, "S")
        self.red_player_config_button_S = ttk.Radiobutton(self.red_player_config_frame, text='S', value='S', variable=self.red_player_config_selection, takefocus=0, style="TRadiobutton")
        self.red_player_config_button_S.grid(column=1, row=1, sticky="w")
        self.red_player_config_button_O = ttk.Radiobutton(self.red_player_config_frame, text='O', value='O', variable=self.red_player_config_selection, takefocus=0, style="TRadiobutton")
        self.red_player_config_button_O.grid(column=2, row=1, sticky="w")
        
        # Blue Player Current Config
        self.blue_player_config_frame = ttk.Frame(self.leftside_frame, relief="flat", borderwidth=0)
        self.blue_player_config_frame.grid(row=4, column=0, sticky="w", pady=5)
        self.blue_player_config_text = ttk.Label(self.blue_player_config_frame, text="Blue Player: ", style="FooterInfo.TLabel", relief="flat")
        self.blue_player_config_text.grid(column=0, row=1, sticky="nsw")
        self.blue_player_config_selection = tk.StringVar(self.blue_player_config_frame, "S")
        self.blue_player_config_button_S = ttk.Radiobutton(self.blue_player_config_frame, text='S', value='S', variable=self.blue_player_config_selection, takefocus=0, style="TRadiobutton")
        self.blue_player_config_button_S.grid(column=1, row=1, sticky="w")
        self.blue_player_config_button_O = ttk.Radiobutton(self.blue_player_config_frame, text='O', value='O', variable=self.blue_player_config_selection, takefocus=0, style="TRadiobutton")
        self.blue_player_config_button_O.grid(column=2, row=1, sticky="w")

        # Reset game config button
        self.reset_button = tk.Button(self.leftside_frame, text="Reset Game Button", command=self.reset_game, background=self.bg_color, foreground="White", relief="flat")
        self.reset_button.grid(row=5, column=0, sticky="w", pady=40)

        # center game frame / main board frame
        self.middle_frame = tk.Frame(self.main_content_frame, bg=self.bg_color, bd=1)
        self.middle_frame.grid(column=1, row=0, sticky="nsew")

        # right side game frame
        self.rightside_frame = tk.Frame(self.main_content_frame, bg=self.bg_color, bd=1)
        self.rightside_frame.grid(column=2, row=0, sticky="nsew")

        # Game state
        self.game_state_text = ttk.Label(self.rightside_frame, text="Game State", style="FooterInfo.TLabel", relief="flat")
        self.game_state_text.grid(row=0, column=0, sticky="w", pady=15)

        self.game_state_current_turn_text_player_type = ttk.Label(self.rightside_frame, text="", style="FooterInfo.TLabel", foreground="Red")
        self.game_state_current_turn_text_player_type.grid(row=1, column=0, sticky="w", pady=5)
        self.game_state_current_turn_text = ttk.Label(self.rightside_frame, text=" player's turn to move", style="FooterInfo.TLabel")
        self.game_state_current_turn_text.grid(row=1, column=1, sticky="w", pady=5)


        # footer frame
        self.footer_frame = tk.Frame(self.mainframe, bg=self.bg_color, bd=1, height=75)
        self.footer_frame.grid(column=0, row=2, sticky="nsew")
        self.footer_frame.pack_propagate(False)

        self.footer_info = ttk.Label(self.footer_frame, text="Ryan Phillips\nUMKC CS 449\nSprint 2 GUI", style="FooterInfo.TLabel")
        self.footer_info.grid(row=0, column=0)

        
        board_size = self.get_total_board_draw_size()
        self.board_canvas = tk.Canvas(self.middle_frame, width=board_size[0], height=board_size[1], bg=self.bg_color, highlightthickness=0)
        self.board_canvas.pack(pady=50)
        #self.board_canvas.grid(row=0, column=0)
        self.board_canvas.bind("<Button-1>", self.on_board_cell_click)
        self.board_canvas.bind("<Motion>", self.on_board_hover_motion)
        self.board_canvas.bind("<Leave>", self.on_board_mouse_leave_event)
        

        self.game_board = None
        self.canvas_board_cell_index_to_params = dict()
        self.reset_game()
        
        # on game window adjustment
        self.bind("<Configure>", self.on_configure)

    def reset_game(self):
        board_dims = self.get_board_dims()

        # only allocate the game once
        if self.game_board is None:
            self.game_board = GameBoard(
                GameType.Simple if self.game_mode_config_selection.get() == "1" else GameType.General, 
                board_dims[0],
                board_dims[1] ,
                PlayerType.Red)
        else:
            self.game_board.reset(
                GameType.Simple if self.game_mode_config_selection.get() == "1" else GameType.General, 
                board_dims[0],
                board_dims[1] ,
                PlayerType.Red)
        
        self.update_turn_text()
        self._draw_board()
    
    def update_turn_text(self):
        turn = self.game_board.get_turn()
        if turn == PlayerType.Red:
            self.game_state_current_turn_text_player_type.config(text="Red", foreground="red")
        else:
            self.game_state_current_turn_text_player_type.config(text="Blue", foreground="blue")


    def on_board_hover_motion(self, event):
        print(f"Canvas motion event {event}, {event.widget}")

        self._clear_hover_state()
        
        closest_cell_id = self._get_closest_cell_spot_index_from_event(event)

        # invalid click spot... ignore
        if closest_cell_id == -1:
            return
        
        cell_params = self.canvas_board_cell_index_to_params[closest_cell_id]
        slot_type = self.game_board.get_slot_type_for_spot(cell_params.row, cell_params.col)

        if slot_type == BoardSlotType.Empty:
            # chnage hover state of cell
            self.board_canvas.itemconfigure(closest_cell_id, fill="grey")

    def on_board_mouse_leave_event(self, event):
        self._clear_hover_state()

     # clear all previous hover states
    def _clear_hover_state(self):
        for id in self.canvas_board_cell_index_to_params:
             self.board_canvas.itemconfigure(id, fill=self.bg_color)

    def on_board_cell_click(self, event) -> None:
        print(f"Canvas clicked on event {event}, {event.widget}")

        closest_cell_id = self._get_closest_cell_spot_index_from_event(event)

        # invalid click spot... ignore
        if closest_cell_id == -1:
            return
        
        cell_params = self.canvas_board_cell_index_to_params[closest_cell_id]

        # try to update game state
        turn = self.game_board.get_turn()
        turn_slot_type = BoardSlotType.Empty
        turn_text = ""

        if turn == PlayerType.Red:
            if self.red_player_config_selection.get() == "S":
                turn_slot_type = BoardSlotType.S
                turn_text = "S"
            else:
                turn_slot_type = BoardSlotType.O
                turn_text = "O"
        else:
            if self.blue_player_config_selection.get() == "S":
                turn_slot_type = BoardSlotType.S
                turn_text = "S"
            else:
                turn_slot_type = BoardSlotType.O
                turn_text = "O"

        move_function_return_type = self.game_board.make_move(
            turn_slot_type, cell_params.row, cell_params.col)
        
        if move_function_return_type != MovefunctionReturnType.ValidMove:
            # TODO: could display popups here ??
            print("Failied move!!!!")
            return

        # update cell ui state
        self.board_canvas.itemconfigure(cell_params.text_canvas_index, text=turn_text)

        # check and display game state iff needed
        if self.game_board.game_state != GameStateType.Ongoing:
            self.reset_game()
        else:
            self._clear_hover_state()
            self.update_turn_text()


    # find closest board cell spot from tkinter event
    def _get_closest_cell_spot_index_from_event(self, event) -> int:
        closest_cell_id = -1
        # have to use find_overlapping over find_closest because closest will return the upper z order text if directly on it
        closest_item_ids = self.board_canvas.find_overlapping(event.x, event.y, event.x, event.y)
        for id in closest_item_ids:
            if id in self.canvas_board_cell_index_to_params:
                closest_cell_id = id
                break
        return closest_cell_id
    
    # Draw the board lines, state, etc.. on the canavs
    # z order for canvas = hover rectangle -> Cell state text (s or o) -> board lines
    def _draw_board(self):
        self.board_canvas.delete("all")

        board_dims = self.get_board_dims()
        cell_size = self.get_cell_size()

        self.canvas_board_cell_index_to_params = dict()
        # draw board cell and init their params
        for row in range(board_dims[0]):
            for col in range(board_dims[1]):
                cell_parameters = GameCellUIParameters()
                cell_parameters.row = row
                cell_parameters.col = col
                
                # cells + hover rexts
                y_space = row * cell_size
                x_space = col * cell_size
                cell_index = self.board_canvas.create_rectangle(
                    x_space, 
                    y_space, 
                    x_space + cell_size, 
                    y_space + cell_size,
                    tags="cell",
                    fill=self.bg_color, outline=self.bg_color)

                # state text (s or o)
                cell_parameters.text_canvas_index = self.board_canvas.create_text(
                    x_space + (cell_size * 0.5), y_space + (cell_size * 0.5), text="", fill="white")

                self.canvas_board_cell_index_to_params[cell_index] = cell_parameters

        total_board_draw_size = self.get_total_board_draw_size()
        # Vertical lines
        for i in range(1, board_dims[1]):
            x = i * cell_size
            self.board_canvas.create_line(x, 0, x, total_board_draw_size[0], width=self.board_line_width, fill="White")
        # Horizontal lines
        for i in range(1, board_dims[0]):
            y = i * cell_size
            self.board_canvas.create_line(0, y, total_board_draw_size[1], y, width=self.board_line_width, fill="White")

    def on_configure(self, event):
        print(f"TKinter Configuration event: {event}")

    def get_board_dims(self):
        return (self.board_size_config_selection_x.get(), self.board_size_config_selection_y.get())
    
    def get_cell_size(self):
        board_dims = self.get_board_dims()
        return self.default_board_cell_size * (self.default_board_dims / max(board_dims))
    
    def get_total_board_draw_size(self):
        board_dims = self.get_board_dims()
        cell_size = self.get_cell_size()
        return ((cell_size * board_dims[0]), (cell_size * board_dims[1]))

# run main app loop
if __name__ == "__main__":
    app = App()
    app.mainloop()