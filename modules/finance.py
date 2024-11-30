from utils.file_manager import FileManager

FINANCE_FILE = "data/finance.json"

def menu():
    while True:
        print("\nУправление финансовыми записями:")
        print("1. Добавить новую запись")
        print("2. Просмотреть все записи")
        print("3. Генерация отчёта")
        print("4. Удалить запись")
        print("5. Экспорт финансовых записей в CSV")
        print("6. Импорт финансовых записей из CSV")
        print("7. Назад")

        choice = input("Выберите действие: ").strip()
        if choice == "1":
            add_finance_record()
        elif choice == "2":
            view_records()
        elif choice == "3":
            generate_report()
        elif choice == "4":
            delete_record()
        elif choice == "5":
            export_records_to_csv()
        elif choice == "6":
            import_records_from_csv()
        elif choice == "7":
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

def add_finance_record():
    amount = float(input("Введите сумму (положительное значение для дохода, отрицательное для расхода): ").strip())
    category = input("Введите категорию (например, Еда, Транспорт): ").strip()
    date = input("Введите дату (ДД-ММ-ГГГГ): ").strip()
    description = input("Введите описание: ").strip()
    records = FileManager.load_json(FINANCE_FILE)
    record_id = max([record["id"] for record in records], default=0) + 1
    records.append({
        "id": record_id, "amount": amount, "category": category,
        "date": date, "description": description
    })
    FileManager.save_json(FINANCE_FILE, records)
    print("Запись успешно добавлена!")

def view_records():
    records = FileManager.load_json(FINANCE_FILE)
    if not records:
        print("Записей пока нет.")
        return
    for record in records:
        print(f"[{record['id']}] {record['date']} | {record['category']} | {record['amount']} | {record['description']}")

def generate_report():
    start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ").strip()
    end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ").strip()
    records = FileManager.load_json(FINANCE_FILE)
    filtered_records = [
        r for r in records if start_date <= r["date"] <= end_date
    ]
    income = sum(r["amount"] for r in filtered_records if r["amount"] > 0)
    expenses = sum(r["amount"] for r in filtered_records if r["amount"] < 0)
    balance = income + expenses
    print(f"Финансовый отчёт за период с {start_date} по {end_date}:")
    print(f"- Общий доход: {income}")
    print(f"- Общие расходы: {expenses}")
    print(f"- Баланс: {balance}")
    FileManager.export_to_csv(f"report_{start_date}_{end_date}.csv", filtered_records)
    print(f"Подробная информация сохранена в report_{start_date}_{end_date}.csv")

def delete_record():
    records = FileManager.load_json(FINANCE_FILE)
    view_records()
    record_id = int(input("Введите ID записи для удаления: ").strip())
    records = [record for record in records if record["id"] != record_id]
    FileManager.save_json(FINANCE_FILE, records)
    print("Запись успешно удалена!")

def export_records_to_csv():
    records = FileManager.load_json(FINANCE_FILE)
    FileManager.export_to_csv("finance_export.csv", records)
    print("Записи экспортированы в finance_export.csv.")

def import_records_from_csv():
    records = FileManager.import_from_csv("finance_import.csv")
    if records:
        FileManager.save_json(FINANCE_FILE, records)
        print("Записи импортированы.")
