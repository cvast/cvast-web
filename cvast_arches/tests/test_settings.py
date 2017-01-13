'''
ARCHES - a program developed to inventory and manage immovable cultural heritage.
Copyright (C) 2013 J. Paul Getty Trust and World Monuments Fund

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''



from cvast_arches.settings import *
import os
import inspect


PACKAGE_NAME = 'arches'
ROOT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
ROOT_DIR = os.path.normpath(os.path.join(ROOT_DIR, '..', 'arches'))
PACKAGE_ROOT = os.path.normpath(os.path.join(ROOT_DIR, '..', 'tests'))

LANGUAGE_CODE = 'en-US'

RESOURCE_GRAPH_LOCATIONS = os.path.join(PACKAGE_ROOT, 'fixtures'),

#########################################
###  START PACKAGE SPECIFIC SETTINGS  ###
#########################################

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'arches',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': 'postgis',                  # Not used with sqlite3.
        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        'SCHEMAS': 'public,data,ontology,concepts', # syncdb will put the admin tables in the first listed schema,
        'POSTGIS_TEMPLATE': 'template_postgis_20',
    }
}
