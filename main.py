
from flask_app import app

def main():
    try:
        app.run()
    # except SystemExit as e:
    #     import sys
    #     sys.exit(3)
    #     import traceback
    #     import sys
        
    #     print(traceback.format_exc())
    #     # or
    #     print(sys.exc_info()[2])
    #     print(e)
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()