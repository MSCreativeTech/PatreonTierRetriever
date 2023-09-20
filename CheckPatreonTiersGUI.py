import patreon
from tkinter import Tk, Label, Entry, Button, StringVar, Text, Scrollbar, messagebox, Menu
import webbrowser

def open_web_link(event):
    webbrowser.open("https://www.patreon.com/portal/registration/register-clients")

def show_context_menu(event):
    context_menu.post(event.x_root, event.y_root)
    
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

        tier_text.delete(1.0, "end")
        for resource in response_data['included']:
            if resource['type'] == 'reward':
                tier_id = resource['id']
                attributes = resource['attributes']
                tier_name = attributes.get('title')
                
                if tier_id == '-1':
                    tier_name = "Special Case -1 (Unknown)"
                elif tier_id == '0':
                    tier_name = "Non-Paying Users"
                elif not tier_name or tier_name.isspace():
                    tier_name = "*Unnamed*"
                
                tier_text.insert("end", f"ID: {tier_id}, Name: {tier_name}\n")
    except AttributeError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_gui():
    global token_var, tier_text, context_menu
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

    Button(root, text="Retrieve Tiers", command=get_tiers).pack(pady=10)

    scroll = Scrollbar(root)
    scroll.pack(side="right", fill="y")

    tier_text = Text(root, wrap="none", yscrollcommand=scroll.set, width=60, height=10)
    tier_text.pack(pady=5)
    scroll.config(command=tier_text.yview)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
