# Google Play Unofficial Python API

An unofficial Python API that let you search, browse and download Android apps from Google Play (formerly Android Market).

This library is inspired by those projects, working with the old version of the API:

* [Android Market Python API](https://github.com/liato/android-market-api-py)
* [Android Market Java API](http://code.google.com/p/android-market-api/)

## Disclaimer
**This is not an official API. I am not afiliated with Google in any way, and am not responsible of any damage that could be done with it. Use it at your own risk.**

## Dependencies
* [Python 2.7+ or Python 3.4+](http://www.python.org)
* [Protocol Buffers](http://code.google.com/p/protobuf/)

## Requirements
You must edit `config.py` before using the provided scripts (`search.py`, `download.py`, `apishell.py`, etc.). First, you need to provide your phone's `androidID`:

    ANDROID_ID      = None # "xxxxxxxxxxxxxxxx"

To get your `androidID`, use `*#*#8255#*#*` on your phone to start *Gtalk Monitor*. The hex string listed after `aid` is your `androidID`.

In order to authenticate to Google Play, you also need to provide either your Google login and password, or a valid subAuthToken.

## Usage

### Searching

    $ python search.py
    Usage: search.py request [nb_results] [offset]
    Search for an app.
    If request contains a space, don't forget to surround it with ""

    $ python search.py earth
    Title;Package name;Creator;Super Dev;Price;Offer Type;Version Code;Size;Rating;Num Downloads
    Google Earth;com.google.earth;Google Inc.;1;Gratuit;1;53;8.6MB;4.46;10 000 000+
    Terre HD Free Edition;ru.gonorovsky.kv.livewall.earthhd;Stanislav Gonorovsky;0;Gratuit;1;33;4.7MB;4.47;1 000 000+
    Earth Live Wallpaper;com.seb.SLWP;unixseb;0;Gratuit;1;60;687.4KB;4.06;5 000 000+
    Super Earth Wallpaper Free;com.mx.spacelwpfree;Mariux;0;Gratuit;1;2;1.8MB;4.41;100 000+
    Earth And Legend;com.dvidearts.earthandlegend;DVide Arts Incorporated;0;5,99 €;1;6;6.8MB;4.82;50 000+
    [...]

Depending on the number of results you ask, you might get an error. My tests show that 100 search results are the maximum, but it may vary.

By default, all scripts have CSV output. You can use Linux's `column` to prettify the output:

    $ alias pp="column -s ';' -t"
    $ python search.py earth | pp
    Title                           Package name                            Creator                  Super Dev  Price    Offer Type  Version Code  Size     Rating  Num Downloads
    Google Earth                    com.google.earth                        Google Inc.              1          Gratuit  1           53            8.6MB    4.46    10 000 000+
    Terre HD Free Edition           ru.gonorovsky.kv.livewall.earthhd       Stanislav Gonorovsky     0          Gratuit  1           33            4.7MB    4.47    1 000 000+
    Earth Live Wallpaper            com.seb.SLWP                            unixseb                  0          Gratuit  1           60            687.4KB  4.06    5 000 000+
    Super Earth Wallpaper Free      com.mx.spacelwpfree                     Mariux                   0          Gratuit  1           2             1.8MB    4.41    100 000+
    Earth And Legend                com.dvidearts.earthandlegend            DVide Arts Incorporated  0          5,99 €   1           6             6.8MB    4.82    50 000+
    Earth 3D                        com.jmsys.earth3d                       Dokon Jang               0          Gratuit  1           12            3.4MB    4.05    500 000+
    [...]

### Browse categories

You can list all app categories this way:

    ID                   Name
    GAME                 Games
    BOOKS_AND_REFERENCE  Books & Reference
    BUSINESS             Business
    COMICS               Comics
    COMMUNICATION        Communication
    EDUCATION            Education
    ENTERTAINMENT        Entertainment
    FINANCE              Finance
    [...]

### List subcategories and apps

All categories have subcategories. You can list them with:

    $ python list.py
    Usage: list.py category [subcategory] [nb_results] [offset]
    List subcategories and apps within them.
    category: To obtain a list of supported catagories, use categories.py
    subcategory: You can get a list of all subcategories available, by supplying a valid category

    $ python list.py WEATHER | pp
    Subcategory ID            Name
    apps_topselling_paid      Top Selling
    apps_topselling_free      Top Apps
    apps_topgrossing          Top Grossing
    apps_topselling_new_paid  Top Selling New
    apps_topselling_new_free  Top New Apps
    apps_movers_shakers       Trending

And then list apps within them:

    $ python list.py WEATHER apps_topselling_free | pp
    Title                           Package name                             Creator                        Super Dev  Price  Offer Type  Version Code  Size    Rating  Num Downloads
    wetter.com                      com.wetter.androidclient                 wetter.com GmbH                0          Free   1           1514242001    10.3MB  4.07    10,000,000+
    Weather Austria XL PRO          com.exovoid.weather.app.at               Exovoid Sàrl                   0          Free   1           29            12.4MB  4.39    50,000+
    MORECAST- Free Premium Weather  com.morecast.weather                     UBIMET                         0          Free   1           206           12.7MB  4.42    500,000+
    [...]
### Viewing permissions

You can use `permissions.py` to see what permissions are required by an app without downloading it:

    $ python search.py gmail 1 | pp
    Title  Package name           Creator      Super Dev  Price  Offer Type  Version Code  Size    Rating  Num Downloads
    Gmail  com.google.android.gm  Google Inc.  1          Free   1           55008625      12.1MB  4.30    1,000,000,000+

    $ python permissions.py com.google.android.gm
    android.permission.ACCESS_NETWORK_STATE
    android.permission.GET_ACCOUNTS
    android.permission.MANAGE_ACCOUNTS
    android.permission.INTERNET
    android.permission.READ_CONTACTS
    android.permission.WRITE_CONTACTS
    android.permission.READ_SYNC_SETTINGS
    android.permission.READ_SYNC_STATS
    android.permission.RECEIVE_BOOT_COMPLETED
    [...]

You can specify multiple apps, using only one request.

### Downloading apps

Downloading an app is really easy, just provide its package name. I only tested with free apps, but I guess it should work as well with non-free as soon as you have enough money on your Google account.

    $ python download.py com.google.android.gm
    Downloading 2.7MB... Done

    $ file com.google.android.gm.apk
    com.google.android.gm.apk: Zip archive data, at least v2.0 to extract

### Interactive shell
An interactive shell can be started using the `apishell.py` script. It initializes the `api` object and logs you in.

    $ python apishell.py

    Google Play Unofficial API Interactive Shell
    Successfully logged in using your Google account. The variable 'api' holds the API object.
    Feel free to use help(api).

    >>> print(api.__doc__)
    Google Play Unofficial API Class
      Usual APIs methods are login(), search(), details(), download(), browse() and list().
      toStr() can be used to pretty print the result (protobuf object) of the previous methods.
      toDict() converts the result into a dict, for easier introspection.

    >>> res = api.search("angry birds")
    >>> for i in res.doc[0].child:
    ...     print(helpers.str_compat(i.title))
    ... 
    Angry Birds
    Angry Birds 2
    Angry Birds POP Bubble Shooter
    Angry Birds Rio
    Angry Birds Transformers
    Angry Birds Star Wars II Free
    Angry Birds Go!
    [...]

All results returned by methods such as `search()`, `details()`, ..., are Protobuf objects. You can use `toStr` and `toDict` method from `GooglePlayAPI` to pretty-print them and make introspection easier if you're not familiar with Protobuf.

    >>> s = api.browse()
    >>> s
    <googleplay_pb2.BrowseResponse object at 0x7f51838c7748>
    >>> d = api.toDict(s)
    >>> d.keys() # on Python 2
    ['promoUrl', 'category', 'contentsUrl']
    >>> d.keys() # on Python 3
    dict_keys(['promoUrl', 'contentsUrl', 'category'])
    >>> print(d['category'])
    [{'name': 'Games', 'dataUrl': 'browse?c=3&cat=GAME'}, {'name': 'Books & Reference', 'dataUrl': 'browse?c=3&cat=BOOKS_AND_REFERENCE'}, {'name': 'Business', 'dataUrl': 'browse?c=3&cat=BUSINESS'}, {'name': 'Comics', 'dataUrl': 'browse?c=3&cat=COMICS'},
    [...]


### Using the API as a module in another project

You only need `googleplay.py` and `googleplay_pb2.py`. All other scripts are just front-ends.

    >>> from googleplay import GooglePlayAPI
    >>> help(GooglePlayAPI)

What else?

### To be continued

Feel free to extend the API, add command-line options to scripts, fork the project, and port it to any language.
You can generate Protobuf stubs from `googleplay.proto` file with Google's `protoc`:

    $ protoc -h
    Usage: protoc [OPTION] PROTO_FILES
    Parse PROTO_FILES and generate output based on the options given:
    [...]
      --cpp_out=OUT_DIR           Generate C++ header and source.
      --java_out=OUT_DIR          Generate Java source file.
      --python_out=OUT_DIR        Generate Python source file.

## License

This project is released under the BSD license.

