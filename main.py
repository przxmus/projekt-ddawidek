import sqlite3
from datetime import datetime

class Log:
    def info(self, message):
        self._log("INFO", message)
    
    def error(self, message):
        self._log("BŁĄD", message)
    
    def _log(self, type, message):
        timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        log_entry = f"[{timestamp}] {type}: {message}\n"
        try:
            with open("logi.txt", 'a', encoding="utf-8") as file:
                file.write(log_entry)
        except Exception:
            pass

class Task:
    def __init__(self, content):
        self.content = content
        self.done = False

class TaskManager:
    def __init__(self, username):
        self.tasks = []
        self.username = username
        self.db_file = f"{username}.db"
        self.log = Log()
        self.load_sqlite()
        
    def add_task(self, content):
        try:
            task = Task(content)
            self.tasks.append(task)
            self.log.info(f"{self.username} dodał zadanie \"{content}\"")
            self.save_sqlite()
        except Exception as e:
            self.log.error(f"Błąd przy dodawaniu zadania: {e}")

    def list_tasks(self):
        try:
            for id, task in enumerate(self.tasks, 1):
                status = "Zrobione!" if task.done else "Do zrobienia."
                print(f"{id}. {task.content} | {status}")
        except Exception as e:
            self.log.error(f"Błąd przy wyświetlaniu zadań: {e}")

    def mark_done(self, id):
        try:
            if id > 0 and id <= len(self.tasks):
                self.tasks[id-1].done = True
                self.log.info(f"{self.username} oznaczył zadanie \"{self.tasks[id-1].content}\" jako zrobione")
                self.save_sqlite()
            else:
                raise IndexError("Nieprawidłowe ID zadania")
        except Exception as e:
            self.log.error(f"Błąd przy oznaczaniu zadania jako zrobione: {e}")

    def delete_task(self, id):
        try:
            if id > 0 and id <= len(self.tasks):
                content = self.tasks[id-1].content
                self.tasks.pop(id-1)
                self.log.info(f"{self.username} usunął zadanie \"{content}\"")
                self.save_sqlite()
            else:
                raise IndexError("Nieprawidłowe ID zadania")
        except Exception as e:
            self.log.error(f"Błąd przy usuwaniu zadania: {e}")

    def search(self, keyword):
        try:
            for id, task in enumerate(self.tasks, 1):
                if keyword.lower() in task.content.lower():
                    status = "Zrobione!" if task.done else "Do zrobienia."
                    print(f"{id}. {task.content} | {status}")
        except Exception as e:
            self.log.error(f"Błąd przy wyszukiwaniu zadań: {e}")

    def save_sqlite(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT, done INTEGER)')
            cursor.execute('DELETE FROM tasks')
            for task in self.tasks:
                cursor.execute('INSERT INTO tasks (content, done) VALUES (?, ?)', (task.content, int(task.done)))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            self.log.error(f"Błąd bazy danych: {e}")

    def load_sqlite(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, content TEXT, done INTEGER)')
            cursor.execute('SELECT content, done FROM tasks')
            rows = cursor.fetchall()
            self.tasks = []
            for row in rows:
                task = Task(row[0])
                task.done = bool(row[1])
                self.tasks.append(task)
            conn.close()
        except sqlite3.Error as e:
            self.log.error(f"Błąd bazy danych: {e}")


def main():
    log = Log()
    print("\n==== TODO ZADAŃ ====")
    username = input("Nazwa użytkownika: ")
    try:
        manager = TaskManager(username)
    except Exception as e:
        log.error(f"Błąd podczas inicjalizacji menedżera zadań: {e}")
        return
    
    while True:
        print("\n==== LISTA ZADAŃ ====")
        print("1. Dodaj zadanie")
        print("2. Lista zadań")
        print("3. Oznacz zadanie jako zrobione")
        print("4. Usuń zadanie")
        print("5. Wyszukaj zadanie")
        print("0. Wyjdź")
        choice = input("Wybierz opcję: ")
        try:
            choice = int(choice)
        except ValueError:
            print("Niepoprawny wybór. Wybierz ponownie.")
            log.error(f"Niepoprawny wybór w menu: {choice}")
            continue
        if choice == 1:
            content = input("Treść zadania: ")
            manager.add_task(content)
        elif choice == 2:
            manager.list_tasks()
        elif choice == 3:
            id_input = input("ID: ")
            try:
                id_val = int(id_input)
                manager.mark_done(id_val)
            except ValueError:
                print("Nieprawidłowe ID. Podaj liczbę.")
                manager.log.error(f"Nieprawidłowe ID przy oznaczaniu: {id_input}")
        elif choice == 4:
            id_input = input("ID: ")
            try:
                id_val = int(id_input)
                manager.delete_task(id_val)
            except ValueError:
                print("Nieprawidłowe ID. Podaj liczbę.")
                manager.log.error(f"Nieprawidłowe ID przy usuwaniu: {id_input}")
        elif choice == 5:
            search = input("Co wyszukać: ")
            manager.search(search)
        elif choice == 0:
            break

if __name__ == '__main__':
    main()
