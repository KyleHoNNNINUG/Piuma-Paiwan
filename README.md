# Piuma-Paiwan

## Function
The code models the stress pattern of Piuma Paiwan, a Taiwanese native language dialect with the following features:
 * Right-aligned trochee system
 * Penultimate syllable stressed with coda consonants nonmoraic
 * If penult nucleus is schwa (ə)
    * Schwa undergoes reduction
    * Stress shifts to final syllable with vowel lengthened
 * Schwa variants and locations:
    * nonmoraic ə → non-head position of a foot
    * bimoraic ə: → head position of a foot
    * monomoraic ə → elsewhere

## DHS
Directional Harmonic Serialism, a method producing pattern through iterative improvement, more accurate<br/>
The files are independent and differentiated by the subject of object-oriented programming (OOP)
 * pattern-wise: treat the entire pattern as an object (an array of stress, lengthening, parse position, and schwa variant information)
 * syllable-wise: treat each syllable as an object (onset, nucleus, and coda on top of pattern information for printing)

>NOTE: code files within this folder are unfinished and still in process

## OT
Optimality Theory, or Parallel Optimality Theory, a method producing pattern by exhaustively comparing number of violations to given rules<br/>
The program is centered around OOP with each syllable as an object<br/>
Different from conventional P-OT, the program is given direction by introducing index-based weight when calculating the violation score<br/>
The code file is open for testing and adding rules suitable for the language
