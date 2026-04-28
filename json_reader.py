import json
import textwrap
import tkinter as tk
from tkinter import ttk
import translators as ts

LANGUAGES = {
    "No translation": None,
    "English":        "en",
    "Chinese (Simplified)": "zh",
    "Spanish":        "es",
    "French":         "fr",
    "German":         "de",
    "Japanese":       "ja",
    "Korean":         "ko",
    "Arabic":         "ar",
    "Portuguese":     "pt",
    "Russian":        "ru",
    "Thai":           "th",
    "Vietnamese":     "vi",
    "Tagalog":        "tl",
}


def translate_text(text, target_lang):
    if not target_lang or not text.strip():
        return text
    return ts.translate_text(text, translator="google", to_language=target_lang)


def format_value(value, indent=0, wrap_width=80, target_lang=None):
    pad = "  " * indent
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(format_value(v, indent + 1, wrap_width, target_lang))
            else:
                lines.append(f"{pad}{k}: {format_value(v, indent, wrap_width, target_lang)}")
        return "\n".join(lines)
    elif isinstance(value, list):
        lines = []
        for item in value:
            if isinstance(item, (dict, list)):
                lines.append(format_value(item, indent, wrap_width, target_lang))
                lines.append("")
            else:
                lines.append(f"{pad}- {format_value(item, indent, wrap_width, target_lang)}")
        return "\n".join(lines).rstrip()
    elif isinstance(value, str):
        text = value.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "")
        text = translate_text(text, target_lang)
        if wrap_width > 0:
            wrapped_lines = []
            for line in text.splitlines():
                wrapped_lines.extend(
                    textwrap.wrap(line, width=wrap_width, subsequent_indent=pad + "  ") or [""]
                )
            return "\n".join(wrapped_lines)
        return text
    else:
        return str(value)


def on_read():
    raw = input_text.get("1.0", tk.END).strip()
    if not raw:
        set_output("Please paste a JSON string or plain text first.")
        return

    target_lang = LANGUAGES[lang_var.get()]
    wrap_width = wrap_var.get()

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = raw  # treat as plain string

    try:
        formatted = format_value(data, wrap_width=wrap_width, target_lang=target_lang)
        sep_start = "=" * 40 + " START " + "=" * 40
        sep_end   = "=" * 41 + " END "   + "=" * 41
        set_output(f"{sep_start}\n{formatted}\n{sep_end}")
    except Exception as e:
        set_output(f"Error: {e}")


def set_output(text):
    output_text.config(state=tk.NORMAL)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, text)
    output_text.config(state=tk.DISABLED)


# --- Main window ---
root = tk.Tk()
root.title("JSON Reader")
root.geometry("900x700")
root.resizable(True, True)

pad = {"padx": 8, "pady": 4}

# Input
tk.Label(root, text="Input (JSON or plain text):", anchor="w").pack(fill=tk.X, **pad)
input_text = tk.Text(root, height=10, wrap=tk.WORD, font=("Courier", 11))
input_text.pack(fill=tk.X, **pad)

# Controls row
ctrl_frame = tk.Frame(root)
ctrl_frame.pack(fill=tk.X, **pad)

tk.Label(ctrl_frame, text="Wrap width:").pack(side=tk.LEFT)
wrap_var = tk.IntVar(value=80)
wrap_scale = tk.Scale(ctrl_frame, from_=20, to=200, resolution=10,
                      orient=tk.HORIZONTAL, variable=wrap_var, length=200)
wrap_scale.pack(side=tk.LEFT, padx=(4, 20))

tk.Label(ctrl_frame, text="Translate to:").pack(side=tk.LEFT)
lang_var = tk.StringVar(value="No translation")
lang_menu = ttk.Combobox(ctrl_frame, textvariable=lang_var,
                         values=list(LANGUAGES.keys()), state="readonly", width=20)
lang_menu.pack(side=tk.LEFT, padx=4)

tk.Button(ctrl_frame, text="Read JSON", command=on_read,
          bg="#0078d4", fg="white", padx=12).pack(side=tk.LEFT, padx=20)

tk.Label(ctrl_frame, text="Font size:").pack(side=tk.LEFT, padx=(20, 0))
font_var = tk.IntVar(value=11)

def on_font_change(val):
    size = int(float(val))
    input_text.config(font=("Courier", size))
    output_text.config(font=("Courier", size))

font_scale = tk.Scale(ctrl_frame, from_=8, to=32, resolution=1,
                      orient=tk.HORIZONTAL, variable=font_var,
                      command=on_font_change, length=150)
font_scale.pack(side=tk.LEFT, padx=4)

# Output
tk.Label(root, text="Output:", anchor="w").pack(fill=tk.X, **pad)
output_text = tk.Text(root, wrap=tk.WORD, font=("Courier", 11), state=tk.DISABLED, bg="#f5f5f5")
output_text.pack(fill=tk.BOTH, expand=True, **pad)

root.mainloop()
