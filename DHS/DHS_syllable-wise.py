import time
# Class for identifying character properties (helper class of Syllable)
class Character:
    vowels = [['a', 'ɑ', 'æ', 'ɐ', 'ɑ̃',
            'e', 'ə', 'ɚ', 'ɵ', 
            'ɛ', 'ɜ', 'ɝ', 'ɛ̃',
            'i', 'ɪ', 'ɨ', 'ɪ̈',
            'o', 'ɔ', 'œ', 'ɒ', 'ɔ̃',
            'ø',
            'u', 'ʊ', 'ʉ']]
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
        return a in Character.vowels[0]
    # Returns True if b is a consonant, False otherwise
    def is_consonant(b):
        return b in Character.consonants[0]
    # Returns True if bcd is a bound consonant, False otherwise
    def is_bound_consonant(bcd):
        return bcd in Character.consonants[1]
# Class of syllable objects and for translating words into syllables
class Syllable:
    # Constructor of a single syllable
    def __init__(self, onset, nucleus, coda, index=0, mora=True, stress="unstressed", foot_position="none", weight="L"):
        self.onset = onset
        self.nucleus = nucleus
        self.coda = coda
        self.schwa = "ə" in nucleus
        self.mora = mora
        self.stress = stress # unstressed/primary/secondary
        self.foot_position = foot_position # none/left/right/whole
        self.weight = weight # L/H
        self.index = index
    # String form of the syllable for printing in singular
    def __str__(self):
        syllable = self.nucleus
        if not self.mora:
            syllable = "^" + syllable
        if self.onset != None:
            syllable = self.onset + syllable
        if self.weight == "H":
            syllable += ":"
        if self.coda != None:
            syllable += self.coda
        if self.stress == "primary":
            syllable = "ˈ" + syllable
        elif self.stress == "secondary":
            syllable = "ˌ" + syllable
        return syllable
    # Returns a copy of the syllable
    def copy(self):
        onset = self.onset
        nucleus = self.nucleus
        coda = self.coda
        mora = self.mora
        stress = self.stress
        foot_position = self.foot_position
        index = self.index
        return Syllable(onset=onset, nucleus=nucleus, coda=coda, index=index, mora=mora, stress=stress, foot_position=foot_position)
    # Returns a copy of the syllable without letter content
    def proxy(self):
        if self.schwa:
            if self.mora:
                schwa = "mora"
            else:
                schwa = "nonmora"
        else:
            schwa = "not schwa"
        stress = self.stress
        foot_position = self.foot_position
        weight = self.weight
        return ProxySyllable(schwa, stress, foot_position, weight)
    # Applies the format from a proxy syllable to the syllable
    def apply(self, proxy_syllable):
        if proxy_syllable.schwa == "nonmora":
            self.mora = False
        self.stress = proxy_syllable.stress
        self.foot_position = proxy_syllable.foot_position
        self.weight = proxy_syllable.weight
    # Turns a word string into separate syllables
    def to_syllable_array(string):
        syllables = []
        syllable_strings = []
        syllable_indices = []
        # Identifies nuclei
        for i in range(len(string)):
            if Character.is_vowel(string[i]) or string[i] == '^':
                if i == 0 or (i >= 1 and Character.is_consonant(string[i-1])) or (i >= 3 and Character.is_bound_consonant(string[i-3:i])):
                    syllable_strings += [[string[i]]]
                    syllable_indices += [i]
                else:
                    syllable_strings[-1][0] += string[i]
        # Adds onsets and codas
        for i in range(len(syllable_indices)):
            index = syllable_indices[i]
            if index >= 3 and Character.is_bound_consonant(string[index-3:index]):
                syllable_strings[i] = [string[index-3:index]] + syllable_strings[i]
            elif index >= 1 and Character.is_consonant(string[index-1]):
                syllable_strings[i] = [string[index-1:index]] + syllable_strings[i]
            if index + 3 < len(string) and Character.is_bound_consonant(string[index+1:index+4]):
                if not (index + 4 in syllable_indices) or index + 4 >= len(string):
                    syllable_strings[i] += [string[index+1:index+4]]
            elif index + 1 < len(string) and Character.is_consonant(string[index+1]):
                if not (index + 2 in syllable_indices) or index + 2 >= len(string):
                    syllable_strings[i] += [string[index+1]]
        # Creates syllable objects from strings
        for i in range(len(syllable_strings)):
            body_array_size = len(syllable_strings[i])
            match body_array_size:
                case 1:
                    syllables += [Syllable(None, syllable_strings[i][0], None, i + 1)]
                case 2:
                    if Character.is_vowel(syllable_strings[0]):
                        syllables += [Syllable(None, syllable_strings[i][0], syllable_strings[i][1], i + 1)]
                    else:
                        syllables += [Syllable(syllable_strings[i][0], syllable_strings[i][1], None, i + 1)]
                case 3:
                    syllables += [Syllable(syllable_strings[i][0], syllable_strings[i][1], syllable_strings[i][2], i + 1)]
        return syllables
    # Modifies the weight of the syllable
    def mod_weight(self, new_weight):
        self.weight = new_weight
# Class of syllable objects with simplified content for efficiency
class ProxySyllable:
    # Constructor of a single syllable without letter content
    def __init__(self, schwa, stress, foot_position, weight="L"):
        self.schwa = schwa # not schwa/mora/nonmora
        self.stress = stress # unstressed/primary/secondary
        self.foot_position = foot_position # none/left/right/whole
        self.weight = weight # L/H
    # String form of the syllable for printing in singular
    def __str__(self):
        if self.schwa == "nonmora":
            syllable = "^ə"
        elif self.schwa == "mora":
            syllable = "ə"
        else:
            syllable = "V"
        syllable = "C" + syllable
        if self.weight == "H":
            syllable += ":"
        if self.stress == "primary":
            syllable = "ˈ" + syllable
        elif self.stress == "secondary":
            syllable = "ˌ" + syllable
        return syllable
    # Returns a copy of the syllable
    def copy(self):
        return ProxySyllable(self.schwa, self.stress, self.foot_position, weight=self.weight)
    # Modifies the foot position of the syllable
    def mod_position(self, new_foot_position):
        self.foot_position = new_foot_position
    # Modifies the stress of the syllable
    def mod_stress(self, new_stress):
        self.stress = new_stress
    # Modifies the weight of the syllable
    def mod_weight(self, new_weight):
        self.weight = new_weight
# Class of violation rule objects
class Violation:
    # Constructor for a violation
    def __init__(self, name, direction, rank):
        self.name = name
        self.direction = direction
        self.rank = rank
        self.in_effect = True
# Class of stress objects for the optimal stress pattern of the given word
class Stress:
    # Constructor
    def __init__(self, syllables):
        self.syllables = syllables
        self.violations = []
        self.candidates = []
        self.not_considering = []
    # Adds a violation type with direction
    def add(self, violation_name, direction):
        violation = Violation(violation_name, direction, len(self.violations))
        self.violations += [violation]
    # Sets stresses before the last stress to secondary
    def classify_stress(syllables):
        has_primary = False
        for i in range(len(syllables)):
            index = len(syllables) - 1 - i
            if syllables[index].stress == "primary":
                if has_primary:
                    syllables[index].mod_stress("secondary")
                else:
                    has_primary = True
        return syllables
    # Returns the original list with all None removed
    def exclude_none(candidates, print_excluded_amount=False):
        count = 0
        valid_candidates = []
        for candidate in candidates:
            if candidate == None:
                count += 1
            else:
                valid_candidates += [candidate]
        if print_excluded_amount:
            print(len(candidates) - count, "option(s) remaining;", count, "option(s) removed")
        return valid_candidates
    # Lists out all possible patterns of the word (syllables)
    def exhaust_candidates(self):
        consider_weight = not "weight" in self.not_considering
        consider_shortening = not "shortening" in self.not_considering
        def all_possibility(whether_schwa, weight):
            possibilities = []
            if whether_schwa:
                proxy_schwa = "mora"
            else:
                proxy_schwa = "not schwa"
            if consider_weight:
                if consider_shortening and weight == "H":
                    proxy_weights = ["L shortened", "H"]
                else:
                    proxy_weights = [weight]
            else:
                proxy_weights = ["L"]
            for proxy_weight in proxy_weights:
                possibilities += [ProxySyllable(proxy_schwa, "unstressed", "none", proxy_weight)]
                for stress in ["unstressed","primary"]:
                    possibilities += [ProxySyllable(proxy_schwa, stress, "half", proxy_weight)]
                possibilities += [ProxySyllable(proxy_schwa, "primary", "whole", proxy_weight)]
                if whether_schwa:
                    for foot_position in ["none","half","whole"]:
                        possibilities += [ProxySyllable("nonmora", "unstressed", foot_position, proxy_weight)]
            return possibilities    
        def append(preceding_syllables, current_whether_schwa, current_weight):
            to_append = all_possibility(current_whether_schwa, current_weight)
            return [preceding_syllables + [syllable] for syllable in to_append]
        def refresh(possibility):
            for i in range(len(possibility)):
                possibility[i] = possibility[i].copy()
            return possibility
        def mod_half(possibility):
            foot_closed = True
            for i in range(len(possibility)):
                if possibility[i].foot_position == "half":
                    if foot_closed:
                        if i + 1 >= len(possibility) or possibility[i + 1].foot_position != "half":
                            return None
                        if (possibility[i].stress != "unstressed") == (possibility[i + 1].stress != "unstressed"):
                            return None
                        if (possibility[i].weight == "H" or possibility[i].stress != "unstressed") and possibility[i + 1].weight == "H":
                            return None
                        possibility[i].mod_position("left")
                    else:
                        possibility[i].mod_position("right")
                    foot_closed = not foot_closed
            return possibility
        possibilities = [[]]
        for syllable in self.syllables:
            temp = []
            for preceding_syllables in possibilities:
                temp += append(preceding_syllables, syllable.schwa, syllable.weight)
            possibilities = temp
        for i in range(len(possibilities)):
            possibilities[i] = refresh(possibilities[i])
        for i in range(len(possibilities)):
            possibilities[i] = mod_half(possibilities[i])
        return possibilities
    # Returns the candidates with the minimum violations of the specific kind
    def min_vio(candidates, violation):
        i = 0
        while candidates[i] == None:
            i += 1
        min_penalty = 2 ** len(candidates[i])
        min_index = -1
        while i < len(candidates):
            if candidates[i] != None:
                penalty = Stress.penalty(candidates[i], violation)
                if penalty < min_penalty:
                    min_penalty = penalty
                    min_index = i
                elif penalty > min_penalty:
                    candidates[i] = None
            i += 1
        for i in range(min_index):
            candidates[i] = None
        return candidates
    # Pick out possibilities based on violations in rank
    def op(self, print_process=False, mode="CV", max_print=100):
        candidates = Stress.exclude_none(self.exhaust_candidates())
        if print_process:
            print("Initial candidates:")
            Stress.print_candidates(candidates,max_print=max_print,mode=mode)
        print()
        for violation in self.violations:
            if len(candidates) == 1:
                break
            if not violation.in_effect:
                continue
            candidates = Stress.min_vio(candidates, violation)
            if print_process:
                print("Considering ", violation.name, sep="", end=": ")
                candidates = Stress.exclude_none(candidates,True)
                if mode != "none":
                    Stress.print_candidates(candidates, mode=mode)
                print()
            else:
                candidates = Stress.exclude_none(candidates,False)
        for i in range(len(candidates)):
            candidates[i] = Stress.classify_stress(candidates[i])
        return candidates
    # Returns the specific violation by syllables in the candidate in value
    def penalty(candidate, violation):
        match violation.name:
            case "Trochee":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    violate = False
                    match candidate[index].foot_position:
                        case "none":
                            pass
                        case "left":
                            if candidate[index].stress != "unstressed":
                                if not candidate[index + 1].schwa != "nonmora" and candidate[index].weight != "H":
                                    violate = True
                            else:
                                if candidate[index].schwa != "nonmora":
                                    violate = True
                        case "right":
                            if candidate[index].stress != "unstressed":
                                if candidate[index - 1].schwa != "nonmora" or candidate[index].weight != "H":
                                    violate = True
                        case "whole":
                            if candidate[index].stress != "unstressed" and candidate[index].weight != "H":
                                violate = True
                    if violate:
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "Iamb":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    violate = False
                    match candidate[index].foot_position:
                        case "none":
                            pass
                        case "left":
                            if candidate[index].stress != "unstressed":
                                if candidate[index + 1].schwa != "nonmora" or candidate[index].weight != "H":
                                    violate = True
                        case "right":
                            if candidate[index].stress != "unstressed":
                                if not candidate[index - 1].schwa != "nonmora" and candidate[index].weight != "H":
                                    violate = True
                            else:
                                if candidate[index].schwa != "nonmora":
                                    violate = True
                        case "whole":
                            if candidate[index].stress != "unstressed" and candidate[index].weight != "H":
                                violate = True
                    if violate:
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "Parse":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].foot_position == "none":
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "NonFin":
                if violation.direction == "R":
                    fin = candidate[-1].stress
                else:
                    fin = candidate[0].stress
                if fin == "unstressed":
                    return 0
                return 1
            case "HD(w)":
                for syllable in candidate:
                    if syllable.foot_position != "none":
                        return 0
                return 1
            case "Bal-Troch":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].foot_position =="right" and candidate[index].stress == "unstressed":
                        if candidate[index - 1].weight == "H" or candidate[index].weight == "H":
                            sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "Foot-Right":
                if violation.direction == "R":
                    fin = candidate[-1].foot_position
                else:
                    fin = candidate[0].foot_position
                if fin == "none":
                    return 1
                return 0
            case "Max(μ)":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].weight == "L shortened":
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "*Stressed/ə":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].schwa != "not schwa" and candidate[index].stress != "unstressed":
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "*Long-V":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].weight == "H":
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "*μ/ə":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].schwa == "mora":
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "HD(ft)":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].foot_position == "whole" and candidate[index].schwa == "nonmora":
                        sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case "*Clash":
                sum = 0
                for i in range(len(candidate)):
                    if violation.direction == "L":
                        index = -1 - i
                    else:
                        index = i
                    if candidate[index].stress != "unstressed":
                        if (index > 0 and candidate[index - 1].stress != "unstressed") or (index + 1 < len(candidate) and candidate[index + 1].stress != "unstressed"):
                            sum += 2 ** (len(candidate) - 1 - i)
                return sum
            case _:
                print("Invalid violation type")
                return -1
    # Prints out the first up to max_print candidates
    def print_candidates(candidates, max_print=100, mode="CV"):
        count = 0
        for candidate in candidates:
            if candidate != None:
                count += 1
                if count > max_print:
                    print("The rest hidden due to length bound")
                    break
                print(count, ". ", sep="", end="")
                Stress.print_syllables(candidate, mode)
    # Prints out the word (syllables) in the pattern represented through proxy syllables
    def print_mod_syllables(self, proxy_syllables):
        temp = []
        for i in range(len(self.syllables)):
            temp += [self.syllables[i].copy()]
            temp[i].apply(proxy_syllables[i])
        return Stress.print_syllables(temp)
    # Prints out the given syllables
    def print_syllables(syllables, mode="original"):
        word = ""
        for syllable in syllables:
            if mode == "weight":
                if syllable.weight == "H":
                    string = "H"
                else:
                    string = "L"
                if syllable.stress == "primary":
                    string = "ˈ" + string
                elif syllable.stress == "secondary":
                    string = "ˌ" + string
            else:
                string = str(syllable)
            match syllable.foot_position:
                case "none":
                    pass
                case "left":
                    string = "(" + string
                case "right":
                    string += ")"
                case "whole":
                    string = "(" + string + ")"
            if type(syllable) == ProxySyllable and mode != "weight":
                string += " "
            word += string
            print(string,end="")
        print()
        return word
    # Takes aspects to ignore in the process: weight, shortening
    def take_not_considering(self):
        print("Enter aspects to ignore; end the input with \"end\"")
        while True:
            string = input()
            if string == "end":
                break
            if string in ["weight", "shortening"]:
                self.not_considering += [string]
            else:
                print("Unknown aspect")
            print("Current list of aspects to ignore:", self.not_considering)
    # Takes violation rule inputs
    def take_violations(self):
        print("Enter violation rules in the format of \"name, direction(L/R)\"; end the input with \"end\"")
        while True:
            string = input()
            if string == "end":
                break
            try:
                sep = string.split(", ")
                self.add(sep[0], sep[1])
            except:
                print("Input not accepted")
    # Takes weight inputs to specify for each syllable before computing
    def take_weights(self):
        print("Enter weights of syllables in string of L/H, no space in between")
        while True:
            string = input()
            try:
                assert len(string) == len(self.syllables)
                for i in range(len(string)):
                    self.syllables[i].mod_weight(string[i])
                break
            except:
                print("Input not accepted")
            
def parse(print_process=False,mode="CV",max_print=100):
    print("Enter the word or number of syllables to parse: ")
    has_word = True
    while True:
        string = input()
        try:
            n = int(string)
            word = ""
            for i in range(n):
                word += "ca"
            stress = Stress(Syllable.to_syllable_array(word))
            has_word = False
            break
        except:
            try:
                stress = Stress(Syllable.to_syllable_array(string))
                break
            except:
                print("Error occurred; enter the word again: ")
    print()
    stress.take_violations()
    print()
    stress.take_not_considering()
    print()
    if not "weight" in stress.not_considering:
        stress.take_weights()
        print()
    start_time = time.time()
    candidates = stress.op(print_process=print_process,mode=mode,max_print=max_print)
    for i in range(len(candidates)):
        if len(candidates) > 1:
            print(i + 1, ". ", sep="", end="\t")
        print("Stress pattern: ", end="")
        Stress.print_syllables(candidates[i], mode=mode)
        if len(candidates) > 1:
            print("\t", end="")
        if has_word:
            print("Parsed word: ", end="")
            word = stress.print_mod_syllables(candidates[i])
        print()
    print("Calculation and printing done in", time.time()-start_time, "seconds")
    if has_word:
        if len(candidates) == 1:
            return word
        else:
            return "More than one candidate"
    else:
        return "No word provided"


print(parse(True,"weight"))