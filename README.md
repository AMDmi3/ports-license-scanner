# ports-license-scanner

This utility scans FreeBSD portstree and compares licenses defined
in the ports with licenses extracted from port sources.

## Depends

* python36+ (lang/python36)
* py3-sqlite3 (databases/py36-sqlite3)
* nomos license scanner (devel/fossology-nomos-standalone)

## Usage

The utility relies on fossology nomos license scanner which is horribly slow,
so instead of just printing scan results it maintains a database of gathered
data and allows scanning and examining results in parallel.

Run ```./pls.py [-v] scan [origins...]``` to scan ports and store data in the
database. Specify ```-v``` for verbose operation. List origins to only process
specific ports. By defaults scans the whole portstree from beginning.

Run ```./pls.py show [origins...]``` to show gathered lincese information.

## Author

* [Dmitry Marakasov](https://github.com/AMDmi3) <amdmi3@amdmi3.ru>

## License

MIT, see COPYING.
