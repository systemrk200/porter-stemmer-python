              стрimport tkinter as tk
from tkinter import ttk

from stemmer import stem

BG = "#f7f5f2"
ACCENT = "#7c5cbf"
TEXT = "#2b2b2b"
PUNCTUATION = ".,!?;:\"'()«»—-"


class StemmerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Алгоритм Портера — выделение основы слова")
        self.geometry("720x680")
        self.configure(bg=BG)

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 11), padding=8)
        style.configure("TLabel", background=BG, foreground=TEXT, font=("Segoe UI", 11))
        style.configure("Header.TLabel", font=("Segoe UI", 13, "bold"), foreground=ACCENT)

        self._build_ui()

    def _build_ui(self):
        frame = tk.Frame(self, bg=BG, padx=20, pady=16)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Одно слово", style="Header.TLabel").pack(anchor="w")

        row = tk.Frame(frame, bg=BG)
        row.pack(fill="x", pady=(8, 0))
        self.word_var = tk.StringVar()
        entry = ttk.Entry(row, textvariable=self.word_var, font=("Segoe UI", 13))
        entry.pack(side="left", fill="x", expand=True)
        entry.bind("<Return>", lambda _: self.stem_word())
        ttk.Button(row, text="Выделить основу", command=self.stem_word).pack(side="left", padx=(10, 0))

        self.result_var = tk.StringVar(value="Результат появится здесь")
        result = ttk.Label(frame, textvariable=self.result_var, font=("Segoe UI", 16, "bold"))
        result.pack(anchor="w", pady=(16, 4))

        ttk.Label(frame, text="Ход алгоритма:", style="Header.TLabel").pack(anchor="w", pady=(10, 4))
        self.trace_box = tk.Text(
            frame, height=12, font=("Consolas", 10), bg="white", fg=TEXT,
            relief="solid", bd=1, highlightthickness=0, state="disabled", wrap="word",
        )
        self.trace_box.pack(fill="both", expand=True)

        ttk.Label(frame, text="Текст целиком", style="Header.TLabel").pack(anchor="w", pady=(14, 4))

        batch_row = tk.Frame(frame, bg=BG)
        batch_row.pack(fill="both", expand=True)
        self.batch_input = tk.Text(
            batch_row, height=5, font=("Segoe UI", 11), bg="white", fg=TEXT,
            relief="solid", bd=1, highlightthickness=0, wrap="word",
        )
        self.batch_input.pack(side="left", fill="both", expand=True)
        self.batch_input.insert("1.0", "мама мыла раму, а кошка сидела на окошке")
        ttk.Button(batch_row, text="Обработать текст", command=self.stem_text).pack(side="left", padx=(10, 0), anchor="n")

        self.batch_output = tk.Text(
            frame, height=5, font=("Consolas", 10), bg="white", fg=TEXT,
            relief="solid", bd=1, highlightthickness=0, state="disabled", wrap="word",
        )
        self.batch_output.pack(fill="both", expand=True, pady=(8, 0))

    def stem_word(self):
        word = self.word_var.get().strip()
        if not word:
            return
        trace = []
        result = stem(word, trace)
        self.result_var.set(f"{word.lower()}  →  {result}")
        self._set_text(self.trace_box, "\n".join(trace))

    def stem_text(self):
        text = self.batch_input.get("1.0", "end").strip()
        if not text:
            return
        tokens = [token.strip(PUNCTUATION) for token in text.split()]
        tokens = [token for token in tokens if token]
        stems = [stem(token) for token in tokens]
        width = max(len(token) for token in tokens)
        lines = [f"{token:<{width}} → {s}" for token, s in zip(tokens, stems)]
        self._set_text(self.batch_output, "\n".join(lines))

    @staticmethod
    def _set_text(widget, content):
        widget.configure(state="normal")
        widget.delete("1.0", "end")
        widget.insert("1.0", content)
        widget.configure(state="disabled")


if __name__ == "__main__":
    StemmerApp().mainloop()
