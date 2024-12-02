import os

class InvalidLineError(Exception):
    def __init__(self, line: str):
        self.line = line
        super().__init__(f"Invalid line: {line}. Expected format: '- item:quantity:price'")

class InvalidItemError(Exception):
    def __init__(self, item: str):
        self.item = item
        super().__init__(f"Invalid item: {item}")

class InvalidQuantityError(Exception):
    def __init__(self, quantity: str, item: str):
        self.quantity = quantity
        self.item = item
        super().__init__(f"Invalid quantity '{quantity}' for item '{item}'")

class InvalidPriceError(Exception):
    def __init__(self, price: str, item: str):
        self.price = price
        self.item = item
        super().__init__(f"Invalid price '{price}' for item '{item}'")

class ListFileError(Exception):
    def __init__(self, path: str):
        self.path = path
        super().__init__(f"Cannot process file: {path}")

def validate_list(file_path: str) -> float:
    if not os.path.exists(file_path):
        raise ListFileError(file_path)

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = [line.strip() for line in file.readlines()]
    except Exception:
        raise ListFileError(file_path)

    total_sum = 0

    for line in lines:
        if line[0] != "-":
            raise InvalidLineError(line)

        parts = line[1:].split(":")

        if len(parts) != 3:
            raise InvalidLineError(line)

        item, quantity_str, price_str = parts

        if len(item) == 0 or item.isdigit():
            raise InvalidItemError(item)

        try: 
            quantity = int(quantity_str)
            if quantity < 0: 
                raise InvalidQuantityError(quantity, item) 
        except ValueError:
            raise InvalidQuantityError(quantity_str, item)

        try: 
            price = float(price_str) 
            if price < 0: 
                raise InvalidPriceError(price, item) 
        except ValueError:
            raise InvalidPriceError(price_str, item)
        
        total_sum += (int(quantity) * float(price))

    return total_sum


assert abs(validate_list(os.path.join("task_1", "list1.txt")) - 11.25) < 0.001

assert int(validate_list(os.path.join("task_1", "list2.txt"))) == 0, "Empty files should return 0"

try:
    validate_list(os.path.join("task_1", "list3.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidLineError:
    pass

try:
    validate_list(os.path.join("task_1", "list4.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidLineError:
    pass

try:
    validate_list(os.path.join("task_1", "list5.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidItemError:
    pass

try:
    validate_list(os.path.join("task_1", "list6.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidQuantityError:
    pass

try:
    validate_list(os.path.join("task_1", "list7.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidQuantityError:
    pass

try:
    validate_list(os.path.join("task_1", "list8.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidQuantityError:
    pass

try:
    validate_list(os.path.join("task_1", "list9.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidPriceError:
    pass

try:
    validate_list(os.path.join("task_1", "list10.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidPriceError:
    pass

try:
    validate_list(os.path.join("task_1", "list11.txt"))
    assert False, "Should raise InvalidLineError"
except InvalidLineError:
    pass

print("✅ All OK! +1 point")