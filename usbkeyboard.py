import argparse
import sys
import tkinter as tk

NOTHING = '[NOTHING]'

KEY_CODES = {
    0x04: ["a", "A"],
    0x05: ["b", "B"],
    0x06: ["c", "C"],
    0x07: ["d", "D"],
    0x08: ["e", "E"],
    0x09: ["f", "F"],
    0x0A: ["g", "G"],
    0x0B: ["h", "H"],
    0x0C: ["i", "I"],
    0x0D: ["j", "J"],
    0x0E: ["k", "K"],
    0x0F: ["l", "L"],
    0x10: ["m", "M"],
    0x11: ["n", "N"],
    0x12: ["o", "O"],
    0x13: ["p", "P"],
    0x14: ["q", "Q"],
    0x15: ["r", "R"],
    0x16: ["s", "S"],
    0x17: ["t", "T"],
    0x18: ["u", "U"],
    0x19: ["v", "V"],
    0x1A: ["w", "W"],
    0x1B: ["x", "X"],
    0x1C: ["y", "Y"],
    0x1D: ["z", "Z"],
    0x1E: ["1", "!"],
    0x1F: ["2", "@"],
    0x20: ["3", "#"],
    0x21: ["4", "$"],
    0x22: ["5", "%"],
    0x23: ["6", "^"],
    0x24: ["7", "&"],
    0x25: ["8", "*"],
    0x26: ["9", "("],
    0x27: ["0", ")"],
    0x28: ["\n", "\n"],
    0x29: ["[ESC]", "[ESC]"],
    0x2A: ["[BACKSPACE]", "[BACKSPACE]"],
    0x2C: [" ", " "],
    0x2D: ["-", "_"],
    0x2E: ["=", "+"],
    0x2F: ["[", "{"],
    0x30: ["]", "}"],
    0x32: ["#", "~"],
    0x33: [";", ":"],
    0x34: ["'", '"'],
    0x36: [",", "<"],
    0x37: [".", ">"],
    0x38: ["/", "?"],
    0x39: ["[CAPSLOCK]", "[CAPSLOCK]"],
    0x2B: ["\t", "\t"],
    0x4F: ["→", "→"],
    0x50: ["←", "←"],
    0x51: ["↓", "↓"],
    0x52: ["↑", "↑"],
}

def parse_keyboard(file : str) -> list[str]:
    '''
    ### Function arguments:
    - file:  path to file to read

    ### Function returns:
    - list of strings rappresenting the history of the keyboard (in the form of key pressed)
    '''
    with open(file, "r") as f:
        datas = f.read().split("\n")
    datas = [d.strip() for d in datas if d]

    history = []
    skip_next = False
    history.append('Cursor')
    for data in datas:
        shift = int(data.split(":")[0], 16)  # 0x2 is left shift 0x20 is right shift
        key = int(data.split(":")[2], 16)

        if skip_next:
            skip_next = False
            continue

        if key == 0 or int(data.split(":")[3], 16) > 0:
            continue

        if shift != 0:
            shift = 1
            skip_next = True

        history.append(KEY_CODES[key][shift])
    
    return history





class MyWindow:
    def __init__(self, win : tk.Tk, data : list[str], instruction_number : int =0):
        """
        ### Function parameters:
        - win: tkinter window
        - data: list of keys pressed
        - instruction_number: index of the key pressed

        ### Function description:
        Constructor of the class MyWindow, generates a tkinter window with a 3x2 grid layout, it includes:
        - two labels, one for the instruction number and one for the key pressed
        - a text box, to display text composed and where the user can modify it
        - a slider, to navigate through the instructions
        - two buttons, one to go to the next instruction and one to go to the previous instruction
        """
        #window config
        win.geometry("500x300")
        win.title("Keyboard")
        win.grid_rowconfigure((0,2), weight=0)
        win.grid_rowconfigure(1, weight=1)
        win.grid_columnconfigure((0,1), weight=1)

        self.instruction_number = instruction_number
        self.data = data
        self.CAPSLOCK = False
        self.stack = []

        #first row: labels
        self.i_number = tk.Label(win, text=f'Number:   {self.instruction_number}')
        self.i_number.grid(row=0, column=0)

        self.key = tk.Label(win, text=f'Key:  {self.data[self.instruction_number]}')
        self.key.grid(row=0, column=1)
        
        #second row: textbox
        self.textbox = tk.Text(win,undo=True,autoseparators=True)
        self.textbox.grid(row=1, column=0, columnspan=2, padx=20, pady=(20, 0), sticky="nsew")
        self.stack.append('')

        #third row: slider
        self.slider = tk.Scale(win, from_=0, to=len(self.data)-1, orient=tk.HORIZONTAL, command=self.slider_callback)
        self.slider.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")

        #fourth row: buttons
        self.prev = tk.Button(win, text="Previous", command=self.press_prev)
        self.prev.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

        self.next = tk.Button(win, text="Next", command=self.press_next)
        self.next.grid(row=3, column=1, padx=20, pady=20, sticky="ew")
    


    def press_prev(self) -> None:
        """
        ### Function description:
        Function called when the user presses the previous button, it updates the instruction number and the key pressed labels and the slider
        then it updates the textbox restoring the previous text saved in the stack
        """      
        if self.instruction_number == 0:
            return
        
        self.instruction_number -= 1
        self.i_number.configure(text=f'Number:   {self.instruction_number}')
        if(self.data[self.instruction_number] == ' '):
                self.key.configure(text=f'Key:  [SPACE]')
        else:
            self.key.configure(text=f'Key:  {self.data[self.instruction_number]}')  
        self.slider.set(self.instruction_number)
        
        if not self.stack:
            self.stack.append('')
        elif(NOTHING == self.stack[-1]):
            self.stack.pop()
        elif(self.textbox.get("1.0", "end-1c") == self.stack[-1]):
            self.stack.pop()
        
        self.textbox.delete("1.0", "end-1c")
        self.textbox.insert(1.0, self.stack.pop())


    def press_next(self) -> None:
        """"
        ### Function description:
        Function called when the user presses the next button, it updates the instruction number and the key pressed labels and the slider
        then it updates the textbox saving the current text in the stack and adding the new key pressed considering the CAPSLOCK status
        and all the special keys (backspace, enter, tab, capslock, space)        
        """
        do_push = True
        if(self.instruction_number > len(self.data)):
            return

        self.instruction_number += 1
        #LABELS
        self.i_number.configure(text=f'Number:   {self.instruction_number}')
        if(self.data[self.instruction_number] == ' '):
            self.key.configure(text=f'Key:  [SPACE]')
        else:
            self.key.configure(text=f'Key:  {self.data[self.instruction_number]}')   

        #SLIDER 
        self.slider.set(self.instruction_number)

        #TEXTBOX
        if(self.data[self.instruction_number] == '[BACKSPACE]'):
            #delete last char before cursor
            self.textbox.delete("insert-1c")

        elif(self.data[self.instruction_number] == '[CAPSLOCK]'):
            #set or unset capslock
            self.CAPSLOCK = not self.CAPSLOCK
            do_push = False

        elif(self.data[self.instruction_number] == '←'):
            #move cursor left
            self.textbox.mark_set("insert", "insert-1c")
            do_push = False
        
        elif(self.data[self.instruction_number] == '→'):
            #move cursor right
            self.textbox.mark_set("insert", "insert+1c")
            do_push = False

            
        elif(self.data[self.instruction_number] == '↑'):
            #move cursor up
            self.textbox.mark_set("insert", "insert-1l")
            do_push = False


        elif(self.data[self.instruction_number] == '↓'):
            #move cursor to the end of the line
            self.textbox.mark_set("insert", "end")
            do_push = False

        elif(self.CAPSLOCK):
            self.textbox.insert("insert", self.data[self.instruction_number].upper())
        else:
            self.textbox.insert("insert", self.data[self.instruction_number])
        
        self.textbox.focus_set()
        if(do_push):
            self.stack.append(self.textbox.get("1.0", "end-1c"))
        else:
            self.stack.append(f'{NOTHING}')

    def slider_callback(self, value):
        """
        ### Function description:
        Function called when the user moves the slider, it uses press_next and press_prev function
        """
        while(self.instruction_number != int(value)):
            if(self.instruction_number < int(value)):
                self.press_next()
            else:
                self.press_prev()


def main():
    #parsing command line arguments
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', type=str, help='path of the file to open')
    parser.add_argument('-o', '--output', type=str, help='path of the output file for the keys log')
    args = parser.parse_args()


    if(args.file == None):
        print("Error: file path not specified")
        exit(1)
    
    history = parse_keyboard(args.file)

    if(args.output != None):
        with open(args.output, 'w') as f:
            for i in range(0,len(history)):
                f.write(f'{i} {history[i]}\n')
    
    #GUI
    window=tk.Tk()
    MyWindow(window,history)
    window.mainloop()

if __name__ == "__main__":
    main()