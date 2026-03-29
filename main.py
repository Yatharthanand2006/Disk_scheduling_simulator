# Final version ready for submission
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# importing scheduling algorithms
from algorithms import fcfs, sstf, scan, cscan


# ---------------- INPUT HELPER (Placeholder Text) ----------------
def set_placeholder(entry_box, placeholder_text):
    entry_box.insert(0, placeholder_text)
    entry_box.config(fg="gray")

    # when user clicks → remove placeholder
    def on_click(event):
        if entry_box.get() == placeholder_text:
            entry_box.delete(0, tk.END)
            entry_box.config(fg="white")

    # when user leaves → restore if empty
    def on_leave(event):
        if entry_box.get() == "":
            entry_box.insert(0, placeholder_text)
            entry_box.config(fg="gray")

    entry_box.bind("<FocusIn>", on_click)
    entry_box.bind("<FocusOut>", on_leave)


# ---------------- MAIN FUNCTION ----------------
def run_simulation():
    try:
        # take inputs from user
        req_input = entry_requests.get()
        head_input = entry_head.get()
        disk_input = entry_disk.get()

        # check if user has not entered real values
        if "e.g." in req_input or "e.g." in head_input or "e.g." in disk_input:
            output_box.insert(tk.END, "⚠ Please enter proper values\n")
            return

        # convert input into numbers
        requests = list(map(int, req_input.split(',')))
        head = int(head_input)
        disk_size = int(disk_input)

        # apply all algorithms
        results = {
            "FCFS": fcfs(requests, head),
            "SSTF": sstf(requests, head),
            "SCAN": scan(requests, head, disk_size),
            "C-SCAN": cscan(requests, head, disk_size)
        }

        # find best algorithm (minimum seek time)
        best_algo = min(results, key=lambda x: results[x][1])

        # update dashboard cards
        card_fcfs.config(text=f"FCFS\n{results['FCFS'][1]}")
        card_sstf.config(text=f"SSTF\n{results['SSTF'][1]}")
        card_scan.config(text=f"SCAN\n{results['SCAN'][1]}")
        card_cscan.config(text=f"C-SCAN\n{results['C-SCAN'][1]}")
        best_label.config(text=f"🏆 BEST: {best_algo}")

        # clear old output
        output_box.delete(1.0, tk.END)

        # print results
        for name, (sequence, seek) in results.items():
            avg = seek / len(sequence)

            output_box.insert(tk.END,
                f"\n-----------------------------\n"
                f"{name}\n"
                f"Path: {' → '.join(map(str, sequence))}\n"
                f"Total Seek Time: {seek}\n"
                f"Average Seek Time: {avg:.2f}\n"
            )

        output_box.insert(tk.END, f"\n🏆 BEST ALGORITHM: {best_algo}\n")
        output_box.see(tk.END)

        # show graph
        draw_graph(results)

    except Exception as err:
        output_box.insert(tk.END, f"Error: {err}\n")


# ---------------- GRAPH FUNCTION ----------------
def draw_graph(results):
    # clear old graph
    for widget in graph_area.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots()

    fig.patch.set_facecolor('#0f172a')
    ax.set_facecolor('#020617')

    # colors for each algorithm
    colors = {
        "FCFS": "#38bdf8",
        "SSTF": "#facc15",
        "SCAN": "#4ade80",
        "C-SCAN": "#f87171"
    }

    lines = {}
    dots = {}

    # create empty lines first
    for name in results:
        line, = ax.plot([], [], marker='o',
                        color=colors[name],
                        linewidth=2,
                        label=name)

        dot = ax.scatter([], [], s=100,
                         color=colors[name],
                         edgecolors='white')

        lines[name] = line
        dots[name] = dot

    ax.set_title("Disk Head Movement", color="white")
    ax.set_xlabel("Steps", color="white")
    ax.set_ylabel("Disk Position", color="white")
    ax.tick_params(colors='white')
    ax.legend()

    canvas = FigureCanvasTkAgg(fig, master=graph_area)
    canvas.get_tk_widget().pack(fill="both", expand=True)

    # animate movement step-by-step
    max_steps = max(len(seq) for seq, _ in results.values())

    for i in range(max_steps):
        for name, (seq, _) in results.items():
            if i < len(seq):
                x_vals = list(range(i + 1))
                y_vals = seq[:i + 1]

                lines[name].set_data(x_vals, y_vals)
                dots[name].set_offsets([[x_vals[-1], y_vals[-1]]])

        ax.relim()
        ax.autoscale_view()

        canvas.draw()
        root.update()
        root.after(200)


# ---------------- UI SETUP ----------------
root = tk.Tk()
root.title("Disk Scheduling Simulator Pro")
root.geometry("1300x850")
root.configure(bg="#0f172a")


# ---------------- LEFT PANEL ----------------
left_panel = tk.Frame(root, bg="#1e293b", width=260)
left_panel.pack(side="left", fill="y")

tk.Label(left_panel, text="OS Project", fg="cyan", bg="#1e293b").pack()

tk.Label(left_panel, text="CONTROL PANEL",
         bg="#1e293b", fg="#38bdf8",
         font=("Segoe UI", 14, "bold")).pack(pady=15)


def create_input(label, placeholder):
    tk.Label(left_panel, text=label,
             bg="#1e293b", fg="white").pack(anchor="w", padx=15)

    entry = tk.Entry(left_panel, bg="#020617",
                     fg="white", relief="flat")
    entry.pack(pady=5, padx=15, fill="x", ipady=5)

    set_placeholder(entry, placeholder)
    return entry


entry_requests = create_input("Requests", "e.g. 98,183,37")
entry_head = create_input("Head Position", "e.g. 53")
entry_disk = create_input("Disk Size", "e.g. 200")

tk.Button(left_panel, text="Run",
          bg="#38bdf8",
          command=run_simulation).pack(pady=20)

best_label = tk.Label(left_panel, text="BEST: -",
                      bg="#1e293b", fg="lime")
best_label.pack()


# ---------------- TOP CARDS ----------------
top_frame = tk.Frame(root, bg="#0f172a")
top_frame.pack(fill="x")


def make_card(parent):
    return tk.Label(parent, text="-",
                    bg="#020617", fg="white",
                    width=15, height=3)


card_fcfs = make_card(top_frame)
card_sstf = make_card(top_frame)
card_scan = make_card(top_frame)
card_cscan = make_card(top_frame)

card_fcfs.pack(side="left", padx=10, pady=10)
card_sstf.pack(side="left", padx=10)
card_scan.pack(side="left", padx=10)
card_cscan.pack(side="left", padx=10)


# ---------------- GRAPH AREA ----------------
graph_area = tk.Frame(root, bg="#020617", height=400)
graph_area.pack(fill="x", padx=10, pady=5)
graph_area.pack_propagate(False)


# ---------------- OUTPUT AREA ----------------
output_frame = tk.Frame(root, bg="#020617")
output_frame.pack(fill="both", expand=True)

output_box = tk.Text(output_frame,
                     bg="#020617",
                     fg="white")
output_box.pack(fill="both", expand=True)


root.mainloop()