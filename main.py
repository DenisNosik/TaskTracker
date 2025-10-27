import datetime
import json


class TaskTracker():
    def __init__(self):
        self.my_tasks_json_file = "tasks.json"
        self.all_tasks_created = 0
        self._ensure_file_exists()

    def _ensure_file_exists(self): # Creating json file if it's not existing
        try:
            with open(self.my_tasks_json_file, "r") as file:
                json.load(file)
        except FileNotFoundError:
            with open(self.my_tasks_json_file, "w") as file:
                json.dump({"all_tasks": []}, file, indent=4)

    def run(self): # running the code
        while True:
            if self.all_tasks_created > 0: # shows your tasks if it's more than 0
                print("\n----- YOUR TASKS -----")
                self.get_all_tasks()
                print("----------------------\n")

            print("------- MENU -------")
            print("1. Create a new task")
            print("2. Update existing task")
            print("3. Delete existing task")
            print("4. Exit")
            print("---------------------")

            input_select_option = input("Select an option (1 to 4): ")
            if input_select_option.isdigit():
                match input_select_option:  # match for MENU options
                    case "1": # CREATE NEW TASK
                        self.create_task_option()
                        continue
                    case "2": # UPDATE TASK STATUS
                        if self.all_tasks_created > 0:
                            self.update_task_option()
                            continue
                        else:
                            print("\nYou don't have any tasks yet.\n")
                            continue
                    case "3": # DELETE TASK
                        if self.all_tasks_created > 0:
                            self.delete_task_option()
                            continue
                        else:
                            print("\nYou don't have any tasks yet.\n")
                            continue
                    case "4": # EXIT
                        break
                    case _: # if user entered wrong number
                        print("Wrong input. Please try again.")
                        continue
            else: # if user entered a letter instead of number
                print("Wrong input. Please try again.")
                continue

    def create_task_option(self): # option 1 in menu
        input_new_task_name = input("\nEnter new task name: ")
        self.create_task(input_new_task_name)
        self.all_tasks_created += 1

    def update_task_option(self): # option 2 in menu
        print("\n----- Which task would you like to update? -----")
        self.get_all_tasks()
        print("------------------------------------------------\n")
        input_task_number = input(f"Enter task number to update (1 - {self.all_tasks_created}): ")
        if input_task_number.isdigit():
            input_task_number = int(input_task_number)
        else:
            print("Wrong Input!")
        if input_task_number > self.all_tasks_created:
            print("Wrong Number!")
        else:
            task_to_update = self.get_task(input_task_number)
            num_for_status = input("\nEnter new status (1 - todo; 2 - in-progress; 3 - done): ").lower()
            match num_for_status:
                case "1":
                    self.update_task_status(task_to_update["id"], "todo")
                case "2":
                    self.update_task_status(task_to_update["id"], "in-progress")
                case "3":
                    self.update_task_status(task_to_update["id"], "done")
                case _:
                    print("Something went wrong")

    def delete_task_option(self): # option 3 in menu
        print("\n----- Which task would you like to delete? -----")
        self.get_all_tasks()
        print("------------------------------------------------\n")
        input_delete_number = input(f"\nEnter task number to delete(1 - {self.all_tasks_created}): ")
        if input_delete_number.isdigit():
            input_delete_number = int(input_delete_number)
        else:
            print("Wrong Input!")
        if input_delete_number > self.all_tasks_created:
            print("Wrong Number!")
        else:
            task_to_delete = self.get_task(input_delete_number)
            self.delete_task(task_to_delete["id"])
            self.all_tasks_created -= 1

    def reset_tasks(self): # reset all tasks in json file
        with open(self.my_tasks_json_file, "r") as file:
            file_data = json.load(file)
            file_data["all_tasks"].clear()
            with open(self.my_tasks_json_file, "w") as file:
                json.dump(file_data, file, indent=4)

    def create_task(self, task_name): # creating new task
        new_task = {
            "id": self.all_tasks_created + 1,
            "name": task_name,
            "status": "todo",
            "createdAt": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "updatedAt": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }

        with open(self.my_tasks_json_file, "r+") as file: #read file "tasks.json" and add new task in it
            file_data = json.load(file)
            file_data["all_tasks"].append(new_task)
            file.seek(0)
            json.dump(file_data, file, indent=4)

    def get_all_tasks(self): # get all existing tasks
        with open(self.my_tasks_json_file, "r") as file:
            file_data = json.load(file)
            for task in file_data["all_tasks"]:
                if task["id"] > 0:
                    print(
                        f"#{task['id']}. "
                        f"{task['name']} | "
                        f"status: {task['status']} | "
                        f"created: {task['createdAt']} | "
                        f"updated: {task['updatedAt']}"
                    )

    def get_task(self, task_id): # get one specific task from "tasks.json" by task id
        with open(self.my_tasks_json_file, "r") as file:
            file_data = json.load(file)
            for task in file_data["all_tasks"]:
                if task["id"] == task_id:
                    return task
            else:
                return None

    def update_task_status(self, task_id, new_status): # updating task status by task id
        with open(self.my_tasks_json_file, "r") as file:
            file_data = json.load(file)
            for task in file_data["all_tasks"]:
                if task["id"] == task_id:
                    task["status"] = new_status
                    task["updatedAt"] = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            with open(self.my_tasks_json_file, "w") as f:
                json.dump(file_data, f, indent=4)

    def delete_task(self, task_id): #deleting one specific task by task id
        with open(self.my_tasks_json_file, "r") as file:
            file_data = json.load(file)
            for task in file_data["all_tasks"]:
                if task["id"] == task_id:
                    file_data["all_tasks"].remove(task)
            for task in file_data["all_tasks"]:
                if task["id"] > task_id:
                    task["id"] = task["id"] - 1

            with open(self.my_tasks_json_file, "w") as f:
                json.dump(file_data, f, indent=4)

if __name__ == "__main__":
    task_traker = TaskTracker()
    task_traker.reset_tasks()
    task_traker.run()

