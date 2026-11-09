import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import os

def run_scan():
    scan_button.config(state=tk.DISABLED)
    mode = mode_var.get()
    scan_type = scan_type_var.get()
    start_port = start_port_entry.get()
    end_port = end_port_entry.get()
    target = target_entry.get()
    file_list = file_list_entry.get()
    threads = threads_entry.get() or "10"
    output_file = output_file_entry.get()

    if not mode or not scan_type:
        messagebox.showerror("Lỗi", "Vui lòng chọn chế độ và loại quét.")
        scan_button.config(state=tk.NORMAL)
        return

    command = ["python", "main.py", "-t", threads, mode]

    if mode == "Local":
        command += ["-l", scan_type]
        if scan_type == "PORT" or scan_type == "SERVICE":
            if not start_port or not end_port:
                messagebox.showerror("Thiếu thông tin", "Vui lòng nhập Start và End Port.")
                scan_button.config(state=tk.NORMAL)
                return
            command += ["-sP", start_port, "-eP", end_port]

    elif mode == "Web":
        command += ["-w", scan_type]
        if scan_type in ["SERVICE", "SUBDOMAIN", "PATH"]:
            if target:
                command += ["-u", target]
            elif file_list:
                command += ["-f", file_list]
            else:
                messagebox.showerror("Thiếu thông tin", "Vui lòng nhập URL hoặc File List.")
                scan_button.config(state=tk.NORMAL)
                return
        if scan_type == "SERVICE":
            if not start_port or not end_port:
                messagebox.showerror("Thiếu thông tin", "Vui lòng nhập Start và End Port.")
                scan_button.config(state=tk.NORMAL)
                return
            command += ["-sP", start_port, "-eP", end_port]

    elif mode == "Network":
        command += ["-n", scan_type]
        if target:
            command += ["-i", target]
        elif file_list:
            command += ["-f", file_list]
        else:
            messagebox.showerror("Thiếu thông tin", "Vui lòng nhập IP/Subnet hoặc File List.")
            scan_button.config(state=tk.NORMAL)
            return
        if scan_type == "SERVICE":
            if not start_port or not end_port:
                messagebox.showerror("Thiếu thông tin", "Vui lòng nhập Start và End Port.")
                scan_button.config(state=tk.NORMAL)
                return
            command += ["-sP", start_port, "-eP", end_port]

    if output_file:
        command += ["-o", output_file]

    print("Running command:", " ".join(command))

    try:
        # Gửi thêm biến môi trường PYTHONIOENCODING=utf-8 để fix lỗi Unicode
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            encoding="utf-8",
            errors="replace",
            env=env  # <<< ĐÂY LÀ DÒNG QUAN TRỌNG
        )
        output, _ = process.communicate()
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, output)
    except Exception as e:
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, f"Lỗi khi quét:\n{str(e)}")
    finally:
        scan_button.config(state=tk.NORMAL)


def update_scan_options(event=None):
    mode = mode_var.get()
    scan_type_box['values'] = []
    if mode == "Local":
        scan_type_box['values'] = ["PORT", "SERVICE"]
    elif mode == "Web":
        scan_type_box['values'] = ["SERVICE", "SUBDOMAIN", "PATH"]
    elif mode == "Network":
        scan_type_box['values'] = ["EXIST", "SERVICE"]
    scan_type_var.set("")

root = tk.Tk()
root.title("Scanner Toolkit GUI")
root.geometry("850x650")
root.configure(padx=20, pady=20)

style = ttk.Style()
style.theme_use('clam')
style.configure("TLabel", font=("Segoe UI", 10))
style.configure("TButton", font=("Segoe UI", 10, "bold"))
style.configure("TEntry", padding=5)
style.configure("TCombobox", padding=5)

# ==== Khung thông tin đầu vào ====
input_frame = ttk.LabelFrame(root, text="Thông tin quét", padding=15)
input_frame.grid(row=0, column=0, sticky="nsew")

# Chế độ
ttk.Label(input_frame, text="Chế độ:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
mode_var = tk.StringVar()
mode_box = ttk.Combobox(input_frame, textvariable=mode_var, values=["Local", "Web", "Network"], state="readonly")
mode_box.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
mode_box.bind("<<ComboboxSelected>>", update_scan_options)

# Loại quét
ttk.Label(input_frame, text="Loại quét:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
scan_type_var = tk.StringVar()
scan_type_box = ttk.Combobox(input_frame, textvariable=scan_type_var, state="readonly")
scan_type_box.grid(row=1, column=1, sticky='ew', padx=5, pady=5)

# Mục tiêu
ttk.Label(input_frame, text="Mục tiêu (IP/Domain):").grid(row=2, column=0, sticky='w', padx=5, pady=5)
target_entry = ttk.Entry(input_frame)
target_entry.grid(row=2, column=1, sticky='ew', padx=5, pady=5)

# File List
ttk.Label(input_frame, text="File List (nếu có):").grid(row=3, column=0, sticky='w', padx=5, pady=5)
file_list_entry = ttk.Entry(input_frame)
file_list_entry.grid(row=3, column=1, sticky='ew', padx=5, pady=5)

# Port
ttk.Label(input_frame, text="Start Port:").grid(row=4, column=0, sticky='w', padx=5, pady=5)
start_port_entry = ttk.Entry(input_frame, width=10)
start_port_entry.grid(row=4, column=1, sticky='w', padx=5, pady=5)

ttk.Label(input_frame, text="End Port:").grid(row=5, column=0, sticky='w', padx=5, pady=5)
end_port_entry = ttk.Entry(input_frame, width=10)
end_port_entry.grid(row=5, column=1, sticky='w', padx=5, pady=5)

# Threads
ttk.Label(input_frame, text="Threads:").grid(row=6, column=0, sticky='w', padx=5, pady=5)
threads_entry = ttk.Entry(input_frame, width=10)
threads_entry.grid(row=6, column=1, sticky='w', padx=5, pady=5)

# Output file
ttk.Label(input_frame, text="Output File (nếu có):").grid(row=7, column=0, sticky='w', padx=5, pady=5)
output_file_entry = ttk.Entry(input_frame)
output_file_entry.grid(row=7, column=1, sticky='ew', padx=5, pady=5)

# Nút chạy
scan_button = ttk.Button(input_frame, text="🔍 Quét ngay", command=run_scan)
scan_button.grid(row=8, column=0, columnspan=2, sticky='ew', padx=5, pady=10)

# ==== Khung kết quả ====
output_frame = ttk.LabelFrame(root, text="Kết quả", padding=15)
output_frame.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
output_text = tk.Text(output_frame, wrap="word", height=15, font=("Courier New", 10))
output_text.pack(expand=True, fill="both")

# Cấu hình co giãn
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)
input_frame.columnconfigure(1, weight=1)

root.mainloop()
