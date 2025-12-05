from ui.main_window import App
from db.database import init_db


# need to encrypt/decrypt by chunks
# need to credit icons8 for the icons
# add hover property for bound labels
# style ui
# more error handling

if __name__ == "__main__":
    init_db()
    app = App()
    app.run()
                     
    
