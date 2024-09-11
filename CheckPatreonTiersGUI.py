import patreon
from tkinter import Tk, Label, Entry, Button, StringVar, Scrollbar, Frame, Canvas, messagebox, Menu, ttk  # Import ttk for themed widgets
import webbrowser

def open_web_link(event):
    """Opens the Patreon client registration link in a web browser."""
    webbrowser.open("https://www.patreon.com/portal/registration/register-clients")

def show_context_menu(event):
    """Displays the context menu for the entry field."""
    context_menu.post(event.x_root, event.y_root)

def copy_to_clipboard(text):
    """Copies the given text to the clipboard."""
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()

def paste_from_clipboard():
    """Pastes text from the clipboard into the entry field."""
    try:
        clipboard_content = root.clipboard_get()
        token_var.set(clipboard_content)
    except:
        messagebox.showwarning("Clipboard Empty", "There is nothing to paste from clipboard.")

def get_tiers():
    """Retrieves tier information from Patreon using the access token and displays it."""
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

        # Get member ID
        member_id = response_data['data']['id']
        member_id_label.config(text=f"Current Member ID: {member_id}")

        # Clear existing tier information
        for widget in tier_frame.winfo_children():
            widget.destroy()

        # Display tier information
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

                copy_id_button = ttk.Button(button_frame, text="Copy Tier ID", command=lambda id=tier_id: copy_to_clipboard(id))  # Use ttk.Button
                copy_id_button.pack(side="left", padx=5)

                if int(tier_id) > 0:
                    copy_name_button = ttk.Button(button_frame, text="Copy Name", command=lambda name=tier_name: copy_to_clipboard(name))  # Use ttk.Button
                    copy_name_button.pack(side="right", padx=5)

    except AttributeError as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def create_gui():
    """Creates the main GUI window and its components."""
    global token_var, tier_frame, context_menu, root, member_id_label
    root = Tk()
    root.title("Patreon Tier Checker")

    # Set a theme for a more modern look
    style = ttk.Style()
    style.theme_use("clam")  # You can try other themes like "alt", "default", "classic"

    # Configure label and entry styles
    style.configure("TLabel", padding=(5, 5), font=("Segoe UI", 10))
    style.configure("TEntry", padding=(5, 5), font=("Segoe UI", 10))

    # Label for instructions
    Label(root, text="Get your Creator Access Token from:").pack(pady=5)

    # Link label with hyperlink
    link_label = Label(root, text="https://www.patreon.com/portal/registration/register-clients", fg="blue", cursor="hand2")
    link_label.pack(pady=5)
    link_label.bind("<Button-1>", open_web_link)

    # Label for access token input
    Label(root, text="Please enter your Creator Access Token:").pack(pady=5)

    # Entry field for access token (using ttk.Entry for themed look)
    token_var = StringVar()
    entry = ttk.Entry(root, textvariable=token_var, width=50)
    entry.pack(pady=5)

    # Context menu for entry field
    context_menu = Menu(root, tearoff=0)
    context_menu.add_command(label="Copy", command=lambda: root.clipboard_append(entry.selection_get()))
    context_menu.add_command(label="Paste", command=lambda: token_var.set(root.clipboard_get()))
    entry.bind("<Button-3>", show_context_menu)

    # Frame for buttons
    button_frame = Frame(root)
    button_frame.pack(pady=10)

    # Buttons with ttk.Button for themed look
    retrieve_button = ttk.Button(button_frame, text="Retrieve Tiers", command=get_tiers)
    retrieve_button.pack(side="left", padx=(0, 5))

    paste_button = ttk.Button(button_frame, text="Paste Clipboard", command=paste_from_clipboard)
    paste_button.pack(side="right", padx=(5, 0))

    # Frame for member ID label and copy button
    member_id_frame = Frame(root)
    member_id_frame.pack(pady=5)

    # Label to display member ID
    member_id_label = Label(member_id_frame, text="Current Member ID: ")
    member_id_label.pack(side="left")

    # Button to copy member ID (using ttk.Button)
    copy_member_id_button = ttk.Button(member_id_frame, text="Copy", command=lambda: copy_to_clipboard(member_id_label.cget("text").split(": ")[1]))
    copy_member_id_button.pack(side="left", padx=5)

    # Scrollbar for tier information
    scroll = Scrollbar(root)
    scroll.pack(side="right", fill="y")

    # Canvas for tier information
    canvas = Canvas(root, bg="#f5f5f5")
    canvas.pack(side="left", fill="both", expand=True)

    # Frame to hold tier information within canvas
    tier_frame = Frame(canvas, bg="#f0f0f0")  # Light gray background
    canvas.create_window((0, 0), window=tier_frame, anchor="nw")

    # Configure scrolling for tier information
    tier_frame.bind("<Configure>", lambda event: canvas.configure(scrollregion=canvas.bbox("all")))
    scroll.config(command=canvas.yview)
    canvas.config(yscrollcommand=scroll.set)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
