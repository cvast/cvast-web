﻿import posixpath
import os
import glob
import codecs

def run_initial_sql():
    here = os.path.dirname(os.path.abspath(__file__))
    db_directory = os.path.abspath(os.path.join(here, '..'))
    path_to_file = os.path.join(db_directory, 'install_db.sql')

    # Generate a sql file that sources all necessary sql files into one file
    buffer = ''
    buffer += "\n\echo Run all the sql scripts in the dependencies folder\n"
    for infile in glob.glob(posixpath.join(db_directory, 'install', 'dependencies', '*.sql')):
        buffer += source(infile.replace("\\", posixpath.sep))

    buffer += "\n\echo Run all the sql scripts in the ddl folder\n"
    for infile in glob.glob(posixpath.join(db_directory, 'ddl', '*.sql')):
        buffer += source(infile.replace("\\", posixpath.sep))

    buffer += "\n\echo Run all the sql scripts in the dml folder\n"
    for infile in glob.glob(posixpath.join(db_directory, 'dml', '*.sql')):
        buffer += source(infile.replace("\\", posixpath.sep))

    buffer += "\n\echo Run all the sql scripts in the postdeployment folder\n"
    for infile in glob.glob(posixpath.join(db_directory, 'install', 'postdeployment', '*.sql')):
        buffer += source(infile.replace("\\", posixpath.sep))

    buffer += "\n\echo Spring cleaning\n"
    buffer += "\n VACUUM ANALYZE\n"

    buffer += "\n\echo Done installing all sql files;\n"
	
    write_to_file(path_to_file, buffer)

    os.system('psql -U postgres -d template_postgis_20 -f %s' % path_to_file)


def write_to_file(fileName, contents, mode='w', encoding='utf-8', **kwargs):
    ensure_dir(fileName)
    file = codecs.open(fileName, mode=mode, encoding=encoding, **kwargs)
    file.write(contents)
    # os.system('chmod -R 777 ' + fileName)
    file.close()


def ensure_dir(f):
    d = os.path.dirname(f)
    if not os.path.exists(d):
        os.makedirs(d)


def source(file):
    return "\i \'" + file + "\'\n"


if __name__ == "__main__":
    run_initial_sql()
