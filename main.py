from blockchain import Blockchain

def afficher_menu():
    print("\n=== MENU BLOCKCHAIN ===")
    print("1. Ajouter une transaction")
    print("2. Miner un bloc")
    print("3. Afficher la blockchain")
    print("4. Vérifier la validité de la chaîne")
    print("5. Quitter")
    print("6. Charger une chaîne concurrente")

def afficher_blockchain(bc):
    for block in bc.chain:
        print(f"\nBloc #{block.index}")
        print(f"Timestamp     : {block.timestamp}")
        print(f"Hash          : {block.hash}")
        print(f"Précédent     : {block.previous_hash}")
        print(f"Nonce         : {block.nonce}")
        print("Transactions  :")
        for tx in block.transactions:
            print(f"  - {tx.sender} → {tx.recipient} : {tx.amount}")

if __name__ == "__main__":
    bc = Blockchain()

    while True:
        afficher_menu()
        choix = input("Choix : ").strip()

        if choix == "1":
            sender = input("Expéditeur : ")
            recipient = input("Destinataire : ")
            try:
                amount = float(input("Montant : "))
            except ValueError:
                print("Montant invalide.")
                continue
            bc.add_transaction(sender, recipient, amount)
            print("Transaction ajoutée.")

        
        elif choix == "2":
            success = bc.mine_pending_transactions()
            if success:
                print("Bloc miné avec succès.")
                bc.save_to_file()

        elif choix == "3":
            afficher_blockchain(bc)

        elif choix == "4":
            if bc.is_chain_valid():
                print("La blockchain est valide.")
            else:
                print("La blockchain est invalide.")

        elif choix == "5":
            bc.save_to_file()
            print("Blockchain sauvegardée.")
            break
        
        elif choix == "6":
            nom_fichier = input("Nom du fichier de la chaîne concurrente (.json) : ")
            nouvelle_chaine = bc.load_external_chain(nom_fichier)
            if nouvelle_chaine:
                bc.replace_chain(nouvelle_chaine)


        else:
            print("Choix invalide.")

        
        
