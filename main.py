from ui.main_window import App
from db.database import init_db


# need to add max file size
# need to add warning about encryption password
# need to implement 15 min time limit for verif code



if __name__ == "__main__":
    init_db()
    app = App()
    app.run()
                     
    
