import tkinter as tk
from tkinter import messagebox

def new_match():
    """Helper to create a new empty match dictionary."""
    return {"p1": None, "p2": None, "score1": None, "score2": None, "winner": None}
    
class HorizontalTop8Bracket(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Top 8 Double-Elimination Bracket (Horizontal) with Manual Control & Scores")
        self.configure(bg="#dddddd")  # Light gray background

        # 1) Editable seed entries at the top.
        self.seed_entries = []
        default_seeds = ["Seed1", "Seed8", "Seed4", "Seed5", "Seed2", "Seed7", "Seed3", "Seed6"]

        self.players_frame = tk.LabelFrame(
            self, text="Edit Player Names", bg="#eeeeee", 
            font=("Arial", 12, "bold"), labelanchor='n', bd=5, padx=5, pady=5
        )
        self.players_frame.grid(row=0, column=0, padx=10, pady=5, sticky="n")

        # Arrange 8 entries (2 rows x 4 columns)
        for i in range(8):
            row_i = i // 4
            col_i = i % 4
            lbl = tk.Label(self.players_frame, text=f"Seed {i+1}:", bg="#eeeeee")
            lbl.grid(row=row_i*2, column=col_i, padx=5, pady=(0,2), sticky="e")
            entry = tk.Entry(self.players_frame, width=10)
            entry.grid(row=row_i*2+1, column=col_i, padx=5, pady=(0,5))
            entry.insert(0, default_seeds[i])
            self.seed_entries.append(entry)

        update_button = tk.Button(
            self.players_frame, text="Update Bracket",
            command=self.update_bracket_with_names
        )
        update_button.grid(row=4, column=0, columnspan=4, pady=5)

        # 2) Bracket data structures.
        # (Winners and Losers bracket dictionaries remain unchanged except each match now has a "winner" key.)
        self.winners = {
            'round1': [ new_match() for _ in range(4) ],
            'round2': [ new_match() for _ in range(2) ],
            'final':  [ new_match() for _ in range(1) ],
            'grand_final': [ new_match() for _ in range(1) ],
            'reset':  [ new_match() for _ in range(1) ]
        }
        self.losers = {
            'round1': [ new_match() for _ in range(2) ],
            'round2': [ new_match() for _ in range(2) ],
            'round3': [ new_match() for _ in range(1) ],
            'round4': [ new_match() for _ in range(1) ]
        }

        self.winners_labels = {}
        self.losers_labels = {}

        # 3) Build the UI layout.
        self.build_bracket_layout()
        self.update_ui()

    def build_bracket_layout(self):
        """Creates bracket panels for Winners (top) and Losers (bottom) horizontally.
           Each match panel now has an extra 'Edit' button for manual control.
        """
        # Winners bracket frame:
        self.winners_frame = tk.LabelFrame(
            self, text="Winners Bracket", bg="#fafafa",
            font=("Arial", 14, "bold"), labelanchor='n', bd=5, padx=5, pady=5
        )
        self.winners_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nw")

        winners_rounds = ['round1','round2','final','grand_final','reset']
        for col_index, round_name in enumerate(winners_rounds):
            rf = tk.LabelFrame(
                self.winners_frame,
                text=self.pretty_round_name(round_name, winners=True),
                bg="#fafafa", font=("Arial", 12, "bold"), labelanchor='n',
                bd=2, padx=5, pady=5
            )
            rf.grid(row=0, column=col_index, padx=10, pady=5, sticky="n")
            for match_index, match in enumerate(self.winners[round_name]):
                # Match label
                m_lbl = tk.Label(rf, text=self.match_text(match), bg="#ffffff", relief="ridge",
                                 width=24, font=("Arial", 10))
                m_lbl.grid(row=match_index*2, column=0, columnspan=3, pady=(5,0))
                self.winners_labels[(round_name, match_index)] = m_lbl

                # Win buttons:
                b1 = tk.Button(rf, text="Win #1",
                               command=lambda rn=round_name, mi=match_index, w=0: self.set_winner('winners', rn, mi, w))
                b1.grid(row=match_index*2+1, column=0, padx=2, pady=(0,5), sticky="e")
                b2 = tk.Button(rf, text="Win #2",
                               command=lambda rn=round_name, mi=match_index, w=1: self.set_winner('winners', rn, mi, w))
                b2.grid(row=match_index*2+1, column=1, padx=2, pady=(0,5), sticky="w")
                # Manual edit button:
                b_edit = tk.Button(rf, text="Edit",
                                  command=lambda rn=round_name, mi=match_index, bt='winners': self.edit_match(bt, rn, mi))
                b_edit.grid(row=match_index*2+1, column=2, padx=2, pady=(0,5))
                
        # Losers bracket frame:
        self.losers_frame = tk.LabelFrame(
            self, text="Losers Bracket", bg="#f0faff",
            font=("Arial", 14, "bold"), labelanchor='n', bd=5, padx=5, pady=5
        )
        self.losers_frame.grid(row=2, column=0, padx=10, pady=10, sticky="sw")

        losers_rounds = list(self.losers.keys())
        for col_index, round_name in enumerate(losers_rounds):
            rf = tk.LabelFrame(
                self.losers_frame,
                text=self.pretty_round_name(round_name, winners=False),
                bg="#f0faff", font=("Arial", 12, "bold"), labelanchor='n',
                bd=2, padx=5, pady=5
            )
            rf.grid(row=0, column=col_index, padx=10, pady=5, sticky="n")
            for match_index, match in enumerate(self.losers[round_name]):
                m_lbl = tk.Label(rf, text=self.match_text(match), bg="#ffffff", relief="ridge",
                                 width=24, font=("Arial", 10))
                m_lbl.grid(row=match_index*2, column=0, columnspan=3, pady=(5,0))
                self.losers_labels[(round_name, match_index)] = m_lbl

                b1 = tk.Button(rf, text="Win #1",
                               command=lambda rn=round_name, mi=match_index, w=0: self.set_winner('losers', rn, mi, w))
                b1.grid(row=match_index*2+1, column=0, padx=2, pady=(0,5), sticky="e")
                b2 = tk.Button(rf, text="Win #2",
                               command=lambda rn=round_name, mi=match_index, w=1: self.set_winner('losers', rn, mi, w))
                b2.grid(row=match_index*2+1, column=1, padx=2, pady=(0,5), sticky="w")
                b_edit = tk.Button(rf, text="Edit",
                                  command=lambda rn=round_name, mi=match_index, bt='losers': self.edit_match(bt, rn, mi))
                b_edit.grid(row=match_index*2+1, column=2, padx=2, pady=(0,5))

    def match_text(self, match):
        """Returns formatted text for a match, including the winner and their score."""
        if match.get("winner"):
            # Show the winner and their score
            winner = match["winner"]
            winner_score = match["score1"] if match["p1"] == winner else match["score2"]
            return f"Winner: {winner} ({winner_score})"
        
        # Default match display
        p1 = match["p1"] if match["p1"] else "-"
        p2 = match["p2"] if match["p2"] else "-"
        s1 = f"({match['score1']})" if match["score1"] is not None else ""
        s2 = f"({match['score2']})" if match["score2"] is not None else ""
        return f"{p1} {s1} vs {p2} {s2}"

    def update_bracket_with_names(self):
        """Seeds Winners Round1 with the edited names."""
        seeds = [entry.get() for entry in self.seed_entries]
        if len(seeds) < 8:
            return
        self.winners['round1'][0] = {"p1": seeds[0], "p2": seeds[1], "score1": None, "score2": None}
        self.winners['round1'][1] = {"p1": seeds[2], "p2": seeds[3], "score1": None, "score2": None}
        self.winners['round1'][2] = {"p1": seeds[4], "p2": seeds[5], "score1": None, "score2": None}
        self.winners['round1'][3] = {"p1": seeds[6], "p2": seeds[7], "score1": None, "score2": None}

        # Clear future winners rounds:
        for r in ['round2', 'final', 'grand_final', 'reset']:
            for m in self.winners[r]:
                m["p1"] = None; m["p2"] = None; m["score1"] = None; m["score2"] = None
        # Clear all losers rounds:
        for rnd, matches in self.losers.items():
            for m in matches:
                m["p1"] = None; m["p2"] = None; m["score1"] = None; m["score2"] = None

        self.update_ui()

    def pretty_round_name(self, round_name, winners=True):
        mapping_winners = {
            'round1': "Winners Round 1",
            'round2': "Winners Semi-Final",
            'final':  "Winners Final",
            'grand_final': "Grand Final",
            'reset': "Reset Match"
        }
        mapping_losers = {
            'round1': "Losers Round 1",
            'round2': "Losers Round 2",
            'round3': "Losers Round 3",
            'round4': "Losers Final"
        }
        return mapping_winners.get(round_name, round_name) if winners else mapping_losers.get(round_name, round_name)

    # -------------------------------
    # Advancement Logic (as before, but now using dict fields)
    # -------------------------------
    # -------------------------------
    # Advancement Logic (modified for winner display)
    # -------------------------------
    # def set_winner(self, bracket_type, round_name, match_index, winner_index):
    #     if bracket_type == 'winners':
    #         match = self.winners[round_name][match_index]
    #     else:
    #         match = self.losers[round_name][match_index]

    #     if (not match["p1"]) or (not match["p2"]):
    #         messagebox.showerror("Error", "Match is not ready or incomplete!")
    #         return

    #     winner = match["p1"] if winner_index == 0 else match["p2"]
    #     loser = match["p2"] if winner_index == 0 else match["p1"]

    #     # Advance match as before…
    #     if bracket_type == 'winners':
    #         self.advance_in_winners(round_name, match_index, winner, loser, winner_index)
    #     else:
    #         self.advance_in_losers(round_name, match_index, winner, loser)

    #     # Set the match winner so that a little text appears.
    #     match["winner"] = winner
    #     # Clear out player names and scores (if you prefer to keep the winner visible, you may decide not to clear it fully)
    #     match["p1"] = None; match["p2"] = None; match["score1"] = None; match["score2"] = None
    #     self.update_ui()

    def set_winner(self, bracket_type, round_name, match_index, winner_index):
        """Sets the winner of a match and advances them in the bracket with their score."""
        if bracket_type == 'winners':
            match = self.winners[round_name][match_index]
        else:
            match = self.losers[round_name][match_index]

        if not match["p1"] or not match["p2"]:
            messagebox.showerror("Error", "Match is not ready or incomplete!")
            return

        # Determine winner and loser
        winner = match["p1"] if winner_index == 0 else match["p2"]
        loser = match["p2"] if winner_index == 0 else match["p1"]
        winner_score = f"{match["score1"]} - {match["score2"]}" if winner_index == 0 else f"{match["score2"]} - {match["score1"]}"
        
        # If the score is not set, default to 2-0
        if winner_score is None or winner_score == 'None - None':
            winner_score = "2-0"  # Defaulting to a 2-0 victory
            match["score1"] = "2-0" if winner_index == 0 else "0-2"
            match["score2"] = "0-2" if winner_index == 0 else "2-0"

        if bracket_type == 'winners':
            self.advance_in_winners(round_name, match_index, winner, loser, winner_index)
        else:
            self.advance_in_losers(round_name, match_index, winner, loser)

        # Set the match winner so that a little text appears.
        match["winner"] = winner
        # Clear out player names and scores (if you prefer to keep the winner visible, you may decide not to clear it fully)
        self.update_ui()

    # The remainder of the code (advance_in_winners, advance_in_losers, place_player_in_match, update_ui, edit_match, etc.)
    # remains unchanged from the previous version.

    def advance_in_winners(self, round_name, match_index, winner, loser, winner_index):
        if round_name == 'round1':
            next_match_idx = match_index // 2
            slot = match_index % 2
            self.place_player_in_match(self.winners['round2'], next_match_idx, winner, slot)
            self.place_player_in_match(self.losers['round1'], match_index // 2, loser, forced_slot=(match_index % 2))
        elif round_name == 'round2':
            next_match_idx = match_index // 2
            slot = match_index % 2
            self.place_player_in_match(self.winners['final'], next_match_idx, winner, slot)
            self.place_player_in_match(self.losers['round2'], match_index, loser, forced_slot=1)
        elif round_name == 'final':
            self.place_player_in_match(self.winners['grand_final'], 0, winner, match_index % 2)
            self.place_player_in_match(self.losers['round4'], 0, loser, forced_slot=1)
        elif round_name == 'grand_final':
            current_match = self.winners['grand_final'][0]
            if winner_index == 0:
                messagebox.showinfo("Tournament Over", f"{winner} is the Champion!")
                messagebox.showinfo("Runner-Up", f"{loser} takes 2nd place!")
            else:
                orig_winner = current_match["p1"]
                self.place_player_in_match(self.winners['reset'], 0, orig_winner, forced_slot=0)
                self.place_player_in_match(self.winners['reset'], 0, winner, forced_slot=1)
                messagebox.showinfo("Reset", "Losers side won the Grand Final! Reset match scheduled.")
        elif round_name == 'reset':
            if winner_index == 0:
                messagebox.showinfo("Tournament Over", f"{winner} is the Champion!")
                messagebox.showinfo("Runner-Up", f"{loser} takes 2nd place!")
            else:
                messagebox.showinfo("Tournament Over", f"{winner} is the Champion!")
                messagebox.showinfo("Runner-Up", f"{loser} takes 2nd place!")

    def advance_in_losers(self, round_name, match_index, winner, loser):
        if round_name == 'round1':
            self.place_player_in_match(self.losers['round2'], match_index, winner, forced_slot=0)
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")
        elif round_name == 'round2':
            placed = self.place_player_in_match(self.losers['round3'], 0, winner)
            if not placed:
                messagebox.showinfo("Eliminated", f"{winner} is eliminated!")
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")
        elif round_name == 'round3':
            self.place_player_in_match(self.losers['round4'], 0, winner, forced_slot=0)
            messagebox.showinfo("Eliminated", f"{loser} is eliminated!")
        elif round_name == 'round4':
            self.place_player_in_match(self.winners['grand_final'], 0, winner, forced_slot=1)
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
        # Update Winners bracket labels.
        for round_name, matches in self.winners.items():
            for i, match in enumerate(matches):
                lbl = self.winners_labels.get((round_name, i))
                if lbl:
                    lbl.config(text=self.match_text(match))
        # Update Losers bracket labels.
        for round_name, matches in self.losers.items():
            for i, match in enumerate(matches):
                lbl = self.losers_labels.get((round_name, i))
                if lbl:
                    lbl.config(text=self.match_text(match))

    # -------------------------------
    # Manual Edit Functionality
    # -------------------------------
    def edit_match(self, bracket_type, round_name, match_index):
        """Opens a pop-up allowing manual editing of a match's players and scores."""
        if bracket_type == 'winners':
            match = self.winners[round_name][match_index]
        else:
            match = self.losers[round_name][match_index]

        editor = tk.Toplevel(self)
        editor.title(f"Edit {bracket_type.capitalize()} {self.pretty_round_name(round_name, bracket_type=='winners')} Match {match_index+1}")
        editor.grab_set()  # Make the pop-up modal

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
            # Try to convert scores to int if possible, else leave as None
            try:
                match["score1"] = int(s1_entry.get())
            except:
                match["score1"] = None
            try:
                match["score2"] = int(s2_entry.get())
            except:
                match["score2"] = None
            self.update_ui()
            editor.destroy()

        save_btn = tk.Button(editor, text="Save", command=save_changes)
        save_btn.grid(row=2, column=0, columnspan=4, pady=10)

if __name__ == "__main__":
    app = HorizontalTop8Bracket()
    app.mainloop()
