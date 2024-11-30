from utils.file_manager import FileManager

CONTACTS_FILE = "data/contacts.json"

def menu():
    while True:
        print("\nУправление контактами:")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Экспорт контактов в CSV")
        print("6. Импорт контактов из CSV")
        print("7. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_contact()
        elif choice == "2":
            search_contact()
        elif choice == "3":
            edit_contact()
        elif choice == "4":
            delete_contact()
        elif choice == "5":
            export_contacts_to_csv()
        elif choice == "6":
            import_contacts_from_csv()
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def add_contact():
    name = input("Введите имя: ").strip()
    phone = input("Введите номер телефона: ").strip()
    email = input("Введите адрес электронной почты: ").strip()
    contacts = FileManager.load_json(CONTACTS_FILE)
    contact_id = max([contact["id"] for contact in contacts], default=0) + 1
    contacts.append({"id": contact_id, "name": name, "phone": phone, "email": email})
    FileManager.save_json(CONTACTS_FILE, contacts)
    print("Контакт успешно добавлен!")

def search_contact():
    query = input("Введите имя или номер телефона для поиска: ").strip()
    contacts = FileManager.load_json(CONTACTS_FILE)
    results = [contact for contact in contacts if query in contact["name"] or query in contact["phone"]]
    if results:
        for contact in results:
            print(f"[{contact['id']}] {contact['name']} - {contact['phone']} | {contact['email']}")
    else:
        print("Контакты не найдены.")

def edit_contact():
    contacts = FileManager.load_json(CONTACTS_FILE)
    search_contact()
    contact_id = int(input("Введите ID контакта для редактирования: ").strip())
    contact = next((c for c in contacts if c["id"] == contact_id), None)
    if contact:
        contact["name"] = input(f"Новое имя ({contact['name']}): ").strip() or contact["name"]
        contact["phone"] = input(f"Новый телефон ({contact['phone']}): ").strip() or contact["phone"]
        contact["email"] = input(f"Новый email ({contact['email']}): ").strip() or contact["email"]
        FileManager.save_json(CONTACTS_FILE, contacts)
        print("Контакт успешно обновлен!")
    else:
        print("Контакт не найден.")

def delete_contact():
    contacts = FileManager.load_json(CONTACTS_FILE)
    search_contact()
    contact_id = int(input("Введите ID контакта для удаления: ").strip())
    contacts = [contact for contact in contacts if contact["id"] != contact_id]
    FileManager.save_json(CONTACTS_FILE, contacts)
    print("Контакт успешно удален!")

def export_contacts_to_csv():
    contacts = FileManager.load_json(CONTACTS_FILE)
    FileManager.export_to_csv("contacts_export.csv", contacts)
    print("Контакты экспортированы в contacts_export.csv.")

def import_contacts_from_csv():
    contacts = FileManager.import_from_csv("contacts_import.csv")
    if contacts:
        FileManager.save_json(CONTACTS_FILE, contacts)
        print("Контакты импортированы.")
