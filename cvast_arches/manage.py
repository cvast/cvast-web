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

#!/usr/bin/env python
import os
import sys
from django.core.management import execute_from_command_line
from cvast_arches import settings

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cvast_arches.settings")
    
    if settings.DEBUG:
        import ptvsd
        debug_secret = settings.get_optional_env_variable("DEBUG_SECRET")
        ptvsd.enable_attach(debug_secret, address = ('0.0.0.0', 3000))

    execute_from_command_line(sys.argv) 

