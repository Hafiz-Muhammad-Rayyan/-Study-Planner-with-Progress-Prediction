import json
import os

DATA_FILE = "study_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
    return data

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_study_session(data):
    print("\nEnter study session details:")
    date = input("Date (YYYY-MM-DD): ").strip()
    while True:
        try:
            hours = float(input("Hours studied: "))
            if hours < 0:
                print("Hours can't be negative. Try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")
    data.append({"date": date, "hours": hours})
    save_data(data)
    print("Session saved successfully!")

def linear_predict(data):
    if len(data) < 2:
        return None
    # Simple linear prediction y = mx + c based on index vs hours
    x_vals = list(range(len(data)))
    y_vals = [entry["hours"] for entry in data]
    n = len(data)
    sum_x = sum(x_vals)
    sum_y = sum(y_vals)
    sum_xy = sum(x*y for x,y in zip(x_vals,y_vals))
    sum_x2 = sum(x*x for x in x_vals)

    denominator = n*sum_x2 - sum_x*sum_x
    if denominator == 0:
        return None
    m = (n*sum_xy - sum_x*sum_y) / denominator
    c = (sum_y - m*sum_x) / n

    next_x = n
    predicted = m*next_x + c
    if predicted < 0:
        predicted = 0
    return round(predicted, 2)

def motivational_message(predicted):
    if predicted is None:
        return "Keep adding more sessions to get predictions!"
    elif predicted < 1:
        return "Don't give up! Start with small steps."
    elif predicted < 3:
        return "Good start! Try to increase your study hours gradually."
    elif predicted < 5:
        return "Great job! Keep the momentum going."
    else:
        return "Excellent work! You're on track to achieve your goals."

def show_progress(data):
    if not data:
        print("No study data available. Please add study sessions.")
        return
    print("\nYour Study Sessions:")
    for entry in data:
        print(f"- {entry['date']}: {entry['hours']} hours")

    predicted = linear_predict(data)
    if predicted is not None:
        print(f"\n📈 Predicted study hours for next session: {predicted} hours")
    else:
        print("\n📈 Not enough data to predict study hours.")

    print("\n" + motivational_message(predicted))

def main():
    print("📚 Personalized Study Planner with Progress Prediction")
    data = load_data()

    while True:
        print("\nMenu:")
        print("1. Add study session")
        print("2. View progress and prediction")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            add_study_session(data)
        elif choice == "2":
            show_progress(data)
        elif choice == "3":
            print("Thank you for using the Study Planner! Keep learning!")
            break
        else:
            print("Invalid choice! Please select 1, 2, or 3.")

if __name__ == "__main__":
    main()
