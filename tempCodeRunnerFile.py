import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# LinkedList Node for tracking decayed atoms


class Node:
    def __init__(self, atom_id, decay_step):
        self.atom_id = atom_id
        self.decay_step = decay_step
        self.next = None

# LinkedList to track decay sequence


class DecayLinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, atom_id, decay_step):
        new_node = Node(atom_id, decay_step)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def get_decay_count_at_step(self, step):
        count = 0
        current = self.head
        while current:
            if current.decay_step == step:
                count += 1
            current = current.next
        return count

    def get_all_decays(self):
        decays = []
        current = self.head
        while current:
            decays.append((current.atom_id, current.decay_step))
            current = current.next
        return decays


# Predefined radioactive isotopes
ISOTOPES = {
    "Carbon-14": 5730,
    "Uranium-238": 4.468e9,
    "Plutonium-239": 24110,
    "Iodine-131": 8.02,
    "Cobalt-60": 5.27,
    "Radium-226": 1600,
    "Radon-222": 3.82,
    "Strontium-90": 28.8,
    "Cesium-137": 30.17,
    "Tritium (H-3)": 12.32,
    "Custom": None
}


class RadioactiveDecaySimulator:
    def __init__(self):
        self.atoms = []
        self.decay_list = DecayLinkedList()
        self.remaining_atoms = []
        self.decayed_atoms = []
        self.time_steps = []

    def initialize(self, num_atoms):
        self.atoms = [{'id': i, 'decayed': False} for i in range(num_atoms)]
        self.decay_list = DecayLinkedList()
        self.remaining_atoms = [num_atoms]
        self.decayed_atoms = [0]
        self.time_steps = [0]

    def calculate_decay_probability(self, half_life):
        decay_constant = math.log(2) / half_life
        return 1 - math.exp(-decay_constant)

    def simulate_step(self, step, decay_prob):
        newly_decayed = 0
        for atom in self.atoms:
            if not atom['decayed']:
                if random.random() < decay_prob:
                    atom['decayed'] = True
                    self.decay_list.append(atom['id'], step)
                    newly_decayed += 1

        remaining = sum(1 for atom in self.atoms if not atom['decayed'])
        decayed = len(self.atoms) - remaining

        self.remaining_atoms.append(remaining)
        self.decayed_atoms.append(decayed)
        self.time_steps.append(step)

        return remaining, decayed

    def run_simulation(self, num_atoms, half_life, num_steps):
        self.initialize(num_atoms)
        decay_prob = self.calculate_decay_probability(half_life)

        for step in range(1, num_steps + 1):
            remaining, decayed = self.simulate_step(step, decay_prob)
            if remaining == 0:
                break

        return self.time_steps, self.remaining_atoms, self.decayed_atoms


class ModernButton(tk.Canvas):
    def __init__(self, parent, text, command, bg_color="#4A90E2", hover_color="#357ABD", **kwargs):
        super().__init__(parent, height=45,
                         bg=parent['bg'], highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text

        self.draw_button(bg_color)

        self.bind("<Enter>", lambda e: self.on_hover())
        self.bind("<Leave>", lambda e: self.on_leave())
        self.bind("<Button-1>", lambda e: self.on_click())

    def draw_button(self, color):
        self.delete("all")
        width = self.winfo_reqwidth() or 200
        height = 45

        # Rounded rectangle
        self.create_rounded_rect(
            2, 2, width-2, height-2, radius=12, fill=color, outline="")

        # Text
        self.create_text(width//2, height//2, text=self.text, fill="white",
                         font=("Segoe UI", 11, "bold"))

    def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [x1+radius, y1,
                  x2-radius, y1,
                  x2, y1,
                  x2, y1+radius,
                  x2, y2-radius,
                  x2, y2,
                  x2-radius, y2,
                  x1+radius, y2,
                  x1, y2,
                  x1, y2-radius,
                  x1, y1+radius,
                  x1, y1]
        return self.create_polygon(points, smooth=True, **kwargs)

    def on_hover(self):
        self.draw_button(self.hover_color)

    def on_leave(self):
        self.draw_button(self.bg_color)

    def on_click(self):
        if self.command:
            self.command()


class DecayVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Radioactive Decay Visualizer")
        self.root.geometry("1400x900")

        # Modern color scheme
        self.colors = {
            'bg': '#F5F7FA',
            'panel': '#FFFFFF',
            'accent': '#4A90E2',
            'success': '#5CB85C',
            'danger': '#E74C3C',
            'text': '#2C3E50',
            'text_light': '#7F8C8D',
            'border': '#E1E8ED'
        }

        self.root.configure(bg=self.colors['bg'])
        self.simulator = RadioactiveDecaySimulator()

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        # Configure frame styles
        style.configure('Card.TFrame', background=self.colors['panel'],
                        relief='flat', borderwidth=0)
        style.configure('Main.TFrame', background=self.colors['bg'])

        # Configure label styles
        style.configure('Title.TLabel', background=self.colors['panel'],
                        foreground=self.colors['text'], font=('Segoe UI', 11, 'bold'))
        style.configure('Header.TLabel', background=self.colors['bg'],
                        foreground=self.colors['text'], font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['panel'],
                        foreground=self.colors['text_light'], font=('Segoe UI', 9))

        # Configure entry and combobox
        style.configure('Modern.TEntry', fieldbackground='white',
                        borderwidth=1, relief='solid')
        style.configure('Modern.TCombobox', fieldbackground='white',
                        borderwidth=1, relief='solid')

        # Configure labelframe
        style.configure('Card.TLabelframe', background=self.colors['panel'],
                        foreground=self.colors['text'], borderwidth=0,
                        font=('Segoe UI', 12, 'bold'))
        style.configure('Card.TLabelframe.Label', background=self.colors['panel'],
                        foreground=self.colors['text'], font=('Segoe UI', 12, 'bold'))

    def create_card(self, parent, title=None):
        """Create a modern card-style container"""
        card = tk.Frame(parent, bg=self.colors['panel'],
                        relief='flat', borderwidth=0)
        card.configure(highlightbackground=self.colors['border'],
                       highlightthickness=1, highlightcolor=self.colors['border'])

        if title:
            title_label = tk.Label(card, text=title, bg=self.colors['panel'],
                                   fg=self.colors['text'], font=(
                                       'Segoe UI', 13, 'bold'),
                                   anchor='w')
            title_label.pack(fill='x', padx=20, pady=(15, 10))

        return card

    def setup_ui(self):
        # Main container with padding
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        # Header
        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 15))

        title = tk.Label(header_frame, text="☢ Radioactive Decay Simulator",
                         bg=self.colors['bg'], fg=self.colors['text'],
                         font=('Segoe UI', 20, 'bold'))
        title.pack(anchor='w')

        subtitle = tk.Label(header_frame,
                            text="Explore how radioactive isotopes decay over time through interactive simulation",
                            bg=self.colors['bg'], fg=self.colors['text_light'],
                            font=('Segoe UI', 10))
        subtitle.pack(anchor='w', pady=(5, 0))

        # Content area with grid
        content = tk.Frame(main_container, bg=self.colors['bg'])
        content.pack(fill='both', expand=True)

        # Left column - Controls
        left_column = tk.Frame(content, bg=self.colors['bg'])
        left_column.pack(side='left', fill='both', padx=(0, 10))

        self.setup_controls(left_column)

        # Right column - Results and Visualization
        right_column = tk.Frame(content, bg=self.colors['bg'])
        right_column.pack(side='left', fill='both', expand=True)

        self.setup_visualization(right_column)

    def setup_controls(self, parent):
        # Parameters Card
        params_card = self.create_card(parent, "Simulation Parameters")
        params_card.pack(fill='x', pady=(0, 15))

        params_content = tk.Frame(params_card, bg=self.colors['panel'])
        params_content.pack(fill='x', padx=20, pady=(0, 20))

        # Isotope Selection
        self.create_input_row(
            params_content, "Select Isotope", 0, is_combobox=True)

        # Half-life
        self.create_input_row(params_content, "Half-life", 1)

        # Number of atoms
        self.create_input_row(
            params_content, "Number of Atoms", 2, default="1000")

        # Simulation steps
        self.create_input_row(
            params_content, "Simulation Steps", 3, default="50")

        # Run button
        button_frame = tk.Frame(params_card, bg=self.colors['panel'])
        button_frame.pack(fill='x', padx=20, pady=(10, 20))

        run_btn = ModernButton(button_frame, "▶ Run Simulation",
                               self.run_simulation, bg_color=self.colors['accent'],
                               hover_color='#357ABD', width=300)
        run_btn.pack()

        # Info Card
        info_card = self.create_card(parent, "Quick Info")
        info_card.pack(fill='both', expand=True)

        info_content = tk.Frame(info_card, bg=self.colors['panel'])
        info_content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        info_text = (
            "📚 About Half-Life:\n"
            "The time required for half of the radioactive atoms to decay.\n\n"
            "🔬 How it works:\n"
            "Each atom has a probability of decaying at each time step based on the isotope's half-life.\n\n"
            "💡 Tips:\n"
            "• Try different isotopes to see varying decay rates\n"
            "• Increase atoms for smoother curves\n"
            "• More steps show longer-term behavior"
        )

        info_label = tk.Label(info_content, text=info_text,
                              bg=self.colors['panel'], fg=self.colors['text'],
                              font=('Segoe UI', 9), justify='left', anchor='nw')
        info_label.pack(fill='both', expand=True)

    def create_input_row(self, parent, label_text, row, is_combobox=False, default=""):
        row_frame = tk.Frame(parent, bg=self.colors['panel'])
        row_frame.pack(fill='x', pady=10)

        # Label
        label = tk.Label(row_frame, text=label_text, bg=self.colors['panel'],
                         fg=self.colors['text'], font=('Segoe UI', 10),
                         anchor='w', width=18)
        label.pack(side='left')

        # Input field
        if is_combobox and label_text == "Select Isotope":
            self.isotope_var = tk.StringVar()
            combo = ttk.Combobox(row_frame, textvariable=self.isotope_var,
                                 values=list(ISOTOPES.keys()), width=25,
                                 state="readonly", font=('Segoe UI', 10))
            combo.pack(side='left', fill='x', expand=True)
            combo.current(0)
            combo.bind("<<ComboboxSelected>>", self.on_isotope_selected)

        elif label_text == "Half-life":
            input_frame = tk.Frame(row_frame, bg=self.colors['panel'])
            input_frame.pack(side='left', fill='x', expand=True)

            self.halflife_var = tk.StringVar(value=str(ISOTOPES["Carbon-14"]))
            self.halflife_entry = ttk.Entry(input_frame, textvariable=self.halflife_var,
                                            width=15, font=('Segoe UI', 10))
            self.halflife_entry.pack(side='left', padx=(0, 5))
            self.halflife_entry.config(state="readonly")

            self.halflife_unit_label = tk.Label(input_frame, text="years",
                                                bg=self.colors['panel'],
                                                fg=self.colors['text_light'],
                                                font=('Segoe UI', 9))
            self.halflife_unit_label.pack(side='left')

        else:
            if label_text == "Number of Atoms":
                self.atoms_var = tk.StringVar(value=default)
                var = self.atoms_var
            elif label_text == "Simulation Steps":
                self.steps_var = tk.StringVar(value=default)
                var = self.steps_var
            else:
                var = tk.StringVar(value=default)

            entry = ttk.Entry(row_frame, textvariable=var, width=25,
                              font=('Segoe UI', 10))
            entry.pack(side='left', fill='x', expand=True)

    def setup_visualization(self, parent):
        # Stats Cards Row
        stats_frame = tk.Frame(parent, bg=self.colors['bg'])
        stats_frame.pack(fill='x', pady=(0, 15))

        self.stats_cards = {}
        stats_info = [
            ("Remaining", "atoms_remaining", self.colors['success']),
            ("Decayed", "atoms_decayed", self.colors['danger']),
            ("Progress", "decay_percent", self.colors['accent'])
        ]

        for i, (title, key, color) in enumerate(stats_info):
            card = self.create_stat_card(stats_frame, title, "—", color)
            card.pack(side='left', fill='x', expand=True,
                      padx=(0, 10 if i < 2 else 0))
            self.stats_cards[key] = card

        # Visualization Card
        viz_card = self.create_card(parent, "Decay Visualization")
        viz_card.pack(fill='both', expand=True)

        viz_content = tk.Frame(viz_card, bg=self.colors['panel'])
        viz_content.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        self.figure = Figure(figsize=(10, 6), dpi=100,
                             facecolor=self.colors['panel'])
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_content)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        # Initial empty plot
        self.draw_empty_plot()

    def create_stat_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=self.colors['panel'], relief='flat',
                        highlightbackground=self.colors['border'],
                        highlightthickness=1)

        content = tk.Frame(card, bg=self.colors['panel'])
        content.pack(fill='both', expand=True, padx=20, pady=15)

        title_label = tk.Label(content, text=title, bg=self.colors['panel'],
                               fg=self.colors['text_light'], font=('Segoe UI', 9))
        title_label.pack(anchor='w')

        value_label = tk.Label(content, text=value, bg=self.colors['panel'],
                               fg=color, font=('Segoe UI', 22, 'bold'))
        value_label.pack(anchor='w', pady=(5, 0))

        card.value_label = value_label
        return card

    def draw_empty_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.text(0.5, 0.5, '▶ Run a simulation to see results',
                ha='center', va='center', fontsize=14, color=self.colors['text_light'],
                transform=ax.transAxes)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        self.canvas.draw()

    def on_isotope_selected(self, event):
        selected = self.isotope_var.get()
        if selected == "Custom":
            self.halflife_entry.config(state="normal")
            self.halflife_var.set("")
            self.halflife_unit_label.config(text="time units")
        else:
            self.halflife_entry.config(state="readonly")
            half_life = ISOTOPES[selected]
            self.halflife_var.set(str(half_life))

            if selected in ["Iodine-131", "Radon-222"]:
                unit = "days"
            else:
                unit = "years"
            self.halflife_unit_label.config(text=unit)

    def run_simulation(self):
        try:
            num_atoms = int(self.atoms_var.get())
            num_steps = int(self.steps_var.get())
            half_life = float(self.halflife_var.get())

            if num_atoms <= 0 or num_steps <= 0 or half_life <= 0:
                messagebox.showerror("Invalid Input",
                                     "All values must be positive numbers!")
                return

            # Run simulation
            time_steps, remaining, decayed = self.simulator.run_simulation(
                num_atoms, half_life, num_steps)

            # Update stats cards
            self.update_stats(remaining[-1], decayed[-1], num_atoms)

            # Visualize
            self.visualize_decay(time_steps, remaining, decayed)

        except ValueError:
            messagebox.showerror("Invalid Input",
                                 "Please enter valid numeric values!")

    def update_stats(self, remaining, decayed, total):
        self.stats_cards['atoms_remaining'].value_label.config(
            text=f"{remaining:,}")
        self.stats_cards['atoms_decayed'].value_label.config(
            text=f"{decayed:,}")
        self.stats_cards['decay_percent'].value_label.config(
            text=f"{(decayed/total)*100:.1f}%")

    def visualize_decay(self, time_steps, remaining, decayed):
        self.figure.clear()

        # Create two subplots with modern styling
        ax1 = self.figure.add_subplot(2, 1, 1, facecolor='white')
        ax2 = self.figure.add_subplot(2, 1, 2, facecolor='white')

        # Plot 1: Remaining vs Decayed
        ax1.plot(time_steps, remaining, color=self.colors['success'],
                 linewidth=2.5, label='Remaining Atoms', marker='o',
                 markersize=4, alpha=0.8)
        ax1.plot(time_steps, decayed, color=self.colors['danger'],
                 linewidth=2.5, label='Decayed Atoms', marker='s',
                 markersize=4, alpha=0.8)

        ax1.fill_between(time_steps, remaining, alpha=0.2,
                         color=self.colors['success'])
        ax1.fill_between(time_steps, decayed, alpha=0.2,
                         color=self.colors['danger'])

        ax1.set_xlabel('Time Step', fontsize=10, color=self.colors['text'])
        ax1.set_ylabel('Number of Atoms', fontsize=10,
                       color=self.colors['text'])
        ax1.set_title('Radioactive Decay Over Time', fontsize=12,
                      fontweight='bold', color=self.colors['text'], pad=15)
        ax1.legend(loc='best', frameon=True, shadow=True, fontsize=9)
        ax1.grid(True, alpha=0.2, linestyle='--')
        ax1.spines['top'].set_visible(False)
        ax1.spines['right'].set_visible(False)

        # Plot 2: Decay rate
        decay_per_step = [decayed[i] - decayed[i-1]
                          if i > 0 else 0 for i in range(len(decayed))]

        bars = ax2.bar(time_steps, decay_per_step, color=self.colors['accent'],
                       alpha=0.7, edgecolor=self.colors['accent'], linewidth=1.5)

        ax2.set_xlabel('Time Step', fontsize=10, color=self.colors['text'])
        ax2.set_ylabel('Atoms Decayed', fontsize=10, color=self.colors['text'])
        ax2.set_title('Decay Rate per Time Step', fontsize=12,
                      fontweight='bold', color=self.colors['text'], pad=15)
        ax2.grid(True, alpha=0.2, axis='y', linestyle='--')
        ax2.spines['top'].set_visible(False)
        ax2.spines['right'].set_visible(False)

        self.figure.tight_layout()
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = DecayVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
