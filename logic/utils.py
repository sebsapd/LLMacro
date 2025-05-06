scancodes_tab = {
        1: "Escape",
        2: "1",
        3: "2",
        4: "3",
        5: "4",
        6: "5",
        7: "6",
        8: "7",
        9: "8",
        10: "9",
        11: "0",
        12: "-",
        13: "=",
        14: "Backspace",
        15: "Tab",
        16: "Q",
        17: "W",
        18: "E",
        19: "R",
        20: "T",
        21: "Y",
        22: "U",
        23: "I",
        24: "O",
        25: "P",
        26: "[",
        27: "]",
        28: "Enter",
        29: "L Ctrl",
        30: "A",
        31: "S",
        32: "D",
        33: "F",
        34: "G",
        35: "H",
        36: "J",
        37: "K",
        38: "L",
        39: ";",
        40: "'",
        41: "~",
        42: "L Shift",
        43: "Back Slash",
        44: "Z",
        45: "X",
        46: "C",
        47: "V",
        48: "B",
        49: "N",
        50: "M",
        51: ",",
        52: ".",
        53: "/",
        54: "R Shift",
        55: "Num *",
        56: "V",
        57: "Spacebar",
        58: "Caps Lock",
        59: "F1",
        60: "F2",
        61: "F3",
        62: "F4",
        63: "F5",
        64: "F6",
        65: "F7",
        66: "F8",
        67: "F9",
        68: "F10",
        69: "Num Lock",
        70: "Scroll Lock",
        71: "Num 7",
        72: "Num 8",
        73: "Num 9",
        74: "Num -",
        75: "Num 4",
        76: "Num 5",
        77: "Num 6",
        78: "Num +",
        79: "Num 1",
        80: "Num 2",
        81: "Num 3",
        82: "Num 0",
        83: "Num .",
        87: "F11",
        88: "F12",
        156: "Num Enter",
        157: "R Ctrl",
        181: "Num /",
        184: "R Alt",
        199: "Home",
        200: "Up Arrow",
        201: "Page Up",
        203: "Left Arrow",
        205: "Right Arrow",
        207: "End",
        208: "Down Arrow",
        209: "Page Down",
        210: "Insert",
        211: "Delete",
        256: "LMB",
        257: "RMB",
        258: "MMB",
        259: "MB3",
        260: "MB4",
        261: "MB5",
        262: "MB6",
        263: "MB7",
        264: "WheelUp",
        265: "WheelDown"
        }

# retrieves the key name from the scancode
def get_key_name(scancode):
        return scancodes_tab.get(scancode, "Unknown key")

# retrieves the scancode from the key name
def get_scancode(key_name):
    key_name_to_scancode = {v: k for k, v in scancodes_tab.items()}
    return key_name_to_scancode.get(key_name, None) 

# checks if the array is empty
def is_loop_fully_empty(loop_event):
    if loop_event["func"] != "loop_event":
        return False

    for event in loop_event.get("events", []):
        if event["func"] == "loop_event":
            if not is_loop_fully_empty(event):
                return False
        else:
            return False
    return True

# calculating the total execution time of one macro iteration
def total_time_counting(total_time, item_time, current_loop_id, loop_repeats):
    if item_time != None and item_time != "":
        if current_loop_id == None or loop_repeats == "1":
            total_time += float(item_time.replace(',', '.'))

        else:
            if loop_repeats != None:
                total_time += float(item_time.replace(',', '.')) * float(loop_repeats)

    return total_time
