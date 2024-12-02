class LAIKA:
    def __init__(self, directory: str, caesar_key: int) -> None:
        self.directory = directory
        self.caesar_key = caesar_key

    def caesar_cipher(self, text: str) -> str:
        result = []
        for char in text:
            if char.isalpha():
                base = ord("A") if char.isupper() else ord("a")
                result.append(chr((ord(char) - base + self.caesar_key) % 26 + base))
            elif char.isdigit():
                result.append(
                    chr((ord(char) - ord("0") + self.caesar_key) % 10 + ord("0"))
                )
            else:
                result.append(char)
        return "".join(result)

    def encode(self, text: str, n: int) -> list[str]:

        result = [text[i] for i in range(0, len(text), 2)]

        if len(text) % 2 == 0:
            result += [text[i] for i in range(len(text) - 1, 0, -2)]
        else:
            result += [text[i] for i in range(len(text) - 2, 0, -2)]

        result = "".join(result)

        encoded = [result[i : i + n] for i in range(0, len(result), n)]

        return encoded

    def decode(self, chunks: list[str]) -> str:
        text = "".join(chunks)
        result = []

        left = 0
        right = len(text) - 1

        while left <= right:
            if left == right:
                result.append(text[left])
            else:
                result.append(text[left])
                result.append(text[right])
            left += 1
            right -= 1

        return "".join(result)

    def encode_to_files(self, text: str, n: int) -> str:
        chunks = self.encode(text, n)
        file_names = []

        for chunk in chunks:
            file_name = self.caesar_cipher(chunk)
            if file_name in file_names or os.path.exists(
                os.path.join(self.directory, file_name)
            ):
                raise FileExistsError("File already exists: " + file_name)
            file_names.append(file_name)

        for i, chunk in enumerate(chunks):
            file_path = os.path.join(self.directory, file_names[i])
            with open(file_path, "w") as f:
                next_file = file_names[i + 1] if i + 1 < len(file_names) else ""
                f.write(f"{next_file}\n")
                f.write(f"{chunk}")

        return file_names[0]

    def decode_from_files(self, start_file: str) -> str:

        current_file = start_file
        chunks = []
        while current_file:
            file_path = os.path.join(self.directory, current_file)
            if not os.path.exists(file_path):
                raise FileNotFoundError("File not found: " + current_file)

            with open(file_path, "r") as f:
                current_file = f.readline().strip()
                chunks.append(f.readline().strip())

        return self.decode(chunks)

# Tests

# Preconditions
import os

root_dir = "task_2"
os.makedirs(root_dir)

l = LAIKA(root_dir, 3)

# encode
assert l.encode("abcdefg", 2) == ["ac", "eg", "fd", "b"]
assert l.encode("abcdefg", 3) == ["ace", "gfd", "b"]
assert l.encode("abcdefg", 5) == ["acegf", "db"]
assert l.encode("abcdefghijkl", 1) == ["a", "c", "e", "g", "i", "k", "l", "j", "h", "f", "d", "b"]
assert l.encode("abcdefghijkl", 2) == ["ac", "eg", "ik", "lj", "hf", "db"]
assert l.encode("abcdefghijkl", 3) == ["ace", "gik", "ljh", "fdb"]
assert l.encode("abcdefghijkl", 4) == ["aceg", "iklj", "hfdb"]
assert l.encode("abcdefghijkl", 4) == ["aceg", "iklj", "hfdb"]
assert l.encode("abcdefghijkl", 12) == ["acegikljhfdb"]
assert l.encode("abcdefghijkl", 24) == ["acegikljhfdb"]

assert l.decode(["ac", "eg", "fd", "b"]) == "abcdefg"
assert l.decode(l.encode("abcdefg", 3)) == "abcdefg"
assert l.decode(l.encode("abcdefg", 5)) == "abcdefg"
assert l.decode(l.encode("abcdefghijkl", 1)) == "abcdefghijkl"
assert l.decode(l.encode("abcdefghijkl", 2)) == "abcdefghijkl"
assert l.decode(l.encode("abcdefghijkl", 3)) == "abcdefghijkl"
assert l.decode(l.encode("abcdefghijkl", 4)) == "abcdefghijkl"
assert l.decode(l.encode("abcdefghijkl", 4)) == "abcdefghijkl"
assert l.decode(l.encode("abcdefghijkl", 12)) == "abcdefghijkl"
assert l.decode(l.encode("abcdefghijkl", 24)) == "abcdefghijkl"


l1 = LAIKA(root_dir, 4)
assert l1.encode_to_files("abcdefghijkl", 3) == "egi"

assert sorted(os.listdir(root_dir)) == ["egi", "jhf", "kmo", "pnl"]

with open(os.path.join(root_dir, "egi")) as fp:
    next_file = fp.readline().strip()
    content = fp.readline().strip()

assert next_file == "kmo"
assert content == "ace"

with open(os.path.join(root_dir, "jhf")) as fp:
    next_file = fp.readline().strip()
    content = fp.readline().strip()

assert next_file == ""
assert content == "fdb"

with open(os.path.join(root_dir, "kmo")) as fp:
    next_file = fp.readline().strip()
    content = fp.readline().strip()

assert next_file == "pnl"
assert content == "gik"

with open(os.path.join(root_dir, "pnl")) as fp:
    next_file = fp.readline().strip()
    content = fp.readline().strip()

assert next_file == "jhf"
assert content == "ljh"
assert l1.decode_from_files("egi") == "abcdefghijkl"


try:
    l1.encode_to_files("abcdefghijkl", 3)
except FileExistsError:
    assert True
except Exception:
    assert False


try:
    l1.decode_from_files("non-existing-file")
except FileNotFoundError:
    assert True
except Exception:
    assert False

print("✅ All OK! +2 points")