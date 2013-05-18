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

int main(int argc, char **argv) {
	if (argc != 4)
		return 1;
	QSettings first(argv[1], QSettings::IniFormat);
	QSettings second(argv[2], QSettings::IniFormat);
	QSettings result(argv[3], QSettings::IniFormat);
	QStringList firstKeys = first.allKeys();
	QStringList secondKeys = second.allKeys();
	for (int i = 0; i < secondKeys.length(); ++i) {
		if (!firstKeys.contains(secondKeys[i])
				||
			second.value(secondKeys[i]) != first.value(secondKeys[i])
		) {
			result.setValue(secondKeys[i], second.value(secondKeys[i]));
		}
	}
	return 0;
}

