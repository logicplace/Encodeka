Command line encoding tester and converter.

Note: The only conversion target encoding will ever be utf8, use iconv if you
 want others.

This is mostly intended for easily testing what encoding a file is in. You may
 test by specific encodings, by language, or by encoding families. This uses
 python's entire [list][http://docs.python.org/library/codecs.html], but you
 can see it with endcodeka.py -l as well.

Quick note: if you use -i it will show samples and save to files, if you use -si
 it will print the entire input to screen. I don't suggest using -si if you
 expect newlines.

# Command Line #
	Usage: encodeka.py [options] [file | string | -i]

	Options:
	  -h, --help            show this help message and exit
	  -l, --list            List all, encodings, families, or languages.
	  -e ENCODING, --encoding=ENCODING
		                    Test given encoding.
	  -f FAMILY, --family=FAMILY
		                    Test entirety of given family.
	  -L LANGUAGE, --language=LANGUAGE, --lang=LANGUAGE
		                    Test entirety of given language.
	  -a, --all             Test all encodings.
	  -o OUTPUT, --output=OUTPUT
		                    Output folder (default: make one in temp).
	  -s, --string          Input is string data, not a folder.
	  -i                    Read from stdin (implies --string).
	  -v, --verbose         Show decoding failures.
	  -n, --names           Print list of filenames instead of samples (not usable
		                    with --string).
