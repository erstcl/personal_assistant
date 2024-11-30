from modules import notes, tasks, contacts, finance, calculator

def main_menu():
    while True:
        print("\nДобро пожаловать в Персональный помощник!")
        print("Выберите действие:")
        print("1. Управление заметками")
        print("2. Управление задачами")
        print("3. Управление контактами")
        print("4. Управление финансовыми записями")
        print("5. Калькулятор")
        print("6. Выход")

        choice = input("Введите номер действия: ").strip()
        if choice == "1":
            notes.menu()
        elif choice == "2":
            tasks.menu()
        elif choice == "3":
            contacts.menu()
        elif choice == "4":
            finance.menu()
        elif choice == "5":
            calculator.menu()
        elif choice == "6":
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
