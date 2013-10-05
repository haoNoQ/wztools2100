/*
 *   compiling:
 *   	qmake -project
 *   	qmake
 *   	make
 *
 *   usage:
 *   	ini-diff first.ini second.ini output.ini
 *
 *   Outputs an INI diff that will be usable as a diff file in a WZ diff mod.
 *   Doesn't look at fields that were present in first.ini but are not present
 *   in second.ini, as diff mods can't remove fields.
 */

#include <QSettings>
#include <QStringList>

// returns 0 if str1 and str2 represent the same comma-separated
// list of substrings, probably in different order, 1 otherwise
bool compareAsLists(const QString& str1, const QString& str2) {
	QStringList lst1 = str1.split(",");
	QStringList lst2 = str2.split(",");
	for (int i = 0; i < lst1.length(); ++i)
		if (!lst2.contains(lst1[i]))
			return 1;
	for (int i = 0; i < lst2.length(); ++i)
		if (!lst1.contains(lst2[i]))
			return 1;
	return 0;
}

int main(int argc, char **argv) {
	if (argc != 4)
		return 1;
	QSettings first(argv[1], QSettings::IniFormat);
	QSettings second(argv[2], QSettings::IniFormat);
	QSettings result(argv[3], QSettings::IniFormat);
	QStringList firstKeys = first.allKeys();
	QStringList secondKeys = second.allKeys();
	for (int i = 0; i < secondKeys.length(); ++i) {
		if (!firstKeys.contains(secondKeys[i]))
			result.setValue(secondKeys[i], second.value(secondKeys[i]));
		if (second.value(secondKeys[i]) != first.value(secondKeys[i])) {
			// here we need to check if we have two similar lists
			// in a different order
			QString str1 = first.value(secondKeys[i]).toString();
			QString str2 = second.value(secondKeys[i]).toString();
			if (compareAsLists(str1, str2))
				result.setValue(secondKeys[i], second.value(secondKeys[i]));
		}
	}
	return 0;
}

