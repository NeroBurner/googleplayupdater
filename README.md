# googleplay-updater-cli
Bulk-updater for a folder with apk-files from googleplay

## Synopsis
```
python2 gp_update.py [-v] <apk_folder_path>
        -v       verbose output
```

## Dependencies

### androguard
androguard https://github.com/androguard/androguard

Patching:

`git checkout tags/1.9`

in the file `androguard/core/bytecodes/api.py` change the following lines

```
from androguard.core import bytecode
from androguard.core import androconf
from androguard.core.bytecodes.dvm_permissions import DVM_PERMISSIONS
```

to

```
from __future__ import absolute_import

from .. import bytecode
from .. import androconf
from .dvm_permissions import DVM_PERMISSIONS
```

googleplay-api https://github.com/timogilvie/googleplay-api

patching:
in `googleplay_api/googleplay.py` change for all done requests `verify=False` with `verify=True`


## Inspiration

Inspired by GooglePlayDownloader and its 'Search updates for local APK(s)'-button http://codingteam.net/project/googleplaydownloader

## Licence
This project is released under the GPLv3 licence.


