import tkinter as tk
from tkinter import ttk, messagebox
import random
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


plt.rcParams['figure.facecolor'] = '#0A0E27'
plt.rcParams['axes.facecolor'] = '#0D1B2A'


class Node:
    def __init__(self, atom_id, decay_step):
        self.atom_id = atom_id
        self.decay_step = decay_step
        self.next = None


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


ISOTOPES = {
    "Carbon-14": {"half_life": 5730, "atoms": 1000, "steps": 20000, "unit": "years"},
    "Uranium-238": {"half_life": 4.468e9, "atoms": 1000, "steps": 15000000000, "unit": "years"},
    "Plutonium-239": {"half_life": 24110, "atoms": 1000, "steps": 80000, "unit": "years"},
    "Iodine-131": {"half_life": 8.02, "atoms": 1000, "steps": 30, "unit": "days"},
    "Cobalt-60": {"half_life": 5.27, "atoms": 1000, "steps": 20, "unit": "years"},
    "Radium-226": {"half_life": 1600, "atoms": 1000, "steps": 6000, "unit": "years"},
    "Radon-222": {"half_life": 3.82, "atoms": 1000, "steps": 15, "unit": "days"},
    "Strontium-90": {"half_life": 28.8, "atoms": 1000, "steps": 100, "unit": "years"},
    "Cesium-137": {"half_life": 30.17, "atoms": 1000, "steps": 100, "unit": "years"},
    "Tritium (H-3)": {"half_life": 12.32, "atoms": 1000, "steps": 50, "unit": "years"},
    "Custom": {"half_life": None, "atoms": 1000, "steps": 50, "unit": "time units"}
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
        self.current_isotope = None

    def calculate_decay_probability(self, half_life):
        if half_life <= 0:
            raise ValueError("Half-life must be positive")
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
    def __init__(self, parent, text, command, bg_color="#00FF41", hover_color="#00CC33", **kwargs):
        super().__init__(parent, height=45,
                         bg=parent['bg'], highlightthickness=0, **kwargs)
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text = text

        self.bind("<Configure>", lambda e: self.draw_button(self.bg_color))
        self.draw_button(bg_color)

        self.bind("<Enter>", lambda e: self.on_hover())
        self.bind("<Leave>", lambda e: self.on_leave())
        self.bind("<Button-1>", lambda e: self.on_click())

    def draw_button(self, color):
        self.delete("all")
        width = self.winfo_width() or 200
        height = 45

        self.create_rounded_rect(
            2, 2, width-2, height-2, radius=12, fill=color, outline="")

        self.create_text(width//2, height//2, text=self.text, fill="#0A0E27",
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

        self.colors = {
            'bg': '#0A0E27',  # Dark background
            'panel1': '#1A0B2E',  # Deep purple panel
            'panel2': '#16213E',  # Dark blue panel
            'panel3': '#0F3460',  # Medium blue panel
            'accent': '#00FF41',  # Neon green
            'success': '#39FF14',  # Neon lime
            'danger': '#FF006E',  # Neon pink
            'warning': '#FFFF00',  # Neon yellow
            'info': '#00D9FF',  # Neon cyan
            'text': '#FFFFFF',  # White text
            'text_neon': '#00FF41',  # Neon green text
            'border_neon': '#FF006E',  # Neon pink border
            'glow': '#8A2BE2'  # Purple glow
        }

        self.root.configure(bg=self.colors['bg'])
        self.simulator = RadioactiveDecaySimulator()

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')

        style.configure('Card.TFrame', background=self.colors['panel1'],
                        relief='flat', borderwidth=0)
        style.configure('Main.TFrame', background=self.colors['bg'])

        style.configure('Title.TLabel', background=self.colors['panel1'],
                        foreground=self.colors['text'], font=('Segoe UI', 11, 'bold'))
        style.configure('Header.TLabel', background=self.colors['bg'],
                        foreground=self.colors['text'], font=('Segoe UI', 16, 'bold'))
        style.configure('Subtitle.TLabel', background=self.colors['panel1'],
                        foreground=self.colors['info'], font=('Segoe UI', 9))

        style.configure('Modern.TEntry',
                        fieldbackground='#1E2749',
                        foreground='#FFFFFF',
                        borderwidth=2,
                        insertcolor='#00FF41')
        style.map('Modern.TEntry',
                  fieldbackground=[('readonly', '#2A3654')],
                  foreground=[('readonly', '#AAAAAA')])

        style.configure('Modern.TCombobox',
                        fieldbackground='#1E2749',
                        foreground='#FFFFFF',
                        borderwidth=2,
                        arrowcolor='#00FF41')
        style.map('Modern.TCombobox',
                  fieldbackground=[('readonly', '#1E2749')],
                  selectbackground=[('readonly', '#0F3460')])

        style.configure('Card.TLabelframe', background=self.colors['panel1'],
                        foreground=self.colors['text_neon'], borderwidth=0,
                        font=('Segoe UI', 12, 'bold'))
        style.configure('Card.TLabelframe.Label', background=self.colors['panel1'],
                        foreground=self.colors['text_neon'], font=('Segoe UI', 12, 'bold'))

    def create_card(self, parent, title=None, panel_color='panel1'):
        """Create a modern card-style container with neon borders"""
        card = tk.Frame(parent, bg=self.colors[panel_color],
                        relief='flat', borderwidth=0)
        card.configure(highlightbackground=self.colors['border_neon'],
                       highlightthickness=2, highlightcolor=self.colors['accent'])

        if title:
            title_label = tk.Label(card, text=title, bg=self.colors[panel_color],
                                   fg=self.colors['text_neon'], font=(
                                       'Segoe UI', 13, 'bold'),
                                   anchor='w')
            title_label.pack(fill='x', padx=20, pady=(15, 10))

        return card

    def setup_ui(self):

        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        header_frame = tk.Frame(main_container, bg=self.colors['bg'])
        header_frame.pack(fill='x', pady=(0, 15))

        title = tk.Label(header_frame, text="☢ RADIOACTIVE DECAY SIMULATOR",
                         bg=self.colors['bg'], fg=self.colors['accent'],
                         font=('Segoe UI', 20, 'bold'))
        title.pack(anchor='w')

        subtitle = tk.Label(header_frame,
                            text="Explore how radioactive isotopes decay over time through interactive simulation",
                            bg=self.colors['bg'], fg=self.colors['info'],
                            font=('Segoe UI', 10))
        subtitle.pack(anchor='w', pady=(5, 0))

        content = tk.Frame(main_container, bg=self.colors['bg'])
        content.pack(fill='both', expand=True)

        left_column = tk.Frame(content, bg=self.colors['bg'])
        left_column.pack(side='left', fill='both', padx=(0, 10))

        self.setup_controls(left_column)

        right_column = tk.Frame(content, bg=self.colors['bg'])
        right_column.pack(side='left', fill='both', expand=True)

        self.setup_visualization(right_column)

    def setup_controls(self, parent):

        params_card = self.create_card(
            parent, "SIMULATION PARAMETERS", 'panel1')
        params_card.pack(fill='x', pady=(0, 15))

        params_content = tk.Frame(params_card, bg=self.colors['panel1'])
        params_content.pack(fill='x', padx=20, pady=(0, 20))

        self.create_input_row(
            params_content, "Select Isotope", 0, is_combobox=True)

        self.rec_label = tk.Label(params_content, text="", bg=self.colors['panel1'],
                                  fg=self.colors['warning'], font=(
                                      'Segoe UI', 8, 'italic'),
                                  justify='left')
        self.rec_label.pack(fill='x', pady=(0, 10))

        self.create_input_row(params_content, "Half-life", 1)

        self.create_input_row(
            params_content, "Number of Atoms", 2, default="1000")

        self.create_input_row(
            params_content, "Simulation Steps", 3, default="50")

        button_frame = tk.Frame(params_card, bg=self.colors['panel1'])
        button_frame.pack(fill='x', padx=20, pady=(10, 20))

        run_btn = ModernButton(button_frame, "▶ RUN SIMULATION",
                               self.run_simulation, bg_color=self.colors['accent'],
                               hover_color=self.colors['success'], width=300)
        run_btn.pack()

        info_card = self.create_card(parent, "QUICK INFO", 'panel2')
        info_card.pack(fill='both', expand=True)

        info_content = tk.Frame(info_card, bg=self.colors['panel2'])
        info_content.pack(fill='both', expand=True, padx=20, pady=(0, 20))

        info_text = (
            "📚 About Half-Life:\n"
            "The time required for half of the radioactive atoms to decay.\n\n"
            "🔬 How it works:\n"
            "Each atom has a probability of decaying at each time step based on the isotope's half-life.\n\n"

        )

        info_label = tk.Label(info_content, text=info_text,
                              bg=self.colors['panel2'], fg=self.colors['text'],
                              font=('Segoe UI', 9), justify='left', anchor='nw')
        info_label.pack(fill='both', expand=True)

    def create_input_row(self, parent, label_text, row, is_combobox=False, default=""):
        row_frame = tk.Frame(parent, bg=self.colors['panel1'])
        row_frame.pack(fill='x', pady=10)

        # Label with neon color
        label = tk.Label(row_frame, text=label_text, bg=self.colors['panel1'],
                         fg=self.colors['info'], font=('Segoe UI', 10, 'bold'),
                         anchor='w', width=18)
        label.pack(side='left')

        # Input field
        if is_combobox and label_text == "Select Isotope":
            self.isotope_var = tk.StringVar()
            combo = ttk.Combobox(row_frame, textvariable=self.isotope_var,
                                 values=list(ISOTOPES.keys()), width=25,
                                 state="readonly", font=('Segoe UI', 10),
                                 style='Modern.TCombobox')
            combo.pack(side='left', fill='x', expand=True)
            combo.current(0)
            combo.bind("<<ComboboxSelected>>", self.on_isotope_selected)

        elif label_text == "Half-life":
            input_frame = tk.Frame(row_frame, bg=self.colors['panel1'])
            input_frame.pack(side='left', fill='x', expand=True)

            self.halflife_var = tk.StringVar(
                value=str(ISOTOPES["Carbon-14"]["half_life"]))
            self.halflife_entry = ttk.Entry(input_frame, textvariable=self.halflife_var,
                                            width=15, font=('Segoe UI', 10),
                                            style='Modern.TEntry')
            self.halflife_entry.pack(side='left', padx=(0, 5))
            self.halflife_entry.config(state="readonly")

            self.halflife_unit_label = tk.Label(input_frame, text="years",
                                                bg=self.colors['panel1'],
                                                fg=self.colors['warning'],
                                                font=('Segoe UI', 9, 'bold'))
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
                              font=('Segoe UI', 10), style='Modern.TEntry')
            entry.pack(side='left', fill='x', expand=True)

    def setup_visualization(self, parent):

        stats_frame = tk.Frame(parent, bg=self.colors['bg'])
        stats_frame.pack(fill='x', pady=(0, 15))

        self.stats_cards = {}
        stats_info = [
            ("REMAINING", "atoms_remaining", self.colors['success'], 'panel1'),
            ("DECAYED", "atoms_decayed", self.colors['danger'], 'panel2'),
            ("PROGRESS", "decay_percent", self.colors['info'], 'panel3')
        ]

        for i, (title, key, color, panel) in enumerate(stats_info):
            card = self.create_stat_card(stats_frame, title, "—", color, panel)
            card.pack(side='left', fill='x', expand=True,
                      padx=(0, 10 if i < 2 else 0))
            self.stats_cards[key] = card

        viz_card = self.create_card(parent, "DECAY VISUALIZATION", 'panel3')
        viz_card.pack(fill='both', expand=True)

        viz_content = tk.Frame(viz_card, bg=self.colors['panel3'])
        viz_content.pack(fill='both', expand=True, padx=15, pady=(0, 15))

        self.figure = Figure(figsize=(10, 6), dpi=100,
                             facecolor=self.colors['panel3'])
        self.canvas = FigureCanvasTkAgg(self.figure, master=viz_content)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)

        self.draw_empty_plot()

    def create_stat_card(self, parent, title, value, color, panel_color):
        card = tk.Frame(parent, bg=self.colors[panel_color], relief='flat',
                        highlightbackground=color,
                        highlightthickness=3)

        content = tk.Frame(card, bg=self.colors[panel_color])
        content.pack(fill='both', expand=True, padx=20, pady=15)

        title_label = tk.Label(content, text=title, bg=self.colors[panel_color],
                               fg=self.colors['text'], font=('Segoe UI', 9, 'bold'))
        title_label.pack(anchor='w')

        value_label = tk.Label(content, text=value, bg=self.colors[panel_color],
                               fg=color, font=('Segoe UI', 22, 'bold'))
        value_label.pack(anchor='w', pady=(5, 0))

        card.value_label = value_label
        return card

    def draw_empty_plot(self):
        self.figure.clear()
        ax = self.figure.add_subplot(111, facecolor=self.colors['panel3'])
        ax.text(0.5, 0.5, '▶ RUN A SIMULATION TO SEE RESULTS',
                ha='center', va='center', fontsize=14, color=self.colors['accent'],
                transform=ax.transAxes, weight='bold')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(self.colors['border_neon'])
            spine.set_linewidth(2)
        self.canvas.draw()

    def on_isotope_selected(self, event):
        selected = self.isotope_var.get()
        isotope_data = ISOTOPES[selected]

        if selected == "Custom":
            self.halflife_entry.config(state="normal")
            self.halflife_var.set("")
            self.halflife_unit_label.config(text=isotope_data["unit"])
            self.atoms_var.set(str(isotope_data["atoms"]))
            self.steps_var.set(str(isotope_data["steps"]))
            self.rec_label.config(text="")
        else:
            self.halflife_entry.config(state="readonly")
            half_life = isotope_data["half_life"]

            if half_life >= 1e6:
                display_value = f"{half_life:.3e}"
            elif half_life >= 1000:
                display_value = f"{half_life:,.0f}"
            else:
                display_value = f"{half_life:.2f}"

            self.halflife_var.set(display_value)
            self.halflife_unit_label.config(text=isotope_data["unit"])

            self.atoms_var.set(str(isotope_data["atoms"]))
            self.steps_var.set(str(isotope_data["steps"]))

            self.rec_label.config(
                text=f"✓ Recommended: {isotope_data['atoms']:,} atoms × {isotope_data['steps']:,} steps"
            )

    def run_simulation(self):
        try:
            num_atoms = int(self.atoms_var.get())
            num_steps = int(self.steps_var.get())
            half_life_str = self.halflife_var.get()

            half_life_str = half_life_str.replace(',', '')
            half_life = float(half_life_str)

            if num_atoms <= 0 or num_steps <= 0 or half_life <= 0:
                messagebox.showerror("Invalid Input",
                                     "All values must be positive numbers!")
                return

            time_steps, remaining, decayed = self.simulator.run_simulation(
                num_atoms, half_life, num_steps)

            self.update_stats(remaining[-1], decayed[-1], num_atoms)

            self.visualize_decay(time_steps, remaining, decayed)

        except ValueError as e:
            messagebox.showerror("Invalid Input",
                                 f"Please enter valid numeric values!\nError: {str(e)}")
        except Exception as e:
            messagebox.showerror("Simulation Error",
                                 f"An error occurred during simulation:\n{str(e)}")

    def update_stats(self, remaining, decayed, total):
        self.stats_cards['atoms_remaining'].value_label.config(
            text=f"{remaining:,}")
        self.stats_cards['atoms_decayed'].value_label.config(
            text=f"{decayed:,}")
        decay_percent = (decayed/total)*100 if total > 0 else 0
        self.stats_cards['decay_percent'].value_label.config(
            text=f"{decay_percent:.1f}%")

    def visualize_decay(self, time_steps, remaining, decayed):
        self.figure.clear()

        ax1 = self.figure.add_subplot(2, 1, 1, facecolor='#0D1B2A')
        ax2 = self.figure.add_subplot(2, 1, 2, facecolor='#0D1B2A')

        ax1.plot(time_steps, remaining, color=self.colors['success'],
                 linewidth=3, label='Remaining Atoms', marker='o',
                 markersize=5, alpha=0.9, markevery=max(1, len(time_steps)//20))
        ax1.plot(time_steps, decayed, color=self.colors['danger'],
                 linewidth=3, label='Decayed Atoms', marker='s',
                 markersize=5, alpha=0.9, markevery=max(1, len(time_steps)//20))

        ax1.fill_between(time_steps, remaining, alpha=0.3,
                         color=self.colors['success'])
        ax1.fill_between(time_steps, decayed, alpha=0.3,
                         color=self.colors['danger'])

        ax1.set_xlabel('Time Step', fontsize=10,
                       color=self.colors['text'], weight='bold')
        ax1.set_ylabel('Number of Atoms', fontsize=10,
                       color=self.colors['text'], weight='bold')
        ax1.set_title('Radioactive Decay Over Time', fontsize=12,
                      fontweight='bold', color=self.colors['accent'], pad=15)
        ax1.legend(loc='best', frameon=True, shadow=False, fontsize=9,
                   facecolor='#0D1B2A', edgecolor=self.colors['border_neon'],
                   labelcolor=self.colors['text'])
        ax1.grid(True, alpha=0.3, linestyle='--', color=self.colors['info'])
        ax1.tick_params(colors=self.colors['text'])
        for spine in ax1.spines.values():
            spine.set_color(self.colors['border_neon'])
            spine.set_linewidth(1.5)

        decay_per_step = [decayed[i] - decayed[i-1]
                          if i > 0 else 0 for i in range(len(decayed))]

        bars = ax2.bar(time_steps, decay_per_step, color=self.colors['info'],
                       alpha=0.8, edgecolor=self.colors['accent'], linewidth=1.5)

        ax2.set_xlabel('Time Step', fontsize=10,
                       color=self.colors['text'], weight='bold')
        ax2.set_ylabel('Atoms Decayed', fontsize=10,
                       color=self.colors['text'], weight='bold')
        ax2.set_title('Decay Rate per Time Step', fontsize=12,
                      fontweight='bold', color=self.colors['warning'], pad=15)
        ax2.grid(True, alpha=0.3, axis='y',
                 linestyle='--', color=self.colors['info'])
        ax2.tick_params(colors=self.colors['text'])
        for spine in ax2.spines.values():
            spine.set_color(self.colors['border_neon'])
            spine.set_linewidth(1.5)

        self.figure.tight_layout()
        self.canvas.draw()


def main():
    root = tk.Tk()
    app = DecayVisualizerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
