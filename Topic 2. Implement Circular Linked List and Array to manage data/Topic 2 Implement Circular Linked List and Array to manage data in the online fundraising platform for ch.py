from tkinter import *
from tkinter import ttk


# Circular Linked List for Donors
class DonorNode:
    def __init__(self, donor_id, name, donation_amount):
        self.donor_id = donor_id
        self.name = name
        self.donation_amount = donation_amount
        self.next = None


class CircularDonorList:
    def __init__(self):
        self.head = None

    def add_donor(self, donor_id, name, donation_amount):
        new_node = DonorNode(donor_id, name, donation_amount)
        if not self.head:
            self.head = new_node
            new_node.next = self.head  # Circular link
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head  # Maintain circular link

    def display_donors(self):
        if not self.head:
            return []
        donors = []
        current = self.head
        while True:
            donors.append((current.donor_id, current.name, current.donation_amount))
            current = current.next
            if current == self.head:
                break
        return donors

    def search_donor(self, donor_id):
        if not self.head:
            return None
        current = self.head
        while True:
            if current.donor_id == donor_id:
                return current
            current = current.next
            if current == self.head:
                break
        return None


# Fundraising Campaigns Array
class FundraisingCampaigns:
    def __init__(self):
        self.campaigns = []

    def add_campaign(self, campaign_name, goal_amount):
        self.campaigns.append({"name": campaign_name, "goal": goal_amount, "raised": 0})

    def update_raised_amount(self, campaign_index, amount):
        if 0 <= campaign_index < len(self.campaigns):
            self.campaigns[campaign_index]["raised"] += amount

    def display_campaigns(self):
        return self.campaigns


# Tkinter GUI
class FundraisingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fundraising Platform")
        self.root.geometry("800x600")

        self.donor_list = CircularDonorList()
        self.campaigns = FundraisingCampaigns()

        self.setup_ui()

    def setup_ui(self):
        # Donor Section
        donor_frame = LabelFrame(self.root, text="Donor Management", padx=10, pady=10)
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

        Button(donor_frame, text="Add Donor", command=self.add_donor).grid(row=3, column=0, padx=10, pady=10)
        Button(donor_frame, text="View All Donors", command=self.display_donors).grid(row=3, column=1, padx=10, pady=10)

        self.donor_tree = ttk.Treeview(donor_frame, columns=("ID", "Name", "Amount"), show="headings", height=5)
        self.donor_tree.grid(row=4, column=0, columnspan=2, pady=10)
        self.donor_tree.heading("ID", text="ID")
        self.donor_tree.heading("Name", text="Name")
        self.donor_tree.heading("Amount", text="Donation Amount")

        # Campaign Section
        campaign_frame = LabelFrame(self.root, text="Campaign Management", padx=10, pady=10)
        campaign_frame.pack(fill="both", expand="yes", padx=10, pady=10)

        Label(campaign_frame, text="Campaign Name").grid(row=0, column=0, padx=10, pady=5)
        self.campaign_name_var = StringVar()
        Entry(campaign_frame, textvariable=self.campaign_name_var).grid(row=0, column=1, padx=10, pady=5)

        Label(campaign_frame, text="Goal Amount").grid(row=1, column=0, padx=10, pady=5)
        self.campaign_goal_var = DoubleVar()
        Entry(campaign_frame, textvariable=self.campaign_goal_var).grid(row=1, column=1, padx=10, pady=5)

        Button(campaign_frame, text="Add Campaign", command=self.add_campaign).grid(row=2, column=0, padx=10, pady=10)
        Button(campaign_frame, text="View Campaigns", command=self.display_campaigns).grid(row=2, column=1, padx=10, pady=10)

        self.campaign_tree = ttk.Treeview(campaign_frame, columns=("Name", "Goal", "Raised"), show="headings", height=5)
        self.campaign_tree.grid(row=3, column=0, columnspan=2, pady=10)
        self.campaign_tree.heading("Name", text="Name")
        self.campaign_tree.heading("Goal", text="Goal Amount")
        self.campaign_tree.heading("Raised", text="Raised Amount")

    def add_donor(self):
        donor_id = self.donor_id_var.get()
        name = self.donor_name_var.get()
        amount = self.donor_amount_var.get()
        self.donor_list.add_donor(donor_id, name, amount)
        self.donor_id_var.set("")
        self.donor_name_var.set("")
        self.donor_amount_var.set("")

    def display_donors(self):
        for item in self.donor_tree.get_children():
            self.donor_tree.delete(item)
        donors = self.donor_list.display_donors()
        for donor in donors:
            self.donor_tree.insert("", "end", values=donor)

    def add_campaign(self):
        name = self.campaign_name_var.get()
        goal = self.campaign_goal_var.get()
        self.campaigns.add_campaign(name, goal)
        self.campaign_name_var.set("")
        self.campaign_goal_var.set("")

    def display_campaigns(self):
        for item in self.campaign_tree.get_children():
            self.campaign_tree.delete(item)
        campaigns = self.campaigns.display_campaigns()
        for campaign in campaigns:
            self.campaign_tree.insert("", "end", values=(campaign["name"], campaign["goal"], campaign["raised"]))


# Run the application
if __name__ == "__main__":
    root = Tk()
    app = FundraisingApp(root)
    root.mainloop()