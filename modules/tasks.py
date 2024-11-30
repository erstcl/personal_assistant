# import datetime
from utils.file_manager import FileManager

TASKS_FILE = "data/tasks.json"

def menu():
    while True:
        print("\nУправление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть задачи")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Экспорт задач в CSV")
        print("7. Импорт задач из CSV")
        print("8. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_task_completed()
        elif choice == "4":
            edit_task()
        elif choice == "5":
            delete_task()
        elif choice == "6":
            export_tasks_to_csv()
        elif choice == "7":
            import_tasks_from_csv()
        elif choice == "8":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def add_task():
    title = input("Введите название задачи: ").strip()
    description = input("Введите описание задачи: ").strip()
    priority = input("Выберите приоритет (Высокий/Средний/Низкий): ").strip()
    due_date = input("Введите срок выполнения (ДД-ММ-ГГГГ): ").strip()
    done = False
    tasks = FileManager.load_json(TASKS_FILE)
    task_id = max([task["id"] for task in tasks], default=0) + 1
    tasks.append({
        "id": task_id, "title": title, "description": description,
        "priority": priority, "due_date": due_date, "done": done
    })
    FileManager.save_json(TASKS_FILE, tasks)
    print("Задача успешно добавлена!")

def view_tasks():
    tasks = FileManager.load_json(TASKS_FILE)
    if not tasks:
        print("Задач пока нет.")
        return
    for task in tasks:
        status = "Выполнена" if task["done"] else "Не выполнена"
        print(f"[{task['id']}] {task['title']} - {status} | {task['priority']} | {task['due_date']}")

def mark_task_completed():
    tasks = FileManager.load_json(TASKS_FILE)
    view_tasks()
    task_id = int(input("Введите ID задачи для отметки как выполненной: ").strip())
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["done"] = True
        FileManager.save_json(TASKS_FILE, tasks)
        print("Задача успешно отмечена как выполненная!")
    else:
        print("Задача не найдена.")

def edit_task():
    tasks = FileManager.load_json(TASKS_FILE)
    view_tasks()
    task_id = int(input("Введите ID задачи для редактирования: ").strip())
    task = next((t for t in tasks if t["id"] == task_id), None)
    if task:
        task["title"] = input(f"Новое название ({task['title']}): ").strip() or task["title"]
        task["description"] = input(f"Новое описание ({task['description']}): ").strip() or task["description"]
        task["priority"] = input(f"Новый приоритет ({task['priority']}): ").strip() or task["priority"]
        task["due_date"] = input(f"Новый срок выполнения ({task['due_date']}): ").strip() or task["due_date"]
        FileManager.save_json(TASKS_FILE, tasks)
        print("Задача успешно обновлена!")
    else:
        print("Задача не найдена.")

def delete_task():
    tasks = FileManager.load_json(TASKS_FILE)
    view_tasks()
    task_id = int(input("Введите ID задачи для удаления: ").strip())
    tasks = [task for task in tasks if task["id"] != task_id]
    FileManager.save_json(TASKS_FILE, tasks)
    print("Задача успешно удалена!")

def export_tasks_to_csv():
    tasks = FileManager.load_json(TASKS_FILE)
    FileManager.export_to_csv("tasks_export.csv", tasks)
    print("Задачи экспортированы в tasks_export.csv.")

def import_tasks_from_csv():
    tasks = FileManager.import_from_csv("tasks_import.csv")
    if tasks:
        FileManager.save_json(TASKS_FILE, tasks)
        print("Задачи импортированы.")
