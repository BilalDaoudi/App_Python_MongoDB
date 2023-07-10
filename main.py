import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from pymongo import MongoClient

class Groupe(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gestion des stagiaires DEVOWFS202")
        self.geometry("500x500")

        # Connexion à la base de données MongoDB
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['stagiaires']
        self.collection = self.db['groupe']

        # Création des widgets
        self.label_id = tk.Label(self, text="ID:")
        self.label_nom = tk.Label(self, text="Nom:")
        self.label_sexe = tk.Label(self, text="Sexe:")
        self.label_nationalite = tk.Label(self, text="Nationalité:")
        self.label_loisirs = tk.Label(self, text="Loisirs:")

        self.entry_id = tk.Entry(self)
        self.entry_nom = tk.Entry(self)

        self.radio_sexe = tk.StringVar()
        self.radio_sexe.set("Homme")
        self.radio_homme = tk.Radiobutton(self, text="Homme", variable=self.radio_sexe, value="Homme")
        self.radio_femme = tk.Radiobutton(self, text="Femme", variable=self.radio_sexe, value="Femme")

        self.combo_nationalite = ttk.Combobox(self, values=["Maroc", "France", "Italy"])

        self.check_lecture = tk.BooleanVar()
        self.checkbutton_lecture = tk.Checkbutton(self, text="Lecture", variable=self.check_lecture)

        self.check_programmation = tk.BooleanVar()
        self.checkbutton_programmation = tk.Checkbutton(self, text="Programmation", variable=self.check_programmation)

        self.check_sport = tk.BooleanVar()
        self.checkbutton_sport = tk.Checkbutton(self, text="Sport", variable=self.check_sport)

        self.button_ajouter = tk.Button(self, text="Ajouter", command=self.ajouter_stagiaire,width=10)
        self.button_supprimer = tk.Button(self, text="Supprimer", command=self.supprimer_stagiaire,width=10)
        self.button_modifier = tk.Button(self, text="Modifier", command=self.modifier_stagiaire,width=10)
        self.button_rechercher = tk.Button(self, text="Rechercher", command=self.rechercher_stagiaire,width=10)
        self.button_vider = tk.Button(self, text="Vider", command=self.vider_champs,width=10)

        # Création du tableau pour afficher les stagiaires
        self.tableau_stagiaires = ttk.Treeview(self, columns=("ID", "Nom", "Sexe", "Nationalité", "Loisirs"))
        self.tableau_stagiaires.heading("ID", text="ID")
        self.tableau_stagiaires.heading("Nom", text="Nom")
        self.tableau_stagiaires.heading("Sexe", text="Sexe")
        self.tableau_stagiaires.heading("Nationalité", text="Nationalité")
        self.tableau_stagiaires.heading("Loisirs", text="Loisirs")
        self.tableau_stagiaires.column("#0", width=0, stretch=tk.NO)  # Colonne invisible pour l'index
        self.tableau_stagiaires.column("ID", width=50, anchor=tk.CENTER)
        self.tableau_stagiaires.column("Nom", width=100, anchor=tk.W)
        self.tableau_stagiaires.column("Sexe", width=70, anchor=tk.CENTER)
        self.tableau_stagiaires.column("Nationalité", width=100, anchor=tk.CENTER)
        self.tableau_stagiaires.column("Loisirs", width=150, anchor=tk.W)
        self.tableau_stagiaires.bind("<ButtonRelease-1>", self.selectionner_stagiaire)
        self.tableau_stagiaires.place(x=10, y=180)

        # Récupération des stagiaires existants dans la base de données
        self.maj_tableau_stagiaires()

        # Placement des widgets dans la fenêtre
        self.label_id.place(x=10, y=10)
        self.label_nom.place(x=10, y=40)
        self.label_sexe.place(x=10, y=70)
        self.label_nationalite.place(x=10, y=100)
        self.label_loisirs.place(x=10, y=130)

        self.entry_id.place(x=120, y=10)
        self.entry_nom.place(x=120, y=40)
        self.radio_homme.place(x=120, y=70)
        self.radio_femme.place(x=200, y=70)
        self.combo_nationalite.place(x=120, y=100)
        self.checkbutton_lecture.place(x=120, y=130)
        self.checkbutton_programmation.place(x=185, y=130)
        self.checkbutton_sport.place(x=300, y=130)

        self.button_ajouter.place(x=400, y=10)
        self.button_supprimer.place(x=400, y=40)
        self.button_modifier.place(x=400, y=70)
        self.button_rechercher.place(x=400, y=100)
        self.button_vider.place(x=400, y=130)

    def maj_tableau_stagiaires(self):
        # Effacer les anciennes données du tableau
        self.tableau_stagiaires.delete(*self.tableau_stagiaires.get_children())

        # Récupérer tous les stagiaires depuis la base de données
        stagiaires = self.collection.find()

        # Ajouter chaque stagiaire dans le tableau
        for stagiaire in stagiaires:
            id_stagiaire = stagiaire.get("id", "")
            nom_stagiaire = stagiaire.get("nom", "")
            sexe_stagiaire = stagiaire.get("sexe", "")
            nationalite_stagiaire = stagiaire.get("nationalite", "")
            loisirs_stagiaire = ", ".join(stagiaire.get("loisirs", []))

            self.tableau_stagiaires.insert("", tk.END, text="", values=(id_stagiaire, nom_stagiaire, sexe_stagiaire,nationalite_stagiaire, loisirs_stagiaire))

    def ajouter_stagiaire(self):
        id_stagiaire = self.entry_id.get()
        nom_stagiaire = self.entry_nom.get()
        sexe_stagiaire = self.radio_sexe.get()
        nationalite_stagiaire = self.combo_nationalite.get()
        loisirs_stagiaire = []

        if self.check_lecture.get():
            loisirs_stagiaire.append("Lecture")
        if self.check_programmation.get():
            loisirs_stagiaire.append("Programmation")
        if self.check_sport.get():
            loisirs_stagiaire.append("Sport")

        stagiaire = {
            "id": id_stagiaire,
            "nom": nom_stagiaire,
            "sexe": sexe_stagiaire,
            "nationalite": nationalite_stagiaire,
            "loisirs": loisirs_stagiaire
        }

        result = self.collection.insert_one(stagiaire)
        if result.inserted_id:
            messagebox.showinfo("Ajout", "Stagiaire ajouté avec succès!")
            self.maj_tableau_stagiaires()
        else:
            messagebox.showerror("Erreur", "Erreur lors de l'ajout du stagiaire!")

    def supprimer_stagiaire(self):
        id_stagiaire = self.entry_id.get()
        result = self.collection.delete_one({"id": id_stagiaire})
        if result.deleted_count == 1:
            messagebox.showinfo("Suppression", "Stagiaire supprimé avec succès!")
            self.maj_tableau_stagiaires()
        else:
            messagebox.showerror("Erreur", "Stagiaire introuvable!")

    def modifier_stagiaire(self):
        id_stagiaire = self.entry_id.get()
        nom_stagiaire = self.entry_nom.get()
        sexe_stagiaire = self.radio_sexe.get()
        nationalite_stagiaire = self.combo_nationalite.get()
        loisirs_stagiaire = []

        if self.check_lecture.get():
            loisirs_stagiaire.append("Lecture")
        if self.check_programmation.get():
            loisirs_stagiaire.append("Programmation")
        if self.check_sport.get():
            loisirs_stagiaire.append("Sport")

        stagiaire = {
            "id": id_stagiaire,
            "nom": nom_stagiaire,
            "sexe": sexe_stagiaire,
            "nationalite": nationalite_stagiaire,
            "loisirs": loisirs_stagiaire
        }

        result = self.collection.update_one({"id": id_stagiaire}, {"$set": stagiaire})
        if result.modified_count == 1:
            messagebox.showinfo("Modification", "Stagiaire modifié avec succès!")
            self.maj_tableau_stagiaires()
        else:
            messagebox.showerror("Erreur", "Stagiaire introuvable!")

    def rechercher_stagiaire(self):
        id_stagiaire = self.entry_id.get()
        stagiaire = self.collection.find_one({"id": id_stagiaire})
        if stagiaire:
            nom_stagiaire = stagiaire.get("nom", "")
            sexe_stagiaire = stagiaire.get("sexe", "")
            nationalite_stagiaire = stagiaire.get("nationalite", "")
            loisirs_stagiaire = ", ".join(stagiaire.get("loisirs", []))

            messagebox.showinfo("Résultat de recherche",
                                f"Nom: {nom_stagiaire}\nSexe: {sexe_stagiaire}\n"
                                f"Nationalité: {nationalite_stagiaire}\nLoisirs: {loisirs_stagiaire}")
        else:
            messagebox.showerror("Erreur", "Stagiaire introuvable!")

    def vider_champs(self):
        self.entry_id.delete(0, tk.END)
        self.entry_nom.delete(0, tk.END)
        self.radio_sexe.set("")
        self.combo_nationalite.set("")
        self.check_lecture.set(False)
        self.check_programmation.set(False)
        self.check_sport.set(False)

    def selectionner_stagiaire(self, event):
        selection = self.tableau_stagiaires.selection()
        if selection:
            item = self.tableau_stagiaires.item(selection[0])
            values = item["values"]
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, values[0])
            self.entry_nom.delete(0, tk.END)
            self.entry_nom.insert(0, values[1])
            self.radio_sexe.set(values[2])
            self.combo_nationalite.set(values[3])
            loisirs = values[4].split(", ")
            self.check_lecture.set("Lecture" in loisirs)
            self.check_programmation.set("Programmation" in loisirs)
            self.check_sport.set("Sport" in loisirs)


groupe = Groupe()
groupe.mainloop()
