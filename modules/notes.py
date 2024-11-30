import datetime
from utils.file_manager import FileManager

NOTES_FILE = "data/notes.json"

def menu():
    while True:
        print("\nУправление заметками:")
        print("1. Добавить новую заметку")
        print("2. Просмотреть заметки")
        print("3. Редактировать заметку")
        print("4. Удалить заметку")
        print("5. Экспорт заметок в CSV")
        print("6. Импорт заметок из CSV")
        print("7. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_note()
        elif choice == "2":
            view_notes()
        elif choice == "3":
            edit_note()
        elif choice == "4":
            delete_note()
        elif choice == "5":
            export_notes_to_csv()
        elif choice == "6":
            import_notes_from_csv()
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def add_note():
    title = input("Введите заголовок заметки: ").strip()
    content = input("Введите содержимое заметки: ").strip()
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    notes = FileManager.load_json(NOTES_FILE)
    note_id = max([note["id"] for note in notes], default=0) + 1
    notes.append({"id": note_id, "title": title, "content": content, "timestamp": timestamp})
    FileManager.save_json(NOTES_FILE, notes)
    print("Заметка успешно добавлена!")

def view_notes():
    notes = FileManager.load_json(NOTES_FILE)
    if not notes:
        print("Заметок пока нет.")
        return
    for note in notes:
        print(f"[{note['id']}] {note['title']} - {note['timestamp']}")

def edit_note():
    notes = FileManager.load_json(NOTES_FILE)
    view_notes()
    note_id = int(input("Введите ID заметки для редактирования: ").strip())
    note = next((n for n in notes if n["id"] == note_id), None)
    if note:
        note["title"] = input(f"Новый заголовок ({note['title']}): ").strip() or note["title"]
        note["content"] = input(f"Новое содержимое ({note['content']}): ").strip() or note["content"]
        note["timestamp"] = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        FileManager.save_json(NOTES_FILE, notes)
        print("Заметка успешно обновлена!")
    else:
        print("Заметка не найдена.")

def delete_note():
    notes = FileManager.load_json(NOTES_FILE)
    view_notes()
    note_id = int(input("Введите ID заметки для удаления: ").strip())
    notes = [note for note in notes if note["id"] != note_id]
    FileManager.save_json(NOTES_FILE, notes)
    print("Заметка успешно удалена!")

def export_notes_to_csv():
    notes = FileManager.load_json(NOTES_FILE)
    FileManager.export_to_csv("notes_export.csv", notes)
    print("Заметки экспортированы в notes_export.csv.")

def import_notes_from_csv():
    notes = FileManager.import_from_csv("notes_import.csv")
    if notes:
        FileManager.save_json(NOTES_FILE, notes)
        print("Заметки импортированы.")
