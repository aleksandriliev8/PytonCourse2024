INVALID_FORMAT_MSG = "Невалиден формат"
INVALID_LETTERS_MSG = "Невалидни букви"
INVALID_CODE_MSG = "Невалиден регионален код"

ALLOWED_LETTERS = set("АВЕКМНОРСТУХ")

REGION_CODES = {
    "Е": "Благоевград",
    "А": "Бургас",
    "В": "Варна",
    "ВТ": "Велико Търново",
    "ВН": "Видин",
    "ВР": "Враца",
    "ЕВ": "Габрово",
    "ТХ": "Добрич",
    "К": "Кърджали",
    "КН": "Кюстендил",
    "ОВ": "Ловеч",
    "М": "Монтана",
    "РА": "Пазарджик",
    "РК": "Перник",
    "ЕН": "Плевен",
    "РВ": "Пловдив",
    "РР": "Разград",
    "Р": "Русе",
    "СС": "Силистра",
    "СН": "Сливен",
    "СМ": "Смолян",
    "СО": "София (област)",
    "С": "София (столица)",
    "СА": "София (столица)",
    "СВ": "София (столица)",
    "СТ": "Стара Загора",
    "Т": "Търговище",
    "Х": "Хасково",
    "Н": "Шумен",
    "У": "Ямбол",
}

#function for counting the number of digits in a string
def digits_counter(str):
    counter = 0

    for char in str:
        if char.isdigit():
            counter += 1
        
    return counter

#function for checking if a string contains invalid letter
def found_invalid_letters(str):
    for char in str:
        if (char not in ALLOWED_LETTERS):
            return True
    return False

#main function
def is_valid(license_plate):

    #needed variables for the solution
    result = ()
    isValid = True
    license_plate = license_plate.upper()
    plate_len = len(license_plate)

    first_letters = ""

    #checking and eventually keeping aside the first one 
    # or two letters from license plate

    if license_plate[0].isalpha():
        first_letters += license_plate[0]
    if license_plate[1].isalpha():
        first_letters += license_plate[1]

    last_letters = ""

    #checking and eventually keeping aside the last two 
    # letters from license plate

    if license_plate[plate_len - 1].isalpha():
        last_letters += license_plate[plate_len - 1]
    if license_plate[plate_len - 2].isalpha():
        last_letters += license_plate[plate_len - 2]

    digits_count = digits_counter(license_plate)
    
    #checking if the format is valid
    if(len(first_letters) == 0 or len(last_letters) != 2 
       or digits_count != 4
       or len(first_letters) + len(last_letters) + digits_count != plate_len):
        isValid = False
        result = (isValid, INVALID_FORMAT_MSG)

    #checking if there are any invalid letters
    elif(found_invalid_letters(first_letters)
        or found_invalid_letters(last_letters)):
        isValid = False
        result = (isValid, INVALID_LETTERS_MSG)
    
    #checking if the first numbers from the plate refer to any region code
    elif(first_letters not in REGION_CODES):
        isValid = False
        result = (isValid, INVALID_CODE_MSG)
    
    #in any other case this means that the license plate is valid
    else:
        result = (isValid, REGION_CODES[first_letters])

    return result

assert is_valid("СА1234АВ") == (True, "София (столица)")
assert is_valid("С1234АВ") == (True, "София (столица)")
assert is_valid("ТХ0000ТХ") == (True, "Добрич")
assert is_valid("ТХ000ТХ") == (False, INVALID_FORMAT_MSG)
assert is_valid("ТХ0000Т") == (False, INVALID_FORMAT_MSG)
assert is_valid("ТХ0000ТХХ") == (False, INVALID_FORMAT_MSG)
assert is_valid("У8888СТ") == (True, "Ямбол")
assert is_valid("Y8888CT") == (False, INVALID_LETTERS_MSG)
assert is_valid("ПЛ7777АА") == (False, INVALID_LETTERS_MSG)
assert is_valid("РВ7777БВ") == (False, INVALID_LETTERS_MSG)
assert is_valid("ВВ6666КН") == (False, INVALID_CODE_MSG)