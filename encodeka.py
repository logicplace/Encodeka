#!/usr/bin/env python
#-*- coding:utf-8 -*-

# MIT Licensed (c) 2012 Sapphire Becker (logicplace.com)

import os
import errno
import codecs
import tempfile
from sys import stdin, stderr, exit
from optparse import OptionParser

ENCODINGS = [
	["ascii", ["646", "us-ascii"], ["English"]],
	["big5", ["big5-tw", "csbig5"], ["Traditional Chinese"]],
	["big5hkscs", ["big5-hkscs", "hkscs"], ["Traditional Chinese"]],
	["cp037", ["IBM037", "IBM039"], ["English"]],
	["cp424", ["EBCDIC-CP-HE", "IBM424"], ["Hebrew"]],
	["cp437", ["437", "IBM437"], ["English"]],
	["cp500", ["EBCDIC-CP-BE", "EBCDIC-CP-CH", "IBM500"], ["Western Europe"]],
	["cp720", [""], ["Arabic"]],
	["cp737", [""], ["Greek"]],
	["cp775", ["IBM775"], ["Baltic languages"]],
	["cp850", ["850", "IBM850"], ["Western Europe"]],
	["cp852", ["852", "IBM852"], ["Central and Eastern Europe"]],
	["cp855", ["855", "IBM855"], ["Bulgarian", "Byelorussian", "Macedonian", "Russian", "Serbian"]],
	["cp856", [""], ["Hebrew"]],
	["cp857", ["857", "IBM857"], ["Turkish"]],
	["cp858", ["858", "IBM858"], ["Western Europe"]],
	["cp860", ["860", "IBM860"], ["Portuguese"]],
	["cp861", ["861", "CP-IS", "IBM861"], ["Icelandic"]],
	["cp862", ["862", "IBM862"], ["Hebrew"]],
	["cp863", ["863", "IBM863"], ["Canadian"]],
	["cp864", ["IBM864"], ["Arabic"]],
	["cp865", ["865", "IBM865"], ["Danish", "Norwegian"]],
	["cp866", ["866", "IBM866"], ["Russian"]],
	["cp869", ["869", "CP-GR", "IBM869"], ["Greek"]],
	["cp874", [""], ["Thai"]],
	["cp875", [""], ["Greek"]],
	["cp932", ["932", "ms932", "mskanji", "ms-kanji"], ["Japanese"]],
	["cp949", ["949", "ms949", "uhc"], ["Korean"]],
	["cp950", ["950", "ms950"], ["Traditional Chinese"]],
	["cp1006", [""], ["Urdu"]],
	["cp1026", ["ibm1026"], ["Turkish"]],
	["cp1140", ["ibm1140"], ["Western Europe"]],
	["cp1250", ["windows-1250"], ["Central and Eastern Europe"]],
	["cp1251", ["windows-1251"], ["Bulgarian", "Byelorussian", "Macedonian", "Russian", "Serbian"]],
	["cp1252", ["windows-1252"], ["Western Europe"]],
	["cp1253", ["windows-1253"], ["Greek"]],
	["cp1254", ["windows-1254"], ["Turkish"]],
	["cp1255", ["windows-1255"], ["Hebrew"]],
	["cp1256", ["windows-1256"], ["Arabic"]],
	["cp1257", ["windows-1257"], ["Baltic languages"]],
	["cp1258", ["windows-1258"], ["Vietnamese"]],
	["euc_jp", ["eucjp", "ujis", "u-jis"], ["Japanese"]],
	["euc_jis_2004", ["jisx0213", "eucjis2004"], ["Japanese"]],
	["euc_jisx0213", ["eucjisx0213"], ["Japanese"]],
	["euc_kr", ["euckr", "korean", "ksc5601", "ks_c-5601", "ks_c-5601-1987", "ksx1001", "ks_x-1001"], ["Korean"]],
	["gb2312", ["chinese", "csiso58gb231280", "euc-cn", "euccn", "eucgb2312-cn", "gb2312-1980", "gb2312-80", "iso-ir-58"], ["Simplified Chinese"]],
	["gbk", ["936", "cp936", "ms936"], ["Unified Chinese"]],
	["gb18030", ["gb18030-2000"], ["Unified Chinese"]],
	["hz", ["hzgb", "hz-gb", "hz-gb-2312"], ["Simplified Chinese"]],
	["iso2022_jp", ["csiso2022jp", "iso2022jp", "iso-2022-jp"], ["Japanese"]],
	["iso2022_jp_1", ["iso2022jp-1", "iso-2022-jp-1"], ["Japanese"]],
	["iso2022_jp_2", ["iso2022jp-2", "iso-2022-jp-2"], ["Japanese", "Korean", "Simplified Chinese", "Western Europe", "Greek"]],
	["iso2022_jp_2004", ["iso2022jp-2004", "iso-2022-jp-2004"], ["Japanese"]],
	["iso2022_jp_3", ["iso2022jp-3", "iso-2022-jp-3"], ["Japanese"]],
	["iso2022_jp_ext", ["iso2022jp-ext", "iso-2022-jp-ext"], ["Japanese"]],
	["iso2022_kr", ["csiso2022kr", "iso2022kr", "iso-2022-kr"], ["Korean"]],
	["latin_1", ["iso-8859-1", "iso8859-1", "8859", "cp819", "latin", "latin1", "L1"], ["West Europe"]],
	["iso8859_2", ["iso-8859-2", "latin2", "L2"], ["Central and Eastern Europe"]],
	["iso8859_3", ["iso-8859-3", "latin3", "L3"], ["Esperanto", "Maltese"]],
	["iso8859_4", ["iso-8859-4", "latin4", "L4"], ["Baltic languages"]],
	["iso8859_5", ["iso-8859-5", "cyrillic"], ["Bulgarian", "Byelorussian", "Macedonian", "Russian", "Serbian"]],
	["iso8859_6", ["iso-8859-6", "arabic"], ["Arabic"]],
	["iso8859_7", ["iso-8859-7", "greek", "greek8"], ["Greek"]],
	["iso8859_8", ["iso-8859-8", "hebrew"], ["Hebrew"]],
	["iso8859_9", ["iso-8859-9", "latin5", "L5"], ["Turkish"]],
	["iso8859_10", ["iso-8859-10", "latin6", "L6"], ["Nordic languages"]],
	["iso8859_13", ["iso-8859-13", "latin7", "L7"], ["Baltic languages"]],
	["iso8859_14", ["iso-8859-14", "latin8", "L8"], ["Celtic languages"]],
	["iso8859_15", ["iso-8859-15", "latin9", "L9"], ["Western Europe"]],
	["iso8859_16", ["iso-8859-16", "latin10", "L10"], ["South-Eastern Europe"]],
	["johab", ["cp1361", "ms1361"], ["Korean"]],
	["koi8_r", [""], ["Russian"]],
	["koi8_u", [""], ["Ukrainian"]],
	["mac_cyrillic", ["maccyrillic"], ["Bulgarian", "Byelorussian", "Macedonian", "Russian", "Serbian"]],
	["mac_greek", ["macgreek"], ["Greek"]],
	["mac_iceland", ["maciceland"], ["Icelandic"]],
	["mac_latin2", ["maclatin2", "maccentraleurope"], ["Central and Eastern Europe"]],
	["mac_roman", ["macroman"], ["Western Europe"]],
	["mac_turkish", ["macturkish"], ["Turkish"]],
	["ptcp154", ["csptcp154", "pt154", "cp154", "cyrillic-asian"], ["Kazakh"]],
	["shift_jis", ["csshiftjis", "shiftjis", "sjis", "s_jis"], ["Japanese"]],
	["shift_jis_2004", ["shiftjis2004", "sjis_2004", "sjis2004"], ["Japanese"]],
	["shift_jisx0213", ["shiftjisx0213", "sjisx0213", "s_jisx0213"], ["Japanese"]],
	["utf_32", ["U32", "utf32"], ["all languages"]],
	["utf_32_be", ["UTF-32BE"], ["all languages"]],
	["utf_32_le", ["UTF-32LE"], ["all languages"]],
	["utf_16", ["U16", "utf16"], ["all languages"]],
	["utf_16_be", ["UTF-16BE"], ["all languages"]],
	["utf_16_le", ["UTF-16LE"], ["all languages"]],
	["utf_7", ["U7", "unicode-1-1-utf-7"], ["all languages"]],
	["utf_8", ["U8", "UTF", "utf8"], ["all languages"]],
	["utf_8_sig", [""], ["all languages"]],
]

families = {
	"big5": ["big5", "big5hkscs"],
	"euc_jp": ["euc_jp", "euc_jis_2004", "euc_jisx0213"],
	"gb": ["gb2312", "gbk", "gb18030"],
	"iso2022": ["iso2022_jp", "iso2022_jp_1", "iso2022_jp_2", "iso2022_jp_2004", "iso2022_jp_3", "iso2022_jp_ext", "iso2022_kr"],
	"iso8859": ["iso8859_2", "iso8859_3", "iso8859_4", "iso8859_5", "iso8859_6", "iso8859_7", "iso8859_8", "iso8859_9", "iso8859_10", "iso8859_13", "iso8859_14", "iso8859_15", "iso8859_16"],
	"mac": ["mac_cyrillic", "mac_greek", "mac_iceland", "mac_latin2", "mac_roman", "mac_turkish"],
	"windows": ["cp932", "cp949", "cp950", "cp1250", "cp1251", "cp1252", "cp1253", "cp1254", "cp1255", "cp1256", "cp1257", "cp1258"],
	"ibm": ["cp037", "cp424", "cp437", "cp500", "cp775", "cp850", "cp852", "cp855", "cp857", "cp858", "cp860", "cp861", "cp862", "cp863", "cp864", "cp865", "cp866"],
	"shift_jis": ["shift_jis", "shift_jis_2004", "shift_jisx0213"],
	"utf32": ["utf_32", "utf_32_be", "utf_32_le"],
	"utf16": ["utf_16", "utf_16_be", "utf_16_le"],
	"utf8": ["utf_8", "utf_8_sig"],
}

encodings = []
for e in ENCODINGS:
	encodings.append(e[0])
	for a in e[1]: encodings.append(a)
#endfor

languages = {}
for e in ENCODINGS:
	for l in e[2]:
		l = l.lower()
		if l not in languages: languages[l] = [e[0]]
		else: languages[l].append(e[0])
	#endfor
#endfor

def print_table(head, table):
	maxw = [] # Max Width
	# Start with header lengths
	for x in head: maxw.append(len(x))

	lines = []
	seps = []
	for row in table:
		# Maximum height of row
		maxlen = 0
		for i, col in enumerate(row):
			if type(col) is not list: row[i] = col = [col]
			maxlen = max(maxlen, len(col))
		#endfor

		# Maximum length findings
		for n in range(maxlen):
			line = []
			for i, col in enumerate(row):
				if n < len(col):
					line.append(col[n])
					maxw[i] = max(maxw[i], len(col[n]))
				else: line.append("")
			#endfor
			lines.append(line)
		#endfor
		seps.append(len(lines) - 1)
	#endfor

	# Print
	line = ""
	for i, x in enumerate(head): line += "+-%s%s-" % (x, "-" * (maxw[i] - len(x)))
	print line + "+"
	line = ("| %%-%is " * len(head) + "|") % tuple(maxw)
	sep = ("+-%s-" * len(head) + "+") % tuple(map(lambda x: "-" * x, maxw))
	for i, l in enumerate(lines):
		print line % tuple(l)
		if i in seps: print sep
	#endfor
#enddef

def main():
	parser = OptionParser(usage="Usage: %prog [options] [file | string | -i]")
	parser.add_option("-l", "--list", action="store_true",
		help="List all, encodings, families, or languages."
	)
	parser.add_option("-e", "--encoding", action="append",
		help="Test given encoding."
	)
	parser.add_option("-f", "--family", action="append",
		help="Test entirety of given family."
	)
	parser.add_option("-L", "--language", "--lang", action="append",
		help="Test entirety of given language."
	)
	parser.add_option("-a", "--all", action="store_true",
		help="Test all encodings."
	)
	parser.add_option("-o", "--output",
		help="Output folder (default: make one in temp)."
	)
	parser.add_option("-s", "--string", action="store_true",
		help="Input is string data, not a folder."
	)
	parser.add_option("-i", action="store_true", dest="stdin",
		help="Read from stdin (implies --string)."
	)
	parser.add_option("-v", "--verbose", action="store_true",
		help="Show decoding failures."
	)
	parser.add_option("-n", "--names", action="store_true",
		help="Print list of filenames instead of samples (not usable with --string)."
	)
	options, args = parser.parse_args()

	if options.list:
		l3 = []
		for x in args: l3.append(x[0:3].lower())
		if not l3 or "enc" in l3:
			print_table(["Name", "Aliases", "Languages"], ENCODINGS)
		#endif
		if not l3 or "fam" in l3:
			print_table(["Family", "Members"], sorted(map(lambda x: [x, families[x]], families)))
		#endif
		if not l3 or "lan" in l3:
			print_table(["Language", "Encodings"], sorted(map(lambda x: [x, languages[x]], languages)))
		#endif
		return 0
	#endif

	if (len(args) == 0 and not options.stdin) or (options.encoding is None and
		options.family is None and options.language is None
	):
		parser.print_help()
		return 0
	#endif

	# Collect encoding test requests
	selected = []
	if options.all: selected = map(lambda x: x[0], ENCODINGS)
	else:
		for x in (options.encoding or []):
			if x in encodings: selected.append(x)
			else: stderr.write('Unknown encoding "%s"\n"' % x)
		#endfor
		for x in (options.family or []):
			x = x.lower()
			if x in families: selected += families[x]
			else: stderr.write('Unknown family "%s"\n"' % x)
		#endfor
		for x in (options.language or []):
			x = x.lower()
			if x in languages: selected += languages[x]
			else: stderr.write('Unknown language "%s"\n"' % x)
		#endfor
	#endif

	if not selected:
		stderr.write("No real encodings selected to test. Maybe use --all?")
		return 2
	#endif

	one = len(selected) == 1

	# Collect data
	if options.stdin: data = stdin.read()
	elif options.string: data = args[0]
	else:
		f = open(args[0], "rb")
		data = f.read()
		f.close()
	#endif

	if not data:
		stderr.write("No data to test.")
		return 3
	#endif

	isfile = not options.string

	if isfile and not one:
		tmpdir = options.output or tempfile.mkdtemp()
		try: os.makedirs(tmpdir)
		except OSError, e:
			if e.errno == errno.EEXIST: pass
			else:
				stderr.write('Error when making %s "%s": %s' % (
					"folder" if options.output else "temp folder",
					tmpdir, os.strerror(e.errno)
				))
				return 4
			#endif
		#endif
		if not one: stderr.write('Compare full files at "%s"\n' % tmpdir)
	#endif

	for x in selected:
		try: string = data.decode(x)
		except:
			if options.verbose: stderr.write('Could not decode with "%s"\n' % x)
		else:
			if options.string or one:
				if one: print string.encode("utf8")
				else: print u'%s: %s'  % (x, string)
			else:
				fn = os.path.join(tmpdir, "%s%stxt" % (x, os.extsep))
				f = codecs.open(fn, "w", "utf8")
				f.write(string)
				f.close()
				if options.names: print fn
				elif one: u"Sample: %s"  % (string[0:30])
				else: print u'"%s" sample: %s'  % (x, string[0:30])
			#endif
		#endtry
	#endfor
	if not one: stderr.write("Tests complete\n")
#enddef

if __name__ == "__main__": exit(main())
