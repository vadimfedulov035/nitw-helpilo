# nitw-helper
Python script to simplify modifications of Night in the Woods phrazes

With the help of NITW-Dialogue-Tool it is possible to extract all .yarn.txt files from the .assets Unity archived files. This script goes a little bit further by collecting all the names and phrazes of the characters from already extracted files in one file, simplifying the process of modifications and eliminating the need to see all the stuff behind the scenes.

`python ./main `| `-r` to decipher originally substituted russificated files| `-e` to translate original emoticons in Esperanto (the program was created to simplify translation of the game in Esperanto, so chances are 99.9% that you won't need it)
1) Extracts all the names and phrazes from the .yarn.txt files situated in "original" directory into "phrazes.txt"
2) Copies contents of "phrazes.txt" into "phrazes_translated.txt", if it didn't existed before, in other case asks for permission to rewrite not to delete progress of modification accidentally.
3) Copies content of "original" directory to "not_patched" for the next step (needed to preserve possible automatic changes based on elected options)
4) Writes addresses of phrazes in separate file named "phraze_addresses.txt", each line of this file corresponds to a specific line of "phrazes_translated.txt" based on its number. (for possibility of knowing which file is being modified and where (file/line/start_of_phraze_end_of_phraze) while changing "phrazes_translated.txt")

`python ./main -p`
1) To patch the content of created on the previous step "not_patched" directory based on "phrazed_translated.txt" changes and write it into "patched" directory.

From this point you can use files from "patched" directory for NITW-Dialogue-Tool and change Night in the Woods to any point you want from the text viewpoint.
