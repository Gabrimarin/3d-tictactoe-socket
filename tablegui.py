import tkinter as tk
import table



class TableGUI(tk.Tk):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback
        self.title("Tic Tac Toe")
        self.geometry("")
        self.table = table.Table()
        self.show_connection_screen()


    def show_connection_screen(self):
        self.enter_ip_label = tk.Label(self, text="Enter the IP of the game you want to join (let it empty if you want to host a game):")
        self.enter_ip_label.grid(row=0, column=0)
        self.enter_ip_entry = tk.Entry(self, width=30)
        self.enter_ip_entry.grid(row=1, column=0, padx=10, pady=5)
        self.enter_game_button = tk.Button(self, text="Start a Game", command=lambda: self.start_game_callback(self.enter_ip_entry.get()))
        self.enter_game_button.grid(row=2, column=0)


    def hide_connection_screen(self):
        self.enter_ip_label.destroy()
        self.enter_ip_entry.destroy()
        self.enter_game_button.destroy()

    def show_waiting_screen(self, ip, as_guest):
        self.waiting_label = tk.Label(self, text="Waiting for connection...")
        self.waiting_label.grid(row=0, column=0)
        self.ip_label = tk.Label(self, text=f"{'Connecting to' if as_guest else 'Your ip'}: {ip}")
        self.ip_label.grid(row=1, column=0)

    def hide_waiting_screen(self):
        self.waiting_label.destroy()
        self.ip_label.destroy()

    def give_up(self):
        self.give_up_sender()

    def get_score_text(self):
        return f"P1 ({self.table.score[0]}x{self.table.score[1]}) P2"

    def show_game_screen(self):
        self.score = tk.Label(self, text=self.get_score_text(), font=("Arial", 20), width=10, height=2, wraplength=200)
        self.score.grid(row=0, column=3, columnspan=3)
        self.player_label = tk.Label(self, text="Waiting...", font=("Arial", 20), width=10, height=2)
        self.player_label.grid(row=1, column=3, columnspan=3)
        # it's a 3d array
        self.labels = [[[None for _ in range(3)] for _ in range(3)] for _ in range(3)]
        # shades of gray
        borders = ["raised", "solid", "sunken"]
        for k in range(3):
            for i in range(3):
                for j in range(3):
                    self.labels[k][i][j] = tk.Label(self, text="", font=("Arial", 20), width=7, height=2, borderwidth=2, relief=borders[k])
                    self.labels[k][i][j].grid(row=i + 2, column=(j + k * 3), padx=(20 if j == 0 else 0, 20 if j == 2 and k == 2 else 0))
                    self.labels[k][i][j].bind("<Button-1>", lambda event, i=i, j=j, k=k: self.on_click(i, j, k))


        self.chat_log = tk.Text(self, width=30, height=10)
        self.chat_log.grid(row=5, column=3, columnspan=3, padx=10, pady=10)

        self.chat_entry = tk.Entry(self, width=30)
        self.chat_entry.grid(row=6, column=3, columnspan=3, padx=10, pady=5)
        self.chat_entry.bind("<Return>", lambda event: self.send_message())
        self.chat_button = tk.Button(self, text="Send", command=self.send_message)
        self.chat_button.grid(row=7, column=3, columnspan=3, padx=10, pady=5)
        self.give_up_button = tk.Button(self, text="Give up", command=self.give_up, background="red")
        self.give_up_button.grid(row=8, column=3, columnspan=3, padx=10, pady=5)
        self.message_sender = lambda message: None
        self.move_sender = lambda x, y, z: None
        self.player = 0
        self.connected = False

    def hide_game_screen(self):
        self.score.destroy()
        self.player_label.destroy()
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.labels[i][j][k].destroy()
        self.chat_log.destroy()
        self.chat_entry.destroy()
        self.chat_button.destroy()
        self.give_up_button.destroy()

    def show_disconnected_screen(self):
        self.disconnected_label = tk.Label(self, text="The game was ended", font=("Arial", 20), width=30, height=10)
        self.disconnected_label.grid(row=0, column=0, columnspan=3)
        def show_connection_screen():
            self.hide_disconnected_screen()
            self.show_connection_screen()
        self.disconnected_button = tk.Button(self, text="Ok", command=show_connection_screen)
        self.disconnected_button.grid(row=1, column=0, columnspan=3)

    def hide_disconnected_screen(self):
        self.disconnected_label.destroy()
        self.disconnected_button.destroy()

    def start_game(self, message_sender, move_sender, give_up_sender, player):
        self.show_game_screen()
        self.message_sender = message_sender
        self.move_sender = move_sender
        self.give_up_sender = give_up_sender
        self.connected = True
        self.player = player
        self.player_label.config(text=f"Player {player}")

    def make_move(self, x, y, z):
        position_validation = self.table.update_table(x, y, z)
        self.player_label.config(fg="green" if self.table.turn == self.player else "red")
        if not position_validation:
            return False
        self.labels[z][x][y].config(text="X" if self.table.turn == 1 else "O")
        if position_validation == 'win':
            winner = 1 if self.table.turn == 2 else 2
            self.append_message(f"Player {winner} wins!")
            self.table.score[winner - 1] += 1
            self.score.config(text=self.get_score_text())
            self.reset_game()
        elif position_validation == 'draw':
            self.append_message("It's a draw!")
            self.reset_game()

    def on_click(self, x, y, z):
        if self.table.turn != self.player:
            return None
        success = self.move_sender(x, y, z)
        if success:
            self.make_move(x, y, z)

    def append_message(self, message):
        self.chat_log.insert(tk.END, message + "\n")
        self.chat_log.see(tk.END)  # Scroll to the end of the chat log

    def send_message(self):
        message = self.chat_entry.get()
        success = self.message_sender(message)
        if success:
            self.chat_entry.delete(0, tk.END)
            self.append_message("You: " + message)


    def reset_game(self):
        self.table.reset_table(True)
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    self.labels[i][j][k].config(text="")

if __name__ == "__main__":
    app = TableGUI()
    app.mainloop()
