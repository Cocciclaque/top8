import tkinter as tk
import os
from tkinter import messagebox, filedialog

def new_match():
    """Helper to create a new empty match dictionary."""
    return {"p1": None, "p2": None, "score1": None, "score2": None, "winner": None}

# Mappings for folder structure based on round keys.
ROUND_MAPPING_WINNERS = {
    "initial": "Round 1",
    "final": "Round 2",
    "grand_final": "Round 3",
    "reset": "Round 4"
}
ROUND_MAPPING_LOSERS = {
    "initial": "Round 1",
    "round2": "Round 2",
    "round3": "Round 3",
    "final": "Round 4"
}

class HorizontalTop8Bracket(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Top 8 Double-Elimination Bracket")
        self.configure(bg="#dddddd")  # Light gray background

        # 0) Stream Files Path Frame: choose the base folder for file export.
        self.stream_path_var = tk.StringVar(value="")  # Start empty.
        self.build_stream_path_frame()

        # 1) Editable seed entries at the top.
        self.seed_entries = []
        default_seeds = ["Seed1", "Seed8", "Seed4", "Seed5", "Seed2", "Seed7", "Seed3", "Seed6"]
        self.players_frame = tk.LabelFrame(
            self, text="Edit Player Names", bg="#eeeeee",
            font=("Arial", 12, "bold"), bd=5, padx=5, pady=5,
        )
        self.players_frame.grid(row=1, column=0, padx=10, pady=5, sticky="n")
        # Arrange 8 entries (2 rows x 4 columns) and disable them initially.
        for i in range(8):
            row_i = i // 4
            col_i = i % 4
            lbl = tk.Label(self.players_frame, text=f"Seed {i+1}:", bg="#eeeeee")
            lbl.grid(row=row_i*2, column=col_i, padx=5, pady=(0,2), sticky="e")
            entry = tk.Entry(self.players_frame, width=10, state="disabled")
            entry.grid(row=row_i*2+1, column=col_i, padx=5, pady=(0,5))
            entry.insert(0, default_seeds[i])
            self.seed_entries.append(entry)
        self.update_button = tk.Button(
            self.players_frame, text="Update Bracket",
            command=self.update_bracket_with_names, state="disabled"
        )
        self.update_all_button = tk.Button(
            self.players_frame, text="Update All Files",
            command=self.update_all_files, state="disabled"
        )
        self.update_all_button.grid(row=5, column=0, columnspan=4, pady=5)

        self.update_button.grid(row=4, column=0, columnspan=4, pady=5)

        # 2) Bracket data structures.
        self.winners = {
            "initial": [ new_match() for _ in range(2) ],
            "final": [ new_match() for _ in range(1) ],
            "grand_final": [ new_match() for _ in range(1) ],
            "reset": [ new_match() for _ in range(1) ]
        }
        self.losers = {
            "initial": [ new_match() for _ in range(2) ],
            "round2": [ new_match() for _ in range(2) ],
            "round3": [ new_match() for _ in range(1) ],
            "final": [ new_match() for _ in range(1) ]
        }
        self.winners_labels = {}
        self.losers_labels = {}

        # 3) Build the UI layout.
        self.build_bracket_layout()
        self.update_ui()

    def build_stream_path_frame(self):
        """Frame at the very top to choose the directory for stream files."""
        path_frame = tk.LabelFrame(
            self, text="Stream Files Path", bg="#eeeeee",
            font=("Arial", 12, "bold"), bd=5, padx=5, pady=5
        )
        path_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nw")
        tk.Label(path_frame, text="Directory:", bg="#eeeeee").grid(row=0, column=0, sticky="e")
        path_entry = tk.Entry(path_frame, textvariable=self.stream_path_var, width=50)
        path_entry.grid(row=0, column=1, padx=5, pady=5)
        browse_btn = tk.Button(path_frame, text="Browse...", command=self.choose_folder)
        browse_btn.grid(row=0, column=2, padx=5, pady=5)

    def choose_folder(self):
        """Open a folder dialog and update the stream path.
           Enables the seed entries and update button, and initializes the file structure.
        """
        folder = filedialog.askdirectory(initialdir=".", title="Select Folder for Match Files")
        if folder:
            self.stream_path_var.set(folder)
            self.enable_players_frame()
            self.initialize_file_structure()
        else:
            messagebox.showerror("Folder Required", "You must select a folder to export files before continuing.")

    def enable_players_frame(self):
        for entry in self.seed_entries:
            entry.config(state="normal")
        self.update_button.config(state="normal")
        self.update_all_button.config(state="normal")


    def initialize_file_structure(self):
        """
        Creates the folder structure with empty files for all matches.
        This is based on our round mappings for both winners and losers.
        """
        base = self.stream_path_var.get()
        # For winners
        for round_key, folder_name in ROUND_MAPPING_WINNERS.items():
            round_folder = os.path.join(base, folder_name)
            os.makedirs(round_folder, exist_ok=True)
            for match_index in range(len(self.winners.get(round_key, []))):
                match_folder = os.path.join(round_folder, f"Winner {match_index+1}")
                os.makedirs(match_folder, exist_ok=True)
                for player_num in [1, 2]:
                    player_folder = os.path.join(match_folder, f"Player {player_num}")
                    os.makedirs(player_folder, exist_ok=True)
                    with open(os.path.join(player_folder, f"Player {player_num}"), "w", encoding="utf-8") as f:
                        f.write("")
                    with open(os.path.join(player_folder, f"Score P{player_num}"), "w", encoding="utf-8") as f:
                        f.write("")
        # For losers
        for round_key, folder_name in ROUND_MAPPING_LOSERS.items():
            round_folder = os.path.join(base, folder_name)
            os.makedirs(round_folder, exist_ok=True)
            for match_index in range(len(self.losers.get(round_key, []))):
                match_folder = os.path.join(round_folder, f"Loser {match_index+1}")
                os.makedirs(match_folder, exist_ok=True)
                for player_num in [1, 2]:
                    player_folder = os.path.join(match_folder, f"Player {player_num}")
                    os.makedirs(player_folder, exist_ok=True)
                    with open(os.path.join(player_folder, f"Player {player_num}"), "w", encoding="utf-8") as f:
                        f.write("")
                    with open(os.path.join(player_folder, f"Score P{player_num}"), "w", encoding="utf-8") as f:
                        f.write("")

    def build_bracket_layout(self):
        """Creates UI panels for Winners and Losers with Win, Edit, and Stream buttons."""
        # Winners Panel
        self.winners_frame = tk.LabelFrame(
            self, text="Winners Bracket", bg="#fafafa",
            font=("Arial", 14, "bold"), bd=5, padx=5, pady=5
        )
        self.winners_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nw")
        winners_rounds = ["initial", "final", "grand_final", "reset"]
        for col_index, round_name in enumerate(winners_rounds):
            rf = tk.LabelFrame(
                self.winners_frame,
                text=self.pretty_round_name(round_name, winners=True),
                bg="#fafafa", font=("Arial", 12, "bold"), bd=2, padx=5, pady=5
            )
            rf.grid(row=0, column=col_index, padx=10, pady=5, sticky="n")
            for match_index, match in enumerate(self.winners[round_name]):
                m_lbl = tk.Label(rf, text=self.match_text(match), bg="#ffffff", relief="ridge",
                                 width=24, font=("Arial", 10))
                m_lbl.grid(row=match_index*2, column=0, columnspan=4, pady=(5,0))
                self.winners_labels[(round_name, match_index)] = m_lbl

                b1 = tk.Button(rf, text="Win #1",
                               command=lambda rn=round_name, mi=match_index, w=0: self.set_winner("winners", rn, mi, w))
                b1.grid(row=match_index*2+1, column=0, padx=2, pady=(0,5), sticky="e")
                b2 = tk.Button(rf, text="Win #2",
                               command=lambda rn=round_name, mi=match_index, w=1: self.set_winner("winners", rn, mi, w))
                b2.grid(row=match_index*2+1, column=1, padx=2, pady=(0,5), sticky="w")
                b_edit = tk.Button(rf, text="Edit",
                                  command=lambda rn=round_name, mi=match_index, bt="winners": self.edit_match(bt, rn, mi))
                b_edit.grid(row=match_index*2+1, column=2, padx=2, pady=(0,5))
                b_stream = tk.Button(rf, text="Stream",
                                     command=lambda rn=round_name, mi=match_index, bt="winners": self.stream_match(bt, rn, mi))
                b_stream.grid(row=match_index*2+1, column=3, padx=2, pady=(0,5))
        # Losers Panel
        self.losers_frame = tk.LabelFrame(
            self, text="Losers Bracket", bg="#f0faff",
            font=("Arial", 14, "bold"), bd=5, padx=5, pady=5
        )
        self.losers_frame.grid(row=3, column=0, padx=10, pady=10, sticky="sw")
        losers_rounds = ["initial", "round2", "round3", "final"]
        for col_index, round_name in enumerate(losers_rounds):
            rf = tk.LabelFrame(
                self.losers_frame,
                text=self.pretty_round_name(round_name, winners=False),
                bg="#f0faff", font=("Arial", 12, "bold"), bd=2, padx=5, pady=5
            )
            rf.grid(row=0, column=col_index, padx=10, pady=5, sticky="n")
            for match_index, match in enumerate(self.losers[round_name]):
                m_lbl = tk.Label(rf, text=self.match_text(match), bg="#ffffff", relief="ridge",
                                 width=24, font=("Arial", 10))
                m_lbl.grid(row=match_index*2, column=0, columnspan=4, pady=(5,0))
                self.losers_labels[(round_name, match_index)] = m_lbl

                b1 = tk.Button(rf, text="Win #1",
                               command=lambda rn=round_name, mi=match_index, w=0: self.set_winner("losers", rn, mi, w))
                b1.grid(row=match_index*2+1, column=0, padx=2, pady=(0,5), sticky="e")
                b2 = tk.Button(rf, text="Win #2",
                               command=lambda rn=round_name, mi=match_index, w=1: self.set_winner("losers", rn, mi, w))
                b2.grid(row=match_index*2+1, column=1, padx=2, pady=(0,5), sticky="w")
                b_edit = tk.Button(rf, text="Edit",
                                  command=lambda rn=round_name, mi=match_index, bt="losers": self.edit_match(bt, rn, mi))
                b_edit.grid(row=match_index*2+1, column=2, padx=2, pady=(0,5))
                b_stream = tk.Button(rf, text="Stream",
                                     command=lambda rn=round_name, mi=match_index, bt="losers": self.stream_match(bt, rn, mi))
                b_stream.grid(row=match_index*2+1, column=3, padx=2, pady=(0,5))

    def match_text(self, match):
        """Returns formatted text for a match, including the winner and full score.
           Display shows full score in format "score1-score2" if a winner is set.
        """
        if match.get("winner"):
            if match["score1"] is not None and match["score2"] is not None:
                full_score = f"{match['score1']}-{match['score2']}"
            else:
                full_score = ""
            return f"Winner: {match['winner']} ({full_score})"
        p1 = match["p1"] if match["p1"] else "-"
        p2 = match["p2"] if match["p2"] else "-"
        s1 = f"({match['score1']})" if match["score1"] is not None else ""
        s2 = f"({match['score2']})" if match["score2"] is not None else ""
        return f"{p1} {s1} vs {p2} {s2}"

    def update_bracket_with_names(self):
        """Seeds the brackets using the 8 entered names.
           Winners 'initial' gets players 1-4 (match0: Seed1 vs Seed4, match1: Seed2 vs Seed3)
           Losers 'initial' gets players 5-8 (match0: Seed5 vs Seed8, match1: Seed6 vs Seed7)
        """
        seeds = [entry.get() for entry in self.seed_entries]
        if len(seeds) < 8:
            return
        self.winners["initial"][0] = {"p1": seeds[0], "p2": seeds[3], "score1": None, "score2": None, "winner": None}
        self.winners["initial"][1] = {"p1": seeds[1], "p2": seeds[2], "score1": None, "score2": None, "winner": None}
        self.losers["initial"][0] = {"p1": seeds[4], "p2": seeds[7], "score1": None, "score2": None, "winner": None}
        self.losers["initial"][1] = {"p1": seeds[5], "p2": seeds[6], "score1": None, "score2": None, "winner": None}
        for r in ["final", "grand_final", "reset"]:
            for m in self.winners[r]:
                m["p1"] = None; m["p2"] = None; m["score1"] = None; m["score2"] = None; m["winner"] = None
        for r in ["round2", "round3", "final"]:
            for m in self.losers[r]:
                m["p1"] = None; m["p2"] = None; m["score1"] = None; m["score2"] = None; m["winner"] = None
        self.update_ui()

    def update_all_files(self):
        for round_name, matches in self.winners.items():
            for i, match in enumerate(matches):
                self.update_match_files(match, "winners", round_name, i)
        for round_name, matches in self.losers.items():
            for i, match in enumerate(matches):
                self.update_match_files(match, "losers", round_name, i)
        messagebox.showinfo("Success", "All match files have been updated.")


    def pretty_round_name(self, round_name, winners=True):
        if winners:
            mapping = {
                "initial": "Winners Initial",
                "final": "Winners Final",
                "grand_final": "Grand Final",
                "reset": "Reset Match"
            }
        else:
            mapping = {
                "initial": "Losers Initial",
                "round2": "Losers Round 2",
                "round3": "Losers Round 3",
                "final": "Losers Final"
            }
        return mapping.get(round_name, round_name)

    # -------------------------------
    # Advancement Logic (modified for new round keys)
    # -------------------------------
    def set_winner(self, bracket_type, round_name, match_index, winner_index):
        """Sets the winner of a match, advances the winner, sends the loser, and updates files."""
        if bracket_type == "winners":
            match = self.winners[round_name][match_index]
        else:
            match = self.losers[round_name][match_index]
        if not match["p1"] or not match["p2"]:
            messagebox.showerror("Error", "Match is not ready or incomplete!")
            return
        winner = match["p1"] if winner_index == 0 else match["p2"]
        loser = match["p2"] if winner_index == 0 else match["p1"]
        if match["score1"] is None and match["score2"] is None:
            if winner_index == 0:
                match["score1"] = 2; match["score2"] = 0
            else:
                match["score1"] = 0; match["score2"] = 2
        if bracket_type == "winners":
            self.advance_in_winners(round_name, match_index, winner, loser, winner_index)
        else:
            self.advance_in_losers(round_name, match_index, winner, loser)
        match["winner"] = winner
        self.update_ui()
        self.update_match_files(match, bracket_type, round_name, match_index)

    def advance_in_winners(self, round_name, match_index, winner, loser, winner_index):
        if round_name == "initial":
            next_match_idx = 0
            slot = match_index
            self.place_player_in_match(self.winners["final"], next_match_idx, winner, slot)
            self.place_player_in_match(self.losers["round2"], match_index, loser, forced_slot=1)
        elif round_name == "final":
            next_match_idx = 0
            slot = match_index
            self.place_player_in_match(self.winners["grand_final"], next_match_idx, winner, slot)
            self.place_player_in_match(self.losers["final"], match_index, loser, forced_slot=1)
        elif round_name == "grand_final":
            current_match = self.winners["grand_final"][0]
            if winner_index == 0:
                messagebox.showinfo("Tournament Over", f"{winner} is the Champion!")
                messagebox.showinfo("Runner-Up", f"{loser} takes 2nd place!")
            else:
                orig_winner = current_match["p1"]
                self.place_player_in_match(self.winners["reset"], 0, orig_winner, forced_slot=0)
                self.place_player_in_match(self.winners["reset"], 0, winner, forced_slot=1)
                messagebox.showinfo("Reset", "Losers side won the Grand Final! Reset match scheduled.")
        elif round_name == "reset":
            if winner_index == 0:
                messagebox.showinfo("Tournament Over", f"{winner} is the Champion!")
                messagebox.showinfo("Runner-Up", f"{loser} takes 2nd place!")
            else:
                messagebox.showinfo("Tournament Over", f"{winner} is the Champion!")
                messagebox.showinfo("Runner-Up", f"{loser} takes 2nd place!")

    def advance_in_losers(self, round_name, match_index, winner, loser):
        if round_name == "initial":
            self.place_player_in_match(self.losers["round2"], match_index, winner, forced_slot=0)
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")
        elif round_name == "round2":
            placed = self.place_player_in_match(self.losers["round3"], 0, winner)
            if not placed:
                messagebox.showinfo("Eliminated", f"{winner} is eliminated!")
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")
        elif round_name == "round3":
            self.place_player_in_match(self.losers["final"], 0, winner, forced_slot=0)
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")
        elif round_name == "final":
            self.place_player_in_match(self.winners["grand_final"], 0, winner, forced_slot=1)
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")

    def place_player_in_match(self, match_list, match_idx, player, forced_slot=None):
        if match_idx is not None:
            m = match_list[match_idx]
            if forced_slot is not None:
                if forced_slot == 0 and m["p1"] is None:
                    m["p1"] = player
                    return True
                elif forced_slot == 1 and m["p2"] is None:
                    m["p2"] = player
                    return True
                alt = 1 - forced_slot
                if alt == 0 and m["p1"] is None:
                    m["p1"] = player
                    return True
                elif alt == 1 and m["p2"] is None:
                    m["p2"] = player
                    return True
                return False
            else:
                if m["p1"] is None:
                    m["p1"] = player
                    return True
                elif m["p2"] is None:
                    m["p2"] = player
                    return True
                return False
        else:
            for m in match_list:
                if forced_slot is not None:
                    if forced_slot == 0 and m["p1"] is None:
                        m["p1"] = player
                        return True
                    elif forced_slot == 1 and m["p2"] is None:
                        m["p2"] = player
                        return True
                    alt = 1 - forced_slot
                    if alt == 0 and m["p1"] is None:
                        m["p1"] = player
                        return True
                    elif alt == 1 and m["p2"] is None:
                        m["p2"] = player
                        return True
                else:
                    if m["p1"] is None:
                        m["p1"] = player
                        return True
                    elif m["p2"] is None:
                        m["p2"] = player
                        return True
            return False

    def update_ui(self):
        for round_name, matches in self.winners.items():
            for i, match in enumerate(matches):
                lbl = self.winners_labels.get((round_name, i))
                if lbl:
                    lbl.config(text=self.match_text(match))
        for round_name, matches in self.losers.items():
            for i, match in enumerate(matches):
                lbl = self.losers_labels.get((round_name, i))
                if lbl:
                    lbl.config(text=self.match_text(match))

    # -------------------------------
    # Stream to File Logic
    # -------------------------------
    def stream_match(self, bracket_type, round_name, match_index):
        if bracket_type == "winners":
            match = self.winners[round_name][match_index]
        else:
            match = self.losers[round_name][match_index]
        self.update_stream_files(match)

    def update_stream_files(self, match):
        p1 = match["p1"] if match["p1"] else "TBD"
        p2 = match["p2"] if match["p2"] else "TBD"
        dir_path = self.stream_path_var.get()
        try:
            if not os.path.isdir(dir_path):
                os.makedirs(dir_path, exist_ok=True)
            with open(os.path.join(dir_path, "player1.tmp"), "w", encoding="utf-8") as f:
                f.write(p1)
            with open(os.path.join(dir_path, "player2.tmp"), "w", encoding="utf-8") as f:
                f.write(p2)
            messagebox.showinfo("Stream Update", f"Updated stream files with:\nPlayer 1: {p1}\nPlayer 2: {p2}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update stream files:\n{e}")

    # -------------------------------
    # File System Export Functionality
    # -------------------------------
    def update_match_files(self, match, bracket_type, round_name, match_index):
        """
        Exports match data to a folder structure:
          BaseFolder/
              Round X/   (X from mapping)
                  Winner Y/ or Loser Y/   (Y = match_index+1)
                      Player 1/    contains "Player 1" and "Score P1"
                      Player 2/    contains "Player 2" and "Score P2"
        """
        if bracket_type == "winners":
            round_folder = ROUND_MAPPING_WINNERS.get(round_name, round_name)
            match_folder = f"Winner {match_index+1}"
        else:
            round_folder = ROUND_MAPPING_LOSERS.get(round_name, round_name)
            match_folder = f"Loser {match_index+1}"
        base = self.stream_path_var.get()
        round_path = os.path.join(base, round_folder)
        match_path = os.path.join(round_path, match_folder)
        os.makedirs(match_path, exist_ok=True)
        for player_num in [1, 2]:
            player_folder = os.path.join(match_path, f"Player {player_num}")
            os.makedirs(player_folder, exist_ok=True)
            if player_num == 1:
                pname = match["p1"] if match["p1"] else "TBD"
                pscore = str(match["score1"]) if match["score1"] is not None else ""
            else:
                pname = match["p2"] if match["p2"] else "TBD"
                pscore = str(match["score2"]) if match["score2"] is not None else ""
            player_file = os.path.join(player_folder, f"Player {player_num}")
            score_file = os.path.join(player_folder, f"Score P{player_num}")
            with open(player_file, "w", encoding="utf-8") as f:
                f.write(pname)
            with open(score_file, "w", encoding="utf-8") as f:
                f.write(pscore)

    # -------------------------------
    # Manual Edit Functionality
    # -------------------------------
    def edit_match(self, bracket_type, round_name, match_index):
        if bracket_type == "winners":
            match = self.winners[round_name][match_index]
        else:
            match = self.losers[round_name][match_index]
        editor = tk.Toplevel(self)
        editor.title(f"Edit {bracket_type.capitalize()} {self.pretty_round_name(round_name, bracket_type=='winners')} Match {match_index+1}")
        editor.grab_set()
        tk.Label(editor, text="Player 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        p1_entry = tk.Entry(editor)
        p1_entry.grid(row=0, column=1, padx=5, pady=5)
        p1_entry.insert(0, match["p1"] if match["p1"] else "")
        tk.Label(editor, text="Score 1:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
        s1_entry = tk.Entry(editor, width=5)
        s1_entry.grid(row=0, column=3, padx=5, pady=5)
        s1_entry.insert(0, match["score1"] if match["score1"] is not None else "")
        tk.Label(editor, text="Player 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        p2_entry = tk.Entry(editor)
        p2_entry.grid(row=1, column=1, padx=5, pady=5)
        p2_entry.insert(0, match["p2"] if match["p2"] else "")
        tk.Label(editor, text="Score 2:").grid(row=1, column=2, padx=5, pady=5, sticky="e")
        s2_entry = tk.Entry(editor, width=5)
        s2_entry.grid(row=1, column=3, padx=5, pady=5)
        s2_entry.insert(0, match["score2"] if match["score2"] is not None else "")
        def save_changes():
            match["p1"] = p1_entry.get() if p1_entry.get() else None
            match["p2"] = p2_entry.get() if p2_entry.get() else None
            try:
                match["score1"] = int(s1_entry.get())
            except:
                match["score1"] = None
            try:
                match["score2"] = int(s2_entry.get())
            except:
                match["score2"] = None
            self.update_ui()
            self.update_match_files(match, bracket_type, round_name, match_index)
            editor.destroy()
        save_btn = tk.Button(editor, text="Save", command=save_changes)
        save_btn.grid(row=2, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    app = HorizontalTop8Bracket()
    app.mainloop()
