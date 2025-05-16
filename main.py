import sqlite3
from datetime import datetime

db_file = "forum.db"

def log(level, message):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log = f"[{timestamp}] {level}: {message}\n"
    try:
        with open("logi.txt", "a", encoding="utf-8") as file:
            file.write(log)
    except Exception:
        pass

class ForumManager:
    def __init__(self):
        self.connection = sqlite3.connect(db_file)
        self.db_init()
        self.current_user = None

    def db_init(self):
        cursor = self.connection.cursor()
        try:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT,
                    registered_at TEXT
                )
            """)
            
            cursor.execute("SELECT id FROM users WHERE username = ?", ("admin",))
            admin_exists = cursor.fetchone()
            if not admin_exists:
                cursor.execute("INSERT INTO users (username, password, registered_at) VALUES (?, ?, ?)",
                          ("admin", "admin", datetime.now()))

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    author_id INTEGER,
                    title TEXT,
                    content TEXT,
                    created_at TEXT,
                    FOREIGN KEY(author_id) REFERENCES users(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    author_id INTEGER,
                    content TEXT,
                    created_at TEXT,
                    FOREIGN KEY(post_id) REFERENCES posts(id),
                    FOREIGN KEY(author_id) REFERENCES users(id)
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS likes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_id INTEGER,
                    user_id INTEGER,
                    UNIQUE(post_id, user_id),
                    FOREIGN KEY(post_id) REFERENCES posts(id),
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """)
            self.connection.commit()
            log("INFO", "Inicjacja bazy danych zakończona")
        except Exception as e:
            log("BŁĄD", f"Błąd inicjacji DB: {e}")

    def register(self):
        try:
            username = input("Login: ").strip()
            password = input("Hasło: ").strip()
            current_date = datetime.now()
            
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                print("Login zajęty.")
                log("BŁĄD", f"Próbowano użyć zajęty login: {username}")
                return

            self.connection.execute(
                "INSERT INTO users (username,password,registered_at) VALUES (?,?,?)",
                (username, password, current_date)
            )
            self.connection.commit()
            log("INFO", f"Użytkownik zarejestrowany: {username}")
            print("Rejestracja zakończona.")
        except Exception as e:
            print("Błąd rejestracji.")
            log("BŁĄD", f"Wystąpił błąd przy rejestracji: {e}")

    def login(self):
        username = input("Login: ").strip()
        password = input("Hasło: ").strip()
        cursor = self.connection.cursor()
        cursor.execute(
            "SELECT id, username, password, registered_at FROM users WHERE username=? AND password=?",
            (username, password)
        )
        user_data = cursor.fetchone()
        if user_data:
            self.current_user = {
                'id': user_data[0],
                'username': user_data[1],
                'registered_at': user_data[3]
            }
            log("INFO", f"Zalogowano jako {username}")
            print(f"Witaj, {username}!")
            return True
        else:
            print("Nieprawidłowe dane.")
            log("BŁĄD", f"Nieudane logowanie: {username}")
            return False

    def logout(self):
        if self.current_user:
            log("INFO", f"Wylogowano: {self.current_user['username']}")
        self.current_user = None
        print("Wylogowano.")

    def create_post(self):
        if not self.current_user:
            print("Musisz być zalogowany, aby dodać post.")
            return

        title = input("Tytuł: ").strip()
        content = input("Treść:\n").strip()
        current_date = datetime.now()
        try:
            self.connection.execute(
                "INSERT INTO posts (author_id,title,content,created_at) VALUES (?,?,?,?)",
                (self.current_user['id'], title, content, current_date)
            )
            self.connection.commit()
            log("INFO", f"Post utworzony przez {self.current_user['username']}: {title}")
            print("Post dodany.")
        except Exception as e:
            print("Błąd dodawania posta.")
            log("BŁĄD", f"Wystąpił błąd przy tworzeniu posta: {e}")

    def list_posts(self):
        sql_query = """
            SELECT p.id, p.title, u.username, p.created_at,
                   COUNT(DISTINCT c.id), COUNT(DISTINCT l.id)
            FROM posts p
            JOIN users u ON p.author_id = u.id
            LEFT JOIN comments c ON p.id = c.post_id
            LEFT JOIN likes l ON p.id = l.post_id
            GROUP BY p.id, p.title, u.username, p.created_at
            ORDER BY p.created_at DESC
        """
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        all_posts = cursor.fetchall()
        
        if not all_posts:
            print("Brak postów.")
            return
        
        print("\n--- Lista Postów ---")
        for post in all_posts:
            post_id, title, author, created_at, comments_count, likes_count = post
            print(f"{post_id}. {title} (autor: {author}) [{likes_count} like, {comments_count} komentarzy]")

    def view_post(self):
        if not self.current_user:
            print("Musisz być zalogowany, aby przeglądać posty.")
            return
            
        post_id = input("ID posta: ")
        try:
            post_id = int(post_id)
        except ValueError:
            print("Nieprawidłowe ID.")
            return

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT p.id, p.title, p.content, p.created_at, p.author_id, u.username
            FROM posts p JOIN users u ON p.author_id=u.id
            WHERE p.id=?
        """, (post_id,))
        post_data = cursor.fetchone()

        if not post_data:
            print("Nie znaleziono posta.")
            return

        fetched_post_id = post_data[0]
        fetched_post_title = post_data[1]
        fetched_post_content = post_data[2]
        fetched_post_created_at = post_data[3]
        fetched_post_author_id = post_data[4]
        fetched_post_author_username = post_data[5]

        print(f"\n--- {fetched_post_title} ---")
        print(f"Autor: {fetched_post_author_username} | Data: {fetched_post_created_at}")
        print(fetched_post_content)
        
        cursor = self.connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM likes WHERE post_id=?", (post_id,))
        likes = cursor.fetchone()[0]
        print(f"[{likes} like]")

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT c.id, u.username, c.content, c.created_at
            FROM comments c JOIN users u ON c.author_id=u.id
            WHERE c.post_id=?
            ORDER BY c.created_at
        """, (post_id,))
        comments = cursor.fetchall()
        
        print(f"-- Komentarze ({len(comments)}) --")
        for comment in comments:
            comment_id, comment_author, comment_content, comment_created_at = comment
            print(f"{comment_id}. {comment_author} @ {comment_created_at}: {comment_content}")
        
        print("\n1. Dodaj komentarz\n2. Polub post")
        if self.current_user['username'] == 'admin' or fetched_post_author_id == self.current_user['id']:
            print("3. Usuń/edytuj post")
        print("0. Powrót")
        
        choice = input("Wybór: ")
        if choice == '1':
            self.add_comment(post_id)
        elif choice == '2':
            self.like_post(post_id)
        elif choice == '3' and (self.current_user['username'] == 'admin' or fetched_post_author_id == self.current_user['id']):
            self.moderate_post(post_id)

    def add_comment(self, target_post_id):
        if not self.current_user:
            print("Musisz być zalogowany, aby dodać komentarz.")
            return

        comment_text = input("Twój komentarz:\n").strip()
        if not comment_text:
            print("Komentarz nie może być pusty.")
            return
            
        current_date = datetime.now()
        try:
            self.connection.execute(
                "INSERT INTO comments (post_id,author_id,content,created_at) VALUES (?,?,?,?)",
                (target_post_id, self.current_user['id'], comment_text, current_date)
            )
            self.connection.commit()
            log("INFO", f"Komentarz dodany przez {self.current_user['username']} do posta {target_post_id}")
            print("Komentarz dodany.")
        except Exception as e:
            print("Błąd dodawania komentarza.")
            log("BŁĄD", f"Wystąpił błąd podczas dodawania komentarza: {e}")

    def like_post(self, target_post_id):
        if not self.current_user:
            print("Musisz być zalogowany, aby polubić post.")
            return
            
        try:
            self.connection.execute(
                "INSERT INTO likes (post_id,user_id) VALUES (?,?)",
                (target_post_id, self.current_user['id'])
            )
            self.connection.commit()
            log("INFO", f"{self.current_user['username']} polubił post {target_post_id}")
            print("Post polubiony.")
        except sqlite3.IntegrityError:
            print("Już polubiłeś ten post.")
        except Exception as e:
            print("Błąd polubienia.")
            log("BŁĄD", f"Wystąpił błąd podczas polubiania postu: {e}")

    def moderate_post(self, target_post_id):
        print("\n--- Moderacja Posta ---")
        print("1. Usuń post\n2. Edytuj post\n0. Anuluj")
        choice = input("Wybór: ")
        
        if choice == '1':
            confirmation = input(f"Czy na pewno chcesz usunąć post ID {target_post_id}? (tak/nie): ").strip().lower()
            if confirmation == 'tak':
                try:
                    self.connection.execute("DELETE FROM likes WHERE post_id=?", (target_post_id,))
                    self.connection.execute("DELETE FROM comments WHERE post_id=?", (target_post_id,))
                    self.connection.execute("DELETE FROM posts WHERE id=?", (target_post_id,))
                    self.connection.commit()
                    log("INFO", f"Post {target_post_id} usunięty przez {self.current_user['username']}")
                    print("Post usunięty.")
                except Exception as e:
                    print("Błąd usuwania posta.")
                    log("BŁĄD", f"Delete post: {e}")
            else:
                print("Usuwanie anulowane.")
        elif choice == '2':
            title = input("Nowy tytuł (zostaw puste by nie zmieniać):\n").strip()
            content = input("Nowa treść (zostaw puste by nie zmieniać):\n").strip()

            list_of_updates = []
            list_of_parameters = []

            if title:
                list_of_updates.append("title=?")
                list_of_parameters.append(title)
            if content:
                list_of_updates.append("content=?")
                list_of_parameters.append(content)
            
            if not list_of_updates:
                print("Nie wprowadzono żadnych zmian.")
                return

            list_of_parameters.append(target_post_id)
            sql_update_query = f"UPDATE posts SET {', '.join(list_of_updates)} WHERE id=?"
            
            try:
                self.connection.execute(sql_update_query, tuple(list_of_parameters))
                self.connection.commit()
                log("INFO", f"Post {target_post_id} edytowany przez {self.current_user['username']}")
                print("Post zaktualizowany.")
            except Exception as e:
                print("Błąd edycji.")
                log("BŁĄD", f"Wystąpił błąd podczas edycji posta: {e}")
        elif choice == '0':
            print("Moderacja anulowana.")
        else:
            print("Nieznana opcja.")

    def search_posts(self):
        search = input("Szukaj (tytuł/treść): ").strip().lower()
        if not search:
            print("Nie wpisano szukanej frazy.")
            return

        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT p.id, p.title, u.username
            FROM posts p JOIN users u ON p.author_id=u.id
            WHERE LOWER(p.title) LIKE ? OR LOWER(p.content) LIKE ?
            ORDER BY p.created_at DESC
        """, (f"%{search}%", f"%{search}%"))
        results = cursor.fetchall()
        
        if not results:
            print("Brak wyników.")
        else:
            print("\n--- Wyniki Wyszukiwania ---")
            for result in results:
                post_id, post_title, author_username = result
                print(f"{post_id}. {post_title} (autor: {author_username})")
    def run(self):
        while True:
            if not self.current_user:
                print("\n--- Witaj na Forum! ---")
                print("1. Zarejestruj się")
                print("2. Zaloguj się")
                print("0. Wyjdź")
                choice = input("Wybór: ").strip()
                if choice == '1':
                    self.register()
                elif choice == '2':
                    self.login()
                elif choice == '0':
                    print("Do zobaczenia!")
                    break
                else:
                    print("Nieznana opcja. Spróbuj ponownie.")
            else:
                print(f"\n== MENU GŁÓWNE (zalogowano jako: {self.current_user['username']}) ==")
                print("1. Utwórz nowy post")
                print("2. Wyświetl wszystkie posty")
                print("3. Przeglądaj konkretny post (podaj ID)")
                print("4. Wyszukaj posty")
                print("5. Wyloguj")
                choice = input("Wybór: ").strip()
                
                if choice == '1':
                    self.create_post()
                elif choice == '2':
                    self.list_posts()
                elif choice == '3':
                    self.view_post()
                elif choice == '4':
                    self.search_posts()
                elif choice == '5':
                    self.logout()
                else:
                    print("Nieznana opcja. Spróbuj ponownie.")
        
        if self.connection:
            self.connection.close()
            log("INFO", "Połączenie z bazą danych zostało zamknięte.")

def main():
    forum_manager = ForumManager()
    forum_manager.run()

if __name__ == '__main__':
    main()