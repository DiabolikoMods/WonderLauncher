import tkinter as tk
from tkinter import ttk, messagebox, font
from PIL import Image, ImageTk
import shutil
import pyglet
import subprocess
import os
import time
import psutil

class WonderCleanerLauncher:
    def __init__(self):
        self.check_another_instance()
        self.root = tk.Tk()
        self.root.title("Wonder Launcher")
        self.root.geometry("280x280")
        self.root.resizable(width=False, height=False)
        self.root.configure(bg='#2C3E50')

        icon_path = os.path.join(os.path.dirname(__file__), "wonderlogo.ico")
        self.root.iconbitmap(default=icon_path)

        script_dir = os.path.dirname(os.path.realpath(__file__))
        font_path = os.path.join(script_dir, "Comfortaa.ttf")
        image_path = os.path.join(script_dir, "wonderlogo2.png")

        try:
            pyglet.font.add_file(font_path)
            self.custom_font = font.Font(family="Comfortaa", size=10)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il caricamento del font: {e}")
            return

        self.canvas = tk.Canvas(self.root, bg='#2C3E50', height=20, width=280)
        self.canvas.pack(side="top")

        self.scroll_text = "Developer: Diaboliko | Youtube: Diaboliko Mods | Telegram: @DiabolikoYT"
        self.text_object = self.canvas.create_text(300, 10, text=self.scroll_text, anchor=tk.E, fill='#ECF0F1', font=self.custom_font)
        self.scroll_speed = 1

        main_frame = tk.Frame(self.root, bg='#2C3E50')
        main_frame.pack(side="top", fill="both", expand=True, pady=10)

        image_frame = tk.Frame(main_frame, bg='#2C3E50')
        image_frame.pack()

        try:
            self.image = Image.open(image_path)
            self.background_image = ImageTk.PhotoImage(self.image)
            self.background_label = tk.Label(image_frame, image=self.background_image, bg='#2C3E50')
            self.background_label.pack(side="top", fill="both")
            self.background_label.pack_propagate(True)
        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il caricamento dell'immagine: {e}")

        text_frame = tk.Frame(main_frame, bg='#2C3E50')
        text_frame.pack(pady=0.1)

        try:
            self.label = ttk.Label(text_frame, text="Benvenuto nel launcher di Wonder!", foreground='#ECF0F1', background='#2C3E50', font=self.custom_font)
            self.label.pack(side="top")

            button_frame = tk.Frame(main_frame, bg='#2C3E50')
            button_frame.pack(side="top", pady=2)

            self.button_launcher = tk.Button(button_frame, text="Avvia Wonder RP", bg='#ff5c33', fg='black', padx=1, pady=1, command=self.run_wonder_rp, font=self.custom_font, width=13, height=1)
            self.button_launcher.pack(side="left", padx=2)

            self.button_cleaner = tk.Button(button_frame, text="Pulisci le Cache", bg='#ff5c33', fg='black', padx=1, pady=1, command=self.run_wonder_cleaner, font=self.custom_font, width=13, height=1)
            self.button_cleaner.pack(side="right", padx=2)

        except Exception as e:
            messagebox.showerror("Errore", f"Errore durante il caricamento dell'immagine: {e}")

    def check_another_instance(self):
        current_pid = os.getpid()
        for process in psutil.process_iter(['pid', 'name']):
            if process.info['name'] == "WonderLauncher.exe" and process.info['pid'] != current_pid:
                try:
                    os.kill(process.info['pid'], 9)
                except Exception as e:
                    messagebox.showerror("Errore", f"Errore durante la chiusura del processo {process.info['pid']}: {e}")

    def update_scroll_text(self):
        self.canvas.move(self.text_object, -self.scroll_speed, 0)

        x1, _, x2, _ = self.canvas.bbox(self.text_object)

        if x2 < 0:
            self.canvas.coords(self.text_object, 300, 10)

        self.root.after(30, self.update_scroll_text)

    def run_wonder_cleaner(self):
        base_path = self.find_base_path()

        if not base_path:
            messagebox.showerror("Errore", "Impossibile trovare le cache di FiveM.")
            return

        confirmation = messagebox.askyesno("Conferma", "Sei sicuro di voler cancellare le cache?")
        if not confirmation:
            messagebox.showinfo("Operazione annullata", "Operazione annullata.")
            return

        progress_window = tk.Toplevel(self.root)
        progress_window.title("Progresso")
        progress_window.geometry("200x50")
        progress_window.resizable(width=False, height=False)

        screen_width = progress_window.winfo_screenwidth()
        screen_height = progress_window.winfo_screenheight()
        x = (screen_width - 350) // 2
        y = (screen_height - 50) // 2
        progress_window.geometry(f"350x50+{x}+{y}")

        progressbar = ttk.Progressbar(progress_window, mode="indeterminate", length=300)
        progressbar.pack(pady=10)
        progressbar.start()

        try:
            self.delete_folders(base_path)
            messagebox.showinfo("Operazione completata", "Cache pulite con successo.")
        except Exception as e:
            messagebox.showerror("Errore", f"Errore generale: {e}")
        finally:
            progressbar.stop()
            progress_window.destroy()

    def delete_folders(self, base_path):
        folders_to_delete = ["cache", "server-cache", "nui-storage", "server-cache-priv"]

        confirmation = messagebox.askyesno("Conferma", f"Sei sicuro di voler eliminare le cache?")
        if not confirmation:
            messagebox.showinfo("Operazione annullata", "Operazione annullata.")
            return

        for folder in folders_to_delete:
            folder_path = os.path.join(base_path, folder)
            try:
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
            except FileNotFoundError:
                pass
            except PermissionError:
                messagebox.showerror("Errore di permessi", f"Non hai i permessi per eliminare '{folder}'.")
            except Exception as e:
                messagebox.showerror("Errore", f"Errore durante l'eliminazione di '{folder}': {e}")

    def find_base_path(self):
        possible_paths = [
            os.path.join(path, 'AppData', 'Local', 'FiveM', 'FiveM.app', 'data')
            for path in [os.path.expanduser('~')] + [os.environ.get('USERPROFILE', '')]
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def check_steam_running(self):
        for process in psutil.process_iter(['pid', 'name']):
            try:
                if 'steam.exe' in process.info['name']:
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def run_wonder_rp(self):
        if not self.check_steam_running():
            messagebox.showerror("Errore", "Steam non è aperto. Apri Steam e riprova.")
            return

        server_url = "roleplaywonder.it"
        
        time.sleep(3)

        start_command = 'start fivem://'
        try:
            subprocess.run(start_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante l'avvio di FiveM: {e}")
            return

        time.sleep(2)

        connect_command = f'start fivem://connect/{server_url}'
        try:
            subprocess.run(connect_command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Errore", f"Errore durante la connessione al server: {e}")
            return

        self.root.after(1000, self.root.destroy)

    def run(self):
        self.root.after(30, self.update_scroll_text)
        self.root.mainloop()

if __name__ == "__main__":
    launcher = WonderCleanerLauncher()
    launcher.run()
