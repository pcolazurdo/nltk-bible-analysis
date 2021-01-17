# This sample code uses Bible API to download a JSON representation of a full Bible book
# to get the list of available Bibles: https://bibliaapi.com/docs/Available_Bibles
# to get your own personal key: https://api.biblia.com/v1/Users/SignIn

import json
import urllib3
import sys
from getopt import getopt
from configparser import ConfigParser


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


class BibliaDownload:

    _url_root = None
    _key = None
    _http = None
    _argv = None

    def __init__(self, argv):
        config = ConfigParser()
        config.read('parse-text.ini')
        self._key = config.get('main', 'biblia_key')

        if self._argv is None:
            self._argv = argv[1:]

    def get_text(self, passage):
        # print(passage)
        r = self._http.request(
            'GET',
            self._url_root,
            fields={
                'key': self._key,
                'passage': passage}
        )
        # print(r.status)
        if (r.status != 200):
            return None
        else:
            return json.loads(r.data.decode('utf-8'))

    def download_book(self, book_name=None, from_chapter=None, to_chapter=None):
        if (from_chapter is None):
            from_chapter = 1
        if (to_chapter is None):
            to_chapter = 150
        eprint("Download chapters {} to {} (if they exist)".format(from_chapter, to_chapter))
        break_counter = 0
        json_dict = {
            "book": book_name,
            "chapters": []
        }
        for chap in range(from_chapter, to_chapter + 1):  # + 1 because range is not inclusive
            if (break_counter > 1):
                break
            verses_arr = []
            for verse in range(1, 100):
                r = self.get_text('{}{}:{}'.format(book_name, chap, verse))
                # print(r)
                if (r and 'text' in r):
                    break_counter = 0
                    verses_arr.append({
                        "verse": verse,
                        "text": r["text"]
                    })
                else:
                    break_counter = break_counter + 1
                    break
            if (len(verses_arr) > 0):
                json_dict["chapters"].append({
                    "chapter": chap,
                    "verses": verses_arr
                })
        return json_dict

    def list_bibles(self):
        r = self._http.request(
            'GET',
            "https://api.biblia.com/v1/bible/find",
            fields={
                'key': self._key
            }
        )
        # print(r.status)
        if (r.status != 200):
            return None
        else:
            return json.loads(r.data.decode('utf-8'))

    def usage(self):
        eprint("Usage is:")
        eprint("  {}: [-hb] --book=string [--from-chapter=n] [--to-chapter=n] [--bible-version=string]".format(sys.argv[0]))
        eprint("  Options")
        eprint("        -h                        (Optional) Displays this text")
        eprint("        -b                        (Optional) Query possible Bibles")
        eprint("        --book=string             (Required) English name of the bible book. Complex Names are represented without spaces. i.e. 1Peter")
        eprint("        --from-chapter=int        (Optional) Starting Chapter number - default: 1")
        eprint("        --to-chapter=int          (Optional) Ending Chapter number - default: 150")
        eprint("        --bible-version=string    (Optional) Id of the Version to process - default: RVR60")
        sys.exit(1)

    def Run(self):
        self._http = urllib3.PoolManager()

        s_opts = "hb"
        l_opts = (
            "help",
            "book=",
            "from-chapter=",
            "to-chapter=",
            "bible-version=",
        )

        opts, args = getopt(self._argv, s_opts, l_opts)
        from_chapter = None
        to_chapter = None
        book = None
        bible_version = 'RVR60'
        for opt, val in opts:
            eprint("opt", opt, "val", val)
            if opt in ("-b", "--bible"):
                r = self.list_bibles()
                print(json.dumps(r))
                sys.exit(0)
            if opt in ("--from-chapter="):
                from_chapter = int(val)
            elif opt in ("--to-chapter="):
                to_chapter = int(val)
            elif opt in ("--book="):
                book = val
            elif opt in ("--bible-version="):
                bible_version = val
            elif opt in ("-h", "--help"):
                self.usage()
        # if not args:
        #     self.usage()

        self._url_root = 'https://api.biblia.com/v1/bible/content/{}.txt.js'.format(bible_version)
        eprint('Downloading {}: {} {} {}'.format(bible_version, book, from_chapter, to_chapter))
        if (book):
            r = self.download_book(book, from_chapter, to_chapter)
            print(json.dumps(r))
        else:
            self.usage()
        sys.exit(0)


if (__name__ == "__main__"):
    c = BibliaDownload(sys.argv)
    c.Run()
