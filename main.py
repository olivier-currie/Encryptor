from ui.main_window import App
from db.database import init_db


# need to add max file size
# might need to create an about page
# need to credit icons8 for the icons
# need to add account info page
# add input/output file history
# add hover property for bound labels
# style ui
# fix timestamp est


if __name__ == "__main__":
    init_db()
    app = App()
    app.run()
                     
    
