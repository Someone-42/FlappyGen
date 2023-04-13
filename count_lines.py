import os

path = "C:/Users/trist/OneDrive/Documents/Programs VS/Python/Flappy-gen - Experimental"

def get_lines(path: str) -> int:
    if os.path.isfile(path): 
        if path[-3:] == ".py":
            return len(open(path, "r", encoding="latin1").readlines())
        return 0
    res = 0
    for e in os.listdir(path):
        if (e == "__pycache__") or (e == ".git") or (e == ".vs") or (e == ".mypy_cache"):
            continue
        res += get_lines(path + "/" + e)
    return res

if __name__ == "__main__":
    print(get_lines(path))
