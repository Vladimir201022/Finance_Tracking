import json
import argparse


def add_expense(budget, expenses, description, amount):
    if budget - amount >=0:
        expenses.append({
            "description": description,
            "amount": amount
        })
        print(f"Было добавлено: {description}, было потрачено: {amount}")
        return budget - amount
    else:
        print("Трата не может быть добавлена, недостаточно денег")
        return budget


def show_budget_details(first_budget, budget, expenses,new_budget):
    print(f"Изначально было денег: {first_budget}")
    print("Траты:")
    for expense in expenses:
        print(f"-{expense['description']}:{expense['amount']}")
    print(f"Потрачено: {get_total_expenses(expenses)}")
    print(f"Добавлено бюджета:{new_budget}")
    print(f"Текущий баланс: {budget}")


def get_total_expenses(expenses):
    total_expenses = 0
    for expense in expenses:
        total_expenses += expense['amount']
    return total_expenses


def save_budget_details(initial_budget, expenses, first_budget, filepath):
    budget_details = {
        "first_budget": first_budget,
        "initial_budget": initial_budget,
        "expenses": expenses
   }
    with open(filepath, 'w',encoding = "UTF-8") as file:
        json.dump(budget_details, file, ensure_ascii=False)


def load_budget_data(filepath):
    try:
        with open(filepath, 'r', encoding = "UTF-8") as file:
            data = json.load(file)
            return data["initial_budget"], data["expenses"], data["first_budget"]
    except(FileNotFoundError, json.JSONDecodeError):
        return 0, [], 0


def update_budget(budget):
    amount_of_money = float(input("Сколько денег вы хотите добавить: "))
    budget = budget + amount_of_money
    return amount_of_money,budget


def main():
    parser = argparse.ArgumentParser(description='Эта программа позволяет:Добавлять бюджет, проверять баланс, отслеживать свои траты, а также записывать их в файл')
    parser.add_argument("-f", "--filepath", help="Введите название файла", required=True)
    args = parser.parse_args()

    initial_budget,expenses,first_budget = load_budget_data(args.filepath)         
    print("Добро пожаловать, здесь вы сможете отслеживать ваши финансы")
    if initial_budget == 0:  
        initial_budget = float(input("Пожалуйста введите имеющееся у вас кол-во денег: "))
        first_budget = initial_budget
    if not expenses:
        expenses = []
    budget = initial_budget
    new_budget = 0
    while True:
        choise = int(input("""Чтобы вы хотели сделать? 
        1. Добавить траты
        2. Показать кол-во оставшихся денег
        3. Обновить бюджет
        4. Выйти
        Ваш выбор 1/2/3/4: 
    """
    ))
        if choise == 1:
            description = input("Введите описание ваших трат: ")
            amount = float(input("Введите сумму ваших трат: "))
            budget = add_expense(budget, expenses, description, amount)
        elif choise == 2:
            show_budget_details(first_budget, budget, expenses,new_budget)
        elif choise == 3:
            new_budget,budget = update_budget(budget)
        elif choise == 4:
            save_budget_details(budget, expenses, first_budget,args.filepath)
            print("Спасибо что воспользовались нашим приложением")
            break
        else:
            print("Проверьте ваш выбор")


if __name__ == "__main__":
    main()