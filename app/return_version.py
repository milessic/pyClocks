from src.__init__ import VERSION

def return_version():
    return "_" + VERSION.replace(".","_")
if __name__ == "__main__":
    print(return_version())

