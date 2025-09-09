import sys, subprocess, importlib, os

req = [("PyQt6","PyQt6"),("PIL","Pillow"),("numpy","numpy")]

def has(m):
    try:
        importlib.import_module(m)
        return True
    except:
        return False

def pip_install(pkg):
    return subprocess.call([sys.executable,"-m","pip","install",pkg]) == 0 or subprocess.call([sys.executable,"-m","pip","install","--user",pkg]) == 0

def ensure():
    missing = [(m,p) for m,p in req if not has(m)]
    if not missing:
        return True
    for m,p in missing:
        if not pip_install(p):
            return False
    return all(has(m) for m,_ in req)

def run():
    base = os.path.dirname(__file__)
    sys.path.insert(0, base)
    mod = importlib.import_module("app.main")
    mod.main()

if __name__ == "__main__":
    if not ensure():
        print("Dependencies missing and automatic install failed.")
        sys.exit(1)
    run()
