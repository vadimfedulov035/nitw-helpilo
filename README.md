# nitw-helpilo
## Python script to simplify modifications of Night in the Woods phrases

[![video](https://github.com/vadimfedulov035/nitw-helpilo/raw/main/cover.png)](https://www.youtube.com/watch?v=u17kM8oSz3k)

Klaku sur bildon por spekti anticipfilmeton pri la ludo!

With the help of [NITW-Dialogue-Tool](https://github.com/emberimp/NITW-Dialogue-Tool) it became possible to extract all the .yarn.txt files from the .assets Unity archived files of Night in the Woods game. This script goes a little bit further by collecting all the names and phrases of the characters from already extracted files in one file, simplifying the process of modifications and eliminating the need to see all the stuff behind the scenes while changing phrases.

Regex codes used for fetching names and phrases respectively (firstly special lines are replaced for convenience):

NITW re_basic_line search pattern: https://regex101.com/r/FIpyta/5

NITW re_special_line search pattern: https://regex101.com/r/2e55Rf/5

`python ./main `| `-r` to decipher originally substituted russificated files| `-e` to translate original emoticons in Esperanto (the script was created to simplify translation of the game in Esperanto, so chances are 99.9% that you won't need it)

### Steps:
1) Extracts all names and phrases from the .yarn.txt files situated in "original" directory into "phrases.txt" via structure: total_line_num:name:phrase
2) Copies content of "phrases_collected.txt" into "phrases_translated.txt", if it didn't existed before, in other case asks for permission to rewrite
3) Writes all phrase addresses into "phrase_addresses.txt", this way becomes possible to learn which specific file is being modified and where exactly while changing "phrases_translated.txt", via strucure: total_line_num/filename/line_num/start_of_phrase/end_of_phrase
4) Copies content of "original" directory to "not_patched" created on the fly (needed to preserve possible automatic changes based on elected options "-r" or "-e")

`python ./main -p`

### Steps:
1) Patches the content of created on the previous step "not_patched" directory based on modified by the user "phrased_translated.txt" and writes all the changes into "patched" directory created on the fly.

From now you can provide files from "patched" directory to [NITW-Dialogue-Tool](https://github.com/emberimp/NITW-Dialogue-Tool) and change Night in the Woods any way you want from the text viewpoint.

Support my translation here:
https://github.com/vadimfedulov035/nitw_taduko
