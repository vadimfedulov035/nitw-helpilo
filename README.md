# nitw-helper
## Python script to simplify modifications of Night in the Woods phrases

With the help of [NITW-Dialogue-Tool](https://github.com/emberimp/NITW-Dialogue-Tool) it is possible to extract all .yarn.txt files from the .assets Unity archived files. This script goes a little bit further by collecting all the names and phrases of the characters from already extracted files in one file, simplifying the process of modifications and eliminating the need to see all the stuff behind the scenes.

Regex codes used for fetching names and phrases respectively (firstly special lines are replaced for convinience):

NITW re_basic_line: https://regex101.com/r/FIpyta/3

NITW re_special_line: https://regex101.com/r/2e55Rf/4

`python ./main `| `-r` to decipher originally substituted russificated files| `-e` to translate original emoticons in Esperanto (the script was created to simplify translation of the game in Esperanto, so chances are 99.9% that you won't need it)

1) Extracts all the names and phrases from the .yarn.txt files situated in "original" directory into "phrases.txt"
2) Copies contents of "phrases.txt" into "phrases_translated.txt" if it didn't existed before, in other case asks for permission to rewrite not to delete progress of modification accidentally.
3) Copies content of "original" directory to "not_patched" created on the fly (needed to preserve possible automatic changes based on elected options)
4) Writes addresses of phrases in separate file named "phrase_addresses.txt", each line of this file corresponds to a specific line of "phrases_translated.txt" based on numbering or line order (this option should be available in your text viewer program), this way becomes possible to know which file is being modified and where exactly while changing "phrases_translated.txt", addresses are represented by this structure: filename/line_num/start_of_phrase/end_of_phrase

`python ./main -p`

1) Patches the content of created on the previous step "not_patched" directory based on modified by the user "phrased_translated.txt" and writes all the changes into "patched" directory created on the fly.

From now you can provide files from "patched" directory to [NITW-Dialogue-Tool](https://github.com/emberimp/NITW-Dialogue-Tool) and change Night in the Woods any way you want from the text viewpoint.
