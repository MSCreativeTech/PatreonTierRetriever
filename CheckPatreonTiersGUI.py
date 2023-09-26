import patreon
from tkinter import Tk, Label, Entry, Button, StringVar, Scrollbar, Frame, Canvas, messagebox, Menu
import webbrowser

def open_web_link(event):
    webbrowser.open("https://www.patreon.com/portal/registration/register-clients")

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def paste_from_clipboard():
    try:
        clipboard_content = root.clipboard_get()
        token_var.set(clipboard_content)
    except:
        messagebox.showwarning("Clipboard Empty", "There is nothing to paste from clipboard.")

def get_tiers():
    access_token = token_var.get().strip()
    if not access_token:
        messagebox.showwarning("Error", "Please enter an access token.")
        return

    try:
        api_client = patreon.API(access_token)
        response = api_client.fetch_user()
        response_data = getattr(response, 'json_data', None)

        if not response_data or 'included' not in response_data:
            messagebox.showerror("Error", "Error retrieving tiers")
            return

        for widget in tier_frame.winfo_children():
            widget.destroy()

        for resource in response_data['included']:
            if resource['type'] == 'reward':
                tier_id = resource['id']
                attributes = resource['attributes']
                tier_name = attributes.get('title')

                single_tier_frame = Frame(tier_frame, bg="#f5f5f5")
                single_tier_frame.pack(fill="x", padx=5, pady=5)

                tier_label_text = f"ID: {tier_id}"

                if tier_id == '0':
                    tier_label_text += ", *Non-Paying Users*"
                elif tier_id == '-1':
                    tier_label_text += ", *Special Case*"
                elif int(tier_id) > 0:
                    tier_label_text += f", Name: {tier_name if tier_name and not tier_name.isspace() else '*Unnamed*'}"

                tier_label = Label(single_tier_frame, text=tier_label_text, anchor="w", bg="#f5f5f5")
                tier_label.pack(side="left")

                button_frame = Frame(single_tier_frame, bg="#f5f5f5")
                button_frame.pack(side="right")

                copy_id_button = Button(button_frame, text="Copy Tier ID", command=lambda id=tier_id: copy_to_clipboard(id))
                copy_id_button.pack(side="left", padx=5)

                if int(tier_id) > 0:
                    copy_name_button = Button(button_frame, text="Copy Name", command=lambda name=tier_name: copy_to_clipboard(name))
                    copy_name_button.pack(side="right", padx=5)

    except AttributeError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_gui():
    global token_var, tier_frame, context_menu, root
    root = Tk()
    root.title("Patreon Tier Checker")

    Label(root, text="Get your Creator Access Token from:").pack(pady=2)
    link_label = Label(root, text="https://www.patreon.com/portal/registration/register-clients", fg="blue", cursor="hand2")
    link_label.pack(pady=2)
    link_label.bind("<Button-1>", open_web_link)

    Label(root, text="Please enter your Creator Access Token:").pack(pady=10)
    token_var = StringVar()
    entry = Entry(root, textvariable=token_var, width=50)
    entry.pack(pady=5)
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Copy", command=lambda: root.clipboard_append(entry.selection_get()))
    context_menu.add_command(label="Paste", command=lambda: token_var.set(root.clipboard_get()))
    entry.bind("<Button-3>", show_context_menu)

    button_frame = Frame(root)
    button_frame.pack(pady=10)

    retrieve_button = Button(button_frame, text="Retrieve Tiers", command=get_tiers)
    retrieve_button.pack(side="left", padx=(0, 5))

    paste_button = Button(button_frame, text="Paste Clipboard", command=paste_from_clipboard)
    paste_button.pack(side="right", padx=(5, 0))

    scroll = Scrollbar(root)
    scroll.pack(side="right", fill="y")

    canvas = Canvas(root, bg="#f5f5f5")
    canvas.pack(side="left", fill="both", expand=True)

    tier_frame = Frame(canvas, bg="#f5f5f5")
    canvas.create_window((0, 0), window=tier_frame, anchor="nw")

    tier_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    scroll.config(command=canvas.yview)
    canvas.config(yscrollcommand=scroll.set)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
