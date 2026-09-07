"""
Dot Plot Visualizer for Sequence Alignment
Human vs Chicken Hemoglobin Beta Chain (HBB)
Pure Python - uses only the standard library (tkinter)
"""

import tkinter as tk
from tkinter import scrolledtext, messagebox

# Default protein sequences (single-letter amino acid code)
HUMAN_HBB = (
    "MVHLTPEEKSAVTALWGKVNVDEVGGEALGRLLVVYPWTQRFFESFGDLSTPDAVMGNPKVKAHGKKVL"
    "GAFSDGLAHLDNLKGTFATLSELHCDKLHVDPENFRLLGNVLVCVLAHHFGKEFTPPVQAAYQKVVAG"
    "VANALAHKYH"
)
CHICKEN_HBB = (
    "MVHWTAEEKQLITGLWGKVNVAECGAEALARLLIVYPWTQRFFASFGNLSSPTAILGNPMVRAHGKKVL"
    "TSFGDAVKNLDNIKNTFSQLSELHCDKLHVDPENFRLLGDILIIVLAAHFSKDFTPECQAAWQKLVRV"
    "VAHALARKYH"
)


class DotPlotApp:
    def __init__(self, root):
        self.root = root
        root.title("Dot Plot - Hemoglobin Beta Chain Alignment (Human vs Chicken)")
        root.geometry("1020x830")
        root.configure(bg="#f0f0f0")

        self.build_input_frame()
        self.build_controls_frame()
        self.build_canvas_frame()
        self.build_output_frame()

    # ---------- UI construction ----------
    def build_input_frame(self):
        frame = tk.LabelFrame(self.root, text="Sequences", bg="#f0f0f0",
                               font=("Arial", 10, "bold"))
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Sequence 1 (Human HBB):", bg="#f0f0f0").grid(
            row=0, column=0, sticky="w", padx=5, pady=2)
        self.seq1_entry = tk.Text(frame, height=3, width=110, wrap="char")
        self.seq1_entry.insert("1.0", HUMAN_HBB)
        self.seq1_entry.grid(row=1, column=0, padx=5, pady=2, columnspan=2)

        tk.Label(frame, text="Sequence 2 (Chicken HBB):", bg="#f0f0f0").grid(
            row=2, column=0, sticky="w", padx=5, pady=2)
        self.seq2_entry = tk.Text(frame, height=3, width=110, wrap="char")
        self.seq2_entry.insert("1.0", CHICKEN_HBB)
        self.seq2_entry.grid(row=3, column=0, padx=5, pady=2, columnspan=2)

    def build_controls_frame(self):
        frame = tk.LabelFrame(self.root, text="Options", bg="#f0f0f0",
                               font=("Arial", 10, "bold"))
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Window size:", bg="#f0f0f0").grid(
            row=0, column=0, padx=5, pady=5)
        self.window_var = tk.IntVar(value=1)
        tk.Spinbox(frame, from_=1, to=10, textvariable=self.window_var,
                   width=5).grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Stringency (matches req. in window):",
                 bg="#f0f0f0").grid(row=0, column=2, padx=5, pady=5)
        self.stringency_var = tk.IntVar(value=1)
        tk.Spinbox(frame, from_=1, to=10, textvariable=self.stringency_var,
                   width=5).grid(row=0, column=3, padx=5)

        tk.Label(frame, text="Min segment length to report:",
                 bg="#f0f0f0").grid(row=0, column=4, padx=5, pady=5)
        self.minseg_var = tk.IntVar(value=4)
        tk.Spinbox(frame, from_=2, to=20, textvariable=self.minseg_var,
                   width=5).grid(row=0, column=5, padx=5)

        tk.Button(frame, text="Generate Dot Plot", command=self.generate,
                  bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold")).grid(row=0, column=6, padx=15)

    def build_canvas_frame(self):
        frame = tk.LabelFrame(self.root, text="Dot Plot", bg="#f0f0f0",
                               font=("Arial", 10, "bold"))
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.canvas_size = 480  # used for the plain/dense mode (long sequences)

        # Canvas + scrollbars, so a big "detailed" grid for short sequences
        # can still be scrolled into view without shrinking the window.
        canvas_holder = tk.Frame(frame, bg="#f0f0f0")
        canvas_holder.pack(fill="both", expand=True, padx=5, pady=5)

        self.canvas = tk.Canvas(canvas_holder, width=self.canvas_size + 60,
                                 height=self.canvas_size + 60, bg="white")
        vbar = tk.Scrollbar(canvas_holder, orient="vertical", command=self.canvas.yview)
        hbar = tk.Scrollbar(canvas_holder, orient="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=vbar.set, xscrollcommand=hbar.set)

        self.canvas.grid(row=0, column=0, sticky="nsew")
        vbar.grid(row=0, column=1, sticky="ns")
        hbar.grid(row=1, column=0, sticky="ew")
        canvas_holder.grid_rowconfigure(0, weight=1)
        canvas_holder.grid_columnconfigure(0, weight=1)

    def build_output_frame(self):
        frame = tk.LabelFrame(self.root, text="Identified Matching Segments",
                               bg="#f0f0f0", font=("Arial", 10, "bold"))
        frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.output_box = scrolledtext.ScrolledText(frame, height=8, wrap="word")
        self.output_box.pack(fill="both", expand=True, padx=5, pady=5)

    # ---------- Logic ----------
    def generate(self):
        seq1 = self.seq1_entry.get("1.0", "end").strip().upper().replace("\n", "").replace(" ", "")
        seq2 = self.seq2_entry.get("1.0", "end").strip().upper().replace("\n", "").replace(" ", "")

        if not seq1 or not seq2:
            messagebox.showerror("Error", "Please enter both sequences.")
            return

        window = self.window_var.get()
        stringency = min(self.stringency_var.get(), window)
        min_seg = self.minseg_var.get()

        self.draw_dot_plot(seq1, seq2, window, stringency)
        self.find_segments(seq1, seq2, min_seg)

    # Sequences at or below this length (in BOTH dimensions) get the
    # big, labeled, gridded "detailed" view instead of the dense dot cloud.
    DETAILED_MODE_MAX_LEN = 40
    CELL_SIZE = 26          # pixels per residue-cell in detailed mode
    DETAILED_MARGIN = 70    # room for axis letters in detailed mode

    def draw_dot_plot(self, seq1, seq2, window, stringency):
        n, m = len(seq1), len(seq2)
        if n <= self.DETAILED_MODE_MAX_LEN and m <= self.DETAILED_MODE_MAX_LEN:
            self._draw_detailed(seq1, seq2, window, stringency)
        else:
            self._draw_dense(seq1, seq2, window, stringency)

    def _draw_dense(self, seq1, seq2, window, stringency):
        """Compact dot-matrix for longer sequences: one tiny dot per match,
        no grid/labels (would be unreadable at this scale)."""
        self.canvas.delete("all")
        n, m = len(seq1), len(seq2)
        size = self.canvas_size
        margin = 45
        self.canvas.config(scrollregion=(0, 0, margin + size + 20, margin + size + 20))

        self.canvas.create_line(margin, margin, margin, margin + size, width=1)
        self.canvas.create_line(margin, margin + size, margin + size, margin + size, width=1)
        self.canvas.create_text(margin + size / 2, margin - 22,
                                 text="Sequence 1 (Human)  \u2192", font=("Arial", 9))
        self.canvas.create_text(16, margin + size / 2,
                                 text="Sequence 2\n(Chicken)\n\u2193", font=("Arial", 9))

        half = window // 2
        xscale = size / n
        yscale = size / m

        for i in range(n):
            for j in range(m):
                matches = 0
                for k in range(-half, window - half):
                    a, b = i + k, j + k
                    if 0 <= a < n and 0 <= b < m and seq1[a] == seq2[b]:
                        matches += 1
                if matches >= stringency:
                    x = margin + i * xscale
                    y = margin + j * yscale
                    self.canvas.create_oval(x, y, x + 1.6, y + 1.6,
                                             fill="black", outline="black")

    def _draw_detailed(self, seq1, seq2, window, stringency):
        """Large, gridded plot for short sequences: every cell is drawn,
        with the actual amino acid letters labeling both axes."""
        self.canvas.delete("all")
        n, m = len(seq1), len(seq2)
        cell = self.CELL_SIZE
        margin = self.DETAILED_MARGIN

        grid_w = n * cell
        grid_h = m * cell
        total_w = margin + grid_w + 20
        total_h = margin + grid_h + 20
        self.canvas.config(scrollregion=(0, 0, total_w, total_h))

        # axis titles
        self.canvas.create_text(margin + grid_w / 2, 15,
                                 text="Sequence 1 (Human)", font=("Arial", 10, "bold"))
        self.canvas.create_text(15, margin + grid_h / 2,
                                 text="Sequence 2\n(Chicken)", font=("Arial", 10, "bold"),
                                 justify="center")

        # column labels (top) - human residues
        for i, aa in enumerate(seq1):
            cx = margin + i * cell + cell / 2
            self.canvas.create_text(cx, margin - 15, text=aa, font=("Consolas", 11, "bold"))

        # row labels (left) - chicken residues
        for j, aa in enumerate(seq2):
            cy = margin + j * cell + cell / 2
            self.canvas.create_text(margin - 15, cy, text=aa, font=("Consolas", 11, "bold"))

        # grid lines
        for i in range(n + 1):
            x = margin + i * cell
            self.canvas.create_line(x, margin, x, margin + grid_h, fill="#cccccc")
        for j in range(m + 1):
            y = margin + j * cell
            self.canvas.create_line(margin, y, margin + grid_w, y, fill="#cccccc")

        # outer border, a bit heavier
        self.canvas.create_rectangle(margin, margin, margin + grid_w, margin + grid_h,
                                      outline="black", width=1.5)

        # fill matching cells
        half = window // 2
        pad = cell * 0.18
        for i in range(n):
            for j in range(m):
                matches = 0
                for k in range(-half, window - half):
                    a, b = i + k, j + k
                    if 0 <= a < n and 0 <= b < m and seq1[a] == seq2[b]:
                        matches += 1
                if matches >= stringency:
                    x0 = margin + i * cell + pad
                    y0 = margin + j * cell + pad
                    x1 = margin + (i + 1) * cell - pad
                    y1 = margin + (j + 1) * cell - pad
                    # highlight the main-diagonal-style exact matches (window=1)
                    # in a slightly darker fill so they pop against the grid
                    self.canvas.create_oval(x0, y0, x1, y1,
                                             fill="#1f6f1f", outline="")

    def find_segments(self, seq1, seq2, min_seg):
        """Scan every diagonal for runs of consecutive identical residues
        (these show up as unbroken diagonal lines on the dot plot)."""
        self.output_box.delete("1.0", "end")
        n, m = len(seq1), len(seq2)
        segments = []

        for d in range(-(n - 1), m):
            i = max(0, -d)
            j = i + d
            run_start_i = run_start_j = None
            run_len = 0
            while i < n and j < m:
                if seq1[i] == seq2[j]:
                    if run_len == 0:
                        run_start_i, run_start_j = i, j
                    run_len += 1
                else:
                    if run_len >= min_seg:
                        segments.append((run_start_i, run_start_j, run_len))
                    run_len = 0
                i += 1
                j += 1
            if run_len >= min_seg:
                segments.append((run_start_i, run_start_j, run_len))

        segments.sort(key=lambda s: -s[2])

        if not segments:
            self.output_box.insert("end", "No matching segments found at this minimum length.\n")
            return

        self.output_box.insert("end", f"Found {len(segments)} identical segment(s) "
                                       f"(length >= {min_seg}):\n\n")
        for si, sj, length in segments:
            frag = seq1[si:si + length]
            self.output_box.insert(
                "end",
                f"Length {length:3d} | Human pos {si+1:3d}-{si+length:3d} | "
                f"Chicken pos {sj+1:3d}-{sj+length:3d} | {frag}\n"
            )


if __name__ == "__main__":
    root = tk.Tk()
    app = DotPlotApp(root)
    root.mainloop()
