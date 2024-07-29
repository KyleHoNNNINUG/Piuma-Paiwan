# In data passing, 
# Stress patterns are represented as an array of character-free syllables, represented as [foot_position, stressed] where
#   foot_position signifies the syllable's position in a foot: 
#       0 for leftmost child, 1 for rightmost child, 2 for both, -1 if not in a foot
#   stressed signifies whether the syllable is stressed: 
#       1 for primary stress, 0 for not stressed, -1 for secondary stress
# Penalties of specific types are represented as an array of violations, represented as a boolean:
#   True for a violation at the position, False for no violation
# Directions of evaluation are represented as a boolean:
#   True for leftward, False for rightward, *None if no direction (word violations)

# Class for identifying character properties (helper class of Syllable_Processor)
class Character:
    vowels = ['a', 'ɑ', 'æ', 'ɐ', 'ɑ̃',
            'e', 'ə', 'ɚ', 'ɵ', 
            'ɛ', 'ɜ', 'ɝ', 'ɛ̃',
            'i', 'ɪ', 'ɨ', 'ɪ̈',
            'o', 'ɔ', 'œ', 'ɒ', 'ɔ̃',
            'ø',
            'u', 'ʊ', 'ʉ']
    consonants = [['b', 'β', 'ɓ',
                'c', 'ç', 'ɕ',
                'd', 'ð', 'ɗ', 'ɖ',
                'f', 
                'g', 'ɠ', 'ɢ',
                'h', 'ħ', 'ɦ', 'ɥ', 'ɧ', 'ʜ',
                'j', 'ʝ', 'ɟ',
                'k', 
                'l', 'ɫ', 'ɭ', 'ɬ', 'ʟ', 'ɮ',
                'm', 'ɱ',
                'n', 'ŋ', 'ɲ', 'ɳ', 'ɴ',
                'p', 'ɸ',
                'q', 
                'r', 'ɾ', 'ɹ', 'ʁ', 'ʀ', 'ɻ', 'ɽ',
                's', 'ʃ', 'ʂ',
                't', 'θ', 'ʈ',
                'v', 'ʌ', 'ʋ',
                'w', 'ɯ', 'ʍ',
                'x', 'χ',
                'y', 'ɣ', 'ʎ', 'ʏ', 'ɤ',
                'z', 'ʒ', 'ʐ', 'ʑ'],
                ['d͡ʒ',  
                't͡ʃ', 't͡s', 
                'tʃh']]
    # Returns True if a is a vowel, False otherwise
    def is_vowel(a):
        return a in Character.vowels
    # Returns True if b is a consonant, False otherwise
    def is_consonant(b):
        return b in Character.consonants[0]
    # Returns True if bcd is a bound consonant, False otherwise
    def is_bound_consonant(bcd):
        return bcd in Character.consonants[1]
# Class for translating and printing words in syllables of different formats
class Syllable_Processor:
    # Turns a word string into separate syllables
    def to_syllables(string):
        syllables = []
        syllable_indices = []
        for i in range(len(string)):
            if Character.is_vowel(string[i]):
                if i == 0 or (i >= 1 and Character.is_consonant(string[i-1])) or (i >= 3 and Character.is_bound_consonant(string[i-3:i])):
                    syllables += string[i]
                    syllable_indices += [i]
                else:
                    syllables[len(syllables)-1] += string[i]
        for i in range(len(syllable_indices)):
            index = syllable_indices[i]
            if index >= 3 and Character.is_bound_consonant(string[index-3:index]):
                syllables[i] = string[index-3:index+1]
            elif index >= 1 and Character.is_consonant(string[index-1]):
                syllables[i] = string[index-1:index+1]
            if index + 3 < len(string) and Character.is_bound_consonant(string[index+1:index+4]):
                if not (index + 4 in syllable_indices) or index + 4 >= len(string):
                    syllables[i] = syllables[i] + string[index+1:index+4]
            elif index + 1 < len(string) and Character.is_consonant(string[index+1]):
                if not (index + 2 in syllable_indices) or index + 2 >= len(string):
                    syllables[i] = syllables[i] + string[index+1]
        return syllables
    # Prints a given stress pattern with 'Li' denoting the i-th syllable
    def print_stress_pattern(stress_pattern):
        proxy = ['L' + str(i + 1) for i in range(len(stress_pattern))]
        Syllable_Processor.print_syllables_stressed(proxy, stress_pattern)
    # Prints a word in a given stress pattern
    def print_syllables_stressed(syllables, stress_pattern):
        for i in range(len(syllables)):
            syllable = syllables[i]
            if stress_pattern[i][1] == 1:
                syllable = "ˈ" + syllable
            elif stress_pattern[i][1] == -1:
                syllable = "ˌ" + syllable
            match stress_pattern[i][0]:
                case -1:
                    print(syllable, end="")
                case 0: 
                    print("(", syllable, sep="", end="")
                case 1:
                    print(syllable, ")", sep="", end="")
                case 2:
                    print("(", syllable, ")", sep="", end="")
        print()

# Class for calculating the optimal stress pattern for a given number of syllables
class Stress:
    # Constructor
    def __init__(self, number_of_syllables):
        self.pattern = [[None,None] for i in range(number_of_syllables)]
        self.finalize_mark = [[False,False] for i in range(number_of_syllables)]
        self.violation_rank = []
        self.word_violation = []
    # Adds a violation type with direction
    def add(self, violation):
        self.violation_rank += [violation]
        word_violation_dict = ["HD(w)"]
        if violation[0] in word_violation_dict:
            self.word_violation += [violation[0]]
    # Modify a single part of stress pattern if the part is not finalized yet
    def assign(self, index, pos, assign_value, finalize_current_change):
        if not self.finalize_mark[index][pos]:
            self.pattern[index][pos] = assign_value
            if finalize_current_change:
                self.finalize_mark[index][pos] = True
    # Removes redundant violations
    def clean(self):
        deleted = []
        # Trochee and Iamb, regardless of directions, determines the stress and foot structures for the entire word
        # Thus, they are considered as in the same type and redundant after one is already considered
        to_ban_after = ["Trochee", "Iamb"]
        start_ban = False
        for i in range(len(self.violation_rank)):
            if self.violation_rank[i] != None and (self.violation_rank[i][0] in to_ban_after):
                if start_ban:
                    deleted += [self.violation_rank[i]]
                    self.violation_rank[i] = None
                    break
                else:
                    start_ban = True
        # When ranked lower than Trochee or Iamb or another Parse, Parse has no effect on the optimal structure
        to_ban_after = ["Trochee", "Iamb"]
        start_ban = False
        has_parse = False
        for i in range(len(self.violation_rank)):
            if self.violation_rank[i] != None:
                if self.violation_rank[i][0] == "Parse":
                    if start_ban:
                        deleted += [self.violation_rank[i]]
                        self.violation_rank[i] = None
                    elif has_parse:
                        deleted += [self.violation_rank[i]]
                        self.violation_rank[i] = None
                    else:
                        has_parse = True
                elif self.violation_rank[i][0] in to_ban_after and not start_ban:
                    start_ban = True
        # When ranked lower than Trochee or Iamb or Parse, word violations has no effect on the optimal structure
        to_ban_after = ["Trochee", "Iamb", "Parse"]
        start_ban = False
        for i in range(len(self.violation_rank)):
            if self.violation_rank[i] != None:
                if start_ban and self.violation_rank[i][0] in self.word_violation:
                    deleted += [self.violation_rank[i]]
                    self.word_violation.remove(self.violation_rank[i][0])
                    self.violation_rank[i] = None
                elif self.violation_rank[i][0] in to_ban_after and not start_ban:
                    start_ban = True
        while None in self.violation_rank:
            self.violation_rank.remove(None)
        return deleted
    # Returns True if the entire stress pattern is finalized, False otherwise
    def finalized(self):
        try:
            for syllable in self.finalize_mark:
                assert(syllable[0])
                assert(syllable[1])
            return True
        except:
            return False
    # Assigns and finalizes stresses with only one possibility
    def in_between(self):
        for i in range(len(self.pattern)):
            if self.pattern[i][0] == None or self.finalize_mark[i][1]:
                continue
            match self.pattern[i][0]:
                case 2:
                    self.assign(i,1,assign_value=1,finalize_current_change=True)
                case -1:
                    self.assign(i,1,assign_value=0,finalize_current_change=True)
                case 0:
                    if self.finalize_mark[i+1][1]:
                        if self.pattern[i+1][1] == 0:
                            self.assign(i,1,assign_value=1,finalize_current_change=True)
                        else:
                            self.assign(i,1,assign_value=0,finalize_current_change=True)
                case 1:
                    if self.finalize_mark[i+1][1]:
                        if self.pattern[i+1][1] == 0:
                            self.assign(i,1,assign_value=1,finalize_current_change=True)
                        else:
                            self.assign(i,1,assign_value=0,finalize_current_change=True)
    # Modify the stress pattern to minimize the current type of violations
    def mod(self, violation):
        match violation[0]:
            case "Iamb":
                if "HD(w)" in self.word_violation:
                    has_foot = False
                    for i in range(len(self.pattern)):
                        if self.finalize_mark[i][0] and self.pattern[i][0] != -1:
                            has_foot = True
                            break
                    if not has_foot:
                        if len(self.pattern) == 1:
                            self.assign(0,0,assign_value=2,finalize_current_change=True)
                        else:
                            if violation[1]:
                                self.assign(0,0,assign_value=0,finalize_current_change=True)
                                self.assign(1,0,assign_value=1,finalize_current_change=True)
                            else:
                                self.assign(-2,0,assign_value=0,finalize_current_change=True)
                                self.assign(-1,0,assign_value=1,finalize_current_change=True)
                for i in range(len(self.pattern)):
                    if self.finalize_mark[i][0] and not self.finalize_mark[i][1]:
                        if self.pattern[i][0] == 0:
                            self.assign(i,1,assign_value=0,finalize_current_change=True)
                        elif self.pattern[i][0] == 1:
                            self.assign(i,1,assign_value=1,finalize_current_change=True)
            case "Trochee":
                if "HD(w)" in self.word_violation:
                    has_foot = False
                    for i in range(len(self.pattern)):
                        if self.finalize_mark[i][0] and self.pattern[i][0] != -1:
                            has_foot = True
                            break
                    if not has_foot:
                        if len(self.pattern) == 1:
                            self.assign(0,0,assign_value=2,finalize_current_change=True)
                        else:
                            if violation[1]:
                                self.assign(0,0,assign_value=0,finalize_current_change=True)
                                self.assign(1,0,assign_value=1,finalize_current_change=True)
                            else:
                                self.assign(-2,0,assign_value=0,finalize_current_change=True)
                                self.assign(-1,0,assign_value=1,finalize_current_change=True)
                for i in range(len(self.pattern)):
                    if self.finalize_mark[i][0] and not self.finalize_mark[i][1]:
                        if self.pattern[i][0] == 0:
                            self.assign(i,1,assign_value=1,finalize_current_change=True)
                        elif self.pattern[i][0] == 1:
                            self.assign(i,1,assign_value=0,finalize_current_change=True)
            case "Parse":
                if len(self.pattern) % 2 == 0:
                    for i in range(len(self.pattern)):
                        self.assign(i,0,assign_value=(i%2),finalize_current_change=True)
                else:
                    if violation[1]:
                        if not (self.finalize_mark[0][1] and not self.pattern[0][1]):
                            self.assign(0,0,assign_value=2,finalize_current_change=True)
                        else:
                            self.assign(0,0,assign_value=-1,finalize_current_change=True)
                        for i in range(1,len(self.pattern)):
                            self.assign(i,0,assign_value=((i-1)%2),finalize_current_change=True)
                    else:
                        if not (self.finalize_mark[-1][1] and not self.pattern[-1][1]):
                            self.assign(-1,0,assign_value=2,finalize_current_change=True)
                        else:
                            self.assign(-1,0,assign_value=-1,finalize_current_change=True)
                        self.finalize_mark[-1][0] = True
                        for i in range(len(self.pattern)-1):
                            self.assign(i,0,assign_value=(i%2),finalize_current_change=True)
            case "NonFin":
                if not ("HD(w)" in self.word_violation and len(self.pattern) <= 1):
                    if violation[1]:
                        self.assign(0,1,assign_value=False,finalize_current_change=True)
                    else:
                        self.assign(-1,1,assign_value=False,finalize_current_change=True)
            case "HD(w)":
                pass
            case _:
                print("Violation type", str(violation[0]), "undefined", sep=" ")
    # Modify the stress pattern to minimize each violation as in the order added
    def op(self, print_process=False, print_message=False):
        deleted = self.clean()
        for violation in self.violation_rank:
            self.mod(violation)
            self.in_between()
            if print_process:
                self.print_sp()
            if self.finalized():
                break
        if print_message:
            self.print_v(deleted)
        if not self.finalized():
            # if print_message:
            #     print("Stress pattern not finalized yet")
            for i in range(len(self.finalize_mark)):
                self.assign(i,0,assign_value=-1,finalize_current_change=True)
                self.assign(i,1,assign_value=False,finalize_current_change=True)
            # if print_message:
            #     print("Finalized remaining parts")
            if print_process:
                self.print_sp()
    # Prints the current stress pattern with marks of whether the information is finalized (F/N)
    # fp denotes the foot position (0/1/2/-1), s denotes whether the syllable is stressed (Y/N)
    def print_sp(self):
        def translate(index, pos):
            if self.pattern[index][pos] == None:
                body = ""
            else:
                if type(self.pattern[index][pos]) == int:
                    if self.pattern[index][pos] != 0:
                        body = "Y "
                    else:
                        body = "N "
                else:
                    body = str(self.pattern[index][pos]) + " "
            if self.finalize_mark[index][pos]:
                whether_finalized = "(F)"
            else:
                whether_finalized = "(N)"
            return body + whether_finalized
        for i in range(len(self.pattern)):
            print("[fp: ", translate(i, 0), ", s: ", translate(i, 1), "]", sep="", end="\t")
        print()
    # Prints the final stress pattern
    def print_sp_final(self):
        if not self.finalized():
            print("Stress pattern not finalized yet")
            return
        Syllable_Processor.print_stress_pattern(self.pattern)
    # Prints the current violations to consider
    def print_v(self, deleted=None):
        print("Syllable violation(s): ", end="")
        for i in range(len(self.violation_rank)):
            if not self.violation_rank[i][0] in self.word_violation:
                if self.violation_rank[i][1]:
                    dir_string = "(leftward)"
                else:
                    dir_string = "(rightward)"
                print(str(self.violation_rank[i][0]) + dir_string, end="")
                if i < len(self.violation_rank) - 1:
                    print(", ", end="")
        print()
        print("Word violation(s): ", end="")
        for i in range(len(self.word_violation)):
            print(str(self.word_violation[i]), end="")
            if i < len(self.word_violation) - 1:
                print(", ", end="")
        print()
        if deleted != None:
            print("Deleted (redundant) violation(s): ", end="")
            for i in range(len(deleted)):
                if deleted[i][1]:
                    dir_string = "(leftward)"
                else:
                    dir_string = "(rightward)"
                print(str(deleted[i][0]) + dir_string, end="")
                if i < len(deleted) - 1:
                    print(", ", end="")
            print()

class Test:
    # Constructor
    def __init__(self, word):
        self.word = word
        self.word_in_syllables = Syllable_Processor.to_syllables(word)
        self.stress = Stress(len(self.word_in_syllables))
    # Sets stress to the optimal stress pattern with the given violations
    def gen(self, print_process=False, print_message=False):
        self.stress.op(print_process=print_process, print_message=print_message)
    # Prints the optimal stress pattern, after Test.gen is executed
    def print_sp(self, final=True):
        if final:
            self.stress.print_sp_final()
        else:
            self.stress.print_sp()
    # Prints the word with the optimal stress applied, after Test.gen is executed
    def print_word(self):
        Syllable_Processor.print_syllables_stressed(self.word_in_syllables, self.stress.pattern)
    # Takes input strings as violations and adds to the violation list to consider, until the signal "end"
    def take_in(self):
        print("Enter violation rules in the format of \"name, direction(L/R)\"")
        print("End the input with \"end\"")
        while True:
            string = input()
            if string == "end":
                break
            try:
                self.stress.add(Test.translate(string))
            except:
                print("Input not accepted")
    # Translates a violation string in the format of "violation_name, direction"
    # to a violation in the format of ["violation_name", direction]
    def translate(string):
        temp = string.split(", ")
        if temp[1] == "L":
            temp[1] = True
        elif temp[1] == "R":
            temp[1] = False
        else:
            print("Unaccepted direction")
            assert(False)
        return temp


t = Test(input("Enter the word to parse: "))
t.take_in()
t.gen(print_message=True)
print("Final stress pattern: ", end="")
t.print_sp()
print("Parsed word: ", end="")
t.print_word()