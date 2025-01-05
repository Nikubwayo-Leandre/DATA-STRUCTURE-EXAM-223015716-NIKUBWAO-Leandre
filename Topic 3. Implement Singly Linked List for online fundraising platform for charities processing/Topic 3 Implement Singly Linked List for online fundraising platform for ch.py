from tkinter import *
from tkinter import ttk


# Singly Linked List Node
class DonorNode:
    def __init__(self, donor_id, name, donation_amount):
        self.donor_id = donor_id
        self.name = name
        self.donation_amount = donation_amount
        self.next = None


# Singly Linked List for Donor Management
class DonorLinkedList:
    def __init__(self):
        self.head = None

    def add_donor(self, donor_id, name, donation_amount):
        new_node = DonorNode(donor_id, name, donation_amount)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def display_donors(self):
        donors = []
        current = self.head
        while current:
            donors.append((current.donor_id, current.name, current.donation_amount))
            current = current.next
        return donors

    def search_donor(self, donor_id):
        current = self.head
        while current:
            if current.donor_id == donor_id:
                return current
            current = current.next
        return None

    def delete_donor(self, donor_id):
        current = self.head
        prev = None
        while current:
            if current.donor_id == donor_id:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False


# Tkinter GUI
class FundraisingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ONLINE FUNDRAISING PLATFORM")
        self.root.geometry("800x600")

        self.donor_list = DonorLinkedList()
        self.setup_ui()

    def setup_ui(self):
        # Donor Section
        donor_frame = LabelFrame(self.root, text="Donor Management", bg=("yellow"), padx=10, pady=10)
        donor_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        Label(donor_frame, text="Donor ID").grid(row=0, column=0, padx=10, pady=5)
        self.donor_id_var = IntVar()
        Entry(donor_frame, textvariable=self.donor_id_var).grid(row=0, column=1, padx=10, pady=5)

        Label(donor_frame, text="Name").grid(row=1, column=0, padx=10, pady=5)
        self.donor_name_var = StringVar()
        Entry(donor_frame, textvariable=self.donor_name_var).grid(row=1, column=1, padx=10, pady=5)

        Label(donor_frame, text="Donation Amount").grid(row=2, column=0, padx=10, pady=5)
        self.donor_amount_var = DoubleVar()
        Entry(donor_frame, textvariable=self.donor_amount_var).grid(row=2, column=1, padx=10, pady=5)

        Button(donor_frame, text="Add Donor", bg=("red"), command=self.add_donor).grid(row=3, column=0, padx=10, pady=10)
        Button(donor_frame, text="Search Donor", bg=("red"), command=self.search_donor).grid(row=3, column=1, padx=10, pady=10)
        Button(donor_frame, text="Delete Donor", bg=("red"), command=self.delete_donor).grid(row=3, column=2, padx=10, pady=10)

        self.donor_tree = ttk.Treeview(donor_frame, columns=("ID", "Name", "Donation Amount"), show="headings", height=10)
        self.donor_tree.grid(row=4, column=0, columnspan=3, pady=10)
        self.donor_tree.heading("ID", text="Donor ID")
        self.donor_tree.heading("Name", text="Name")
        self.donor_tree.heading("Donation Amount", text="Donation Amount")

    def refresh_donor_table(self):
        # Clear table and refresh with current data
        for item in self.donor_tree.get_children():
            self.donor_tree.delete(item)
        for donor in self.donor_list.display_donors():
            self.donor_tree.insert("", "end", values=donor)

    def add_donor(self):
        donor_id = self.donor_id_var.get()
        name = self.donor_name_var.get()
        donation_amount = self.donor_amount_var.get()

        self.donor_list.add_donor(donor_id, name, donation_amount)
        self.refresh_donor_table()

        self.donor_id_var.set("")
        self.donor_name_var.set("")
        self.donor_amount_var.set("")

    def search_donor(self):
        donor_id = self.donor_id_var.get()
        donor = self.donor_list.search_donor(donor_id)

        if donor:
            self.show_popup("Donor Found", f"ID: {donor.donor_id}\nName: {donor.name}\nDonation Amount: ${donor.donation_amount}")
        else:
            self.show_popup("Error", "Donor not found.")

    def delete_donor(self):
        donor_id = self.donor_id_var.get()
        if self.donor_list.delete_donor(donor_id):
            self.refresh_donor_table()
            self.show_popup("Success", f"Donor ID {donor_id} deleted successfully.")
        else:
            self.show_popup("Error", "Donor not found.")

    def show_popup(self, title, message):
        popup = Toplevel(self.root)
        popup.title(title)
        Label(popup, text=message, font=("times new roman", 14)).pack(padx=20, pady=20)
        Button(popup, text="OK", command=popup.destroy).pack(pady=10)


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = FundraisingApp(root)
    root.mainloop()
