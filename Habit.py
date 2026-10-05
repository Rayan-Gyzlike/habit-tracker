import json
from pathlib import Path
from datetime import datetime, timedelta

###Complete transition from CLI to GUI


# Загрузка привычек
def load_data():
    default_data = {"habits": []}
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / "Habit.json"
    if not file_path.exists() or file_path.stat().st_size == 0:
        with open(file_path, "w", encoding="utf8") as file:
            json.dump(default_data, file, ensure_ascii=False, indent=4)
    with open(file_path, encoding="utf8") as file:
        data = json.load(file)
    return data


# Сохранение всех привычек
def save_data(data):
    script_dir = Path(__file__).resolve().parent
    file_path = script_dir / "Habit.json"
    with open(file_path, "w", encoding="utf8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


### Добавление новой привычки
def add_habit(data, name):
    max_id = 0
    found = False
    if data["habits"]:
        for habit in data["habits"]:
            if name.lower() == habit["name"].lower():  # Проверка на одинаковые имена
                found = True
                break
            if habit.get("id") > max_id:  # Поиск айди для новой привычки
                max_id = habit.get("id")
    if not found:
        new_habit = {"id": max_id + 1, "name": name, "completed": []}
        data["habits"].append(new_habit)
    else:
        return "Такая привычка уже есть!!!"
    return data


# Запись дня привычки
def done_habit(data, habit_name):
    today = str(datetime.today().date())
    found_to_add_date = False
    for habit in data["habits"]:
        if habit["name"].lower() == habit_name.lower():
            found_to_add_date = True
            if today not in habit["completed"]:
                habit["completed"].append(today)
            else:
                return "Сегодня уже было!!!"
    if not (found_to_add_date):
        return "Нет такой привычки"
    return data


# Вывод привычек в терминал
def list_habits(data):
    lst = {}
    for habit in data["habits"]:
        lst[habit["id"]] = habit["name"]
    return lst


# Удалить привычку
def remove_habit(data, habit_name):
    found_to_remove = False
    for habit in data["habits"]:
        if habit_name.lower() == habit["name"].lower():
            found_to_remove = True
            break
    if found_to_remove:
        data["habits"] = [
            habit for habit in data["habits"] if habit["name"] != habit_name
        ]
        return f"Привычка {habit_name} - удалена", data
    else:
        return "Нет такой привычки!!!"


def stats_habit(data, name):
    current_streak = 0
    best_streak = 0
    dates = []
    not_found_name_habit = True
    if data.get("habits"):
        for habit in data["habits"]:
            if name.lower() == habit["name"].lower():
                dates = sorted([date for date in habit["completed"]])
                not_found_name_habit = False
                break
    if not_found_name_habit:
        print("Нет привычки с таким названием!!!")
        return 0, 0, 0, None
    if not dates:
        return 0, 0, 0, None

    all_days = len(dates)
    last_day = max(dates)

    dates = [datetime.strptime(date, "%Y-%m-%d").date() for date in dates]

    temp_streak = 1
    best_streak = 1

    for num in range(len(dates) - 1):
        if (dates[num + 1] - dates[num]).days == 1:
            temp_streak += 1
        else:
            if temp_streak > best_streak:
                best_streak = temp_streak
            temp_streak = 1

    if temp_streak > best_streak:
        best_streak = temp_streak

    today = datetime.today().date()
    yesterday = today - timedelta(days=1)

    if dates[-1] == today or dates[-1] == yesterday:
        current_streak = temp_streak

    if current_streak > best_streak:
        best_streak = current_streak

    return f"""
Статистика: {name}
          
Выполнено дней: {all_days}
Последнее выполнение: {last_day}
Текущая серия: {current_streak}
Лучшая серия: {best_streak}"""


def rename_habit(data, name, next_name):
    for habit in data["habits"]:
        if habit["name"].lower() == name.lower():
            habit["name"] = next_name
            return "Привычка переименована"
