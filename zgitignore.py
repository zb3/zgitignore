"""
ZgitIgnore - check if something is ignored by a .(z)gitignore file

This is very similar to .gitignore but slightly modified to allow more.

Features:
- ** works everywhere. Example: aaa**ooo will match aaapotato2000/beeeee/llllll/sdsdooo
- custom regex via {}. Example: aaa{12(34|56|78)oo(aa|bb|dd)ii}888 will match aaa1256oobbii888
This means you can use \} to pass } to regex and \\ to pass \ to regex

"""
import os
import re


def normalize_path(path, sep=os.path.sep):
    path = path.replace(sep, '/')

    while path.startswith('./'):
        path = path[2:]

    if path[-1] == '/':
        path = path[:-1]

    return path


def convert_pattern(pat):
    if not pat or pat[0] == '#' or pat == '/':
        return None

    ptr, n = 0, len(pat)
    regex = '^'
    void = False  # wow I can use this name, finally :O
    negate = False

    if pat[ptr] == '!':
        negate = True
        ptr += 1

    # cut trailing spaces, sophisticated approach :)
    ptr2 = n - 1
    while pat[ptr2] == ' ':
        num_backslashes = 0
        ptr3 = ptr2 - 1

        while ptr3 >= 0 and pat[ptr3] == '\\':
            num_backslashes += 1
            ptr3 -= 1

        if not num_backslashes % 2:
            ptr2 -= 1
        else:
            break

    pat = pat[:ptr2 + 1]

    dironly = pat[-1] == '/'
    if (dironly):
        pat = pat[:-1]

    n = len(pat)

    # because if it ends with a slash and doesn't contain any other ones, it's
    # still for any directory
    if not '/' in pat[:-1]:
        regex += '(?:.+/)?'

    # cut the **/
    # we just didn't want that regex above, but didn't want this slash either
    if pat[ptr] == '/':
        ptr += 1

    while ptr < n:
        if void:
            regex += re.escape(pat[ptr])
            void = False

        elif pat[ptr] == '\\':
            ptr += 1
            void = True

        elif pat[ptr] == '*':
            # ** means anything, .*
            if not ptr == n - 1 and pat[ptr + 1] == '*':
                # **/ can also match nothing
                if not ptr == n - 2 and pat[ptr + 2] == '/':
                    regex += '(?:.+/)?'
                    ptr += 3
                else:
                    regex += '.*'
                    ptr += 2
            else:
                regex += '[^/]*'
                ptr += 1

        elif pat[ptr] == '?':
            regex += '[^/]'
            ptr += 1

        elif pat[ptr] == '[':
            ptr2 = ptr + 1

            if ptr2 < n and pat[ptr2] == '!':
                ptr2 += 1

            if ptr2 < n and pat[ptr2] == ']':
                ptr2 += 1

            while ptr < n and pat[ptr2] != ']':
                ptr2 += 1

            if ptr2 < n:
                ptr2 += 1
                regex += '['

                if pat[ptr + 1] == '!':
                    regex += '^'
                    ptr += 1
                elif pat[ptr + 1] == '^':
                    regex += '\\^'
                    ptr += 1

                regex += pat[ptr + 1:ptr2].replace('\\', '\\\\')

                ptr = ptr2
            else:
                regex += '\\['
                ptr += 1

        # powerful and easy... idk why the [ stuff even exists.
        elif pat[ptr] == '{':
            ptr2 = ptr + 1
            escape2 = False

            while ptr2 < n:
                if escape2:
                    # so \\ is \ in regex not \\. example => aaa{asas\\n\}fgfg}
                    regex += pat[ptr2]
                    escape2 = False
                    ptr2 += 1
                elif pat[ptr2] == '\\':
                    escape2 = True
                    ptr2 += 1
                elif pat[ptr2] == '}':
                    ptr2 += 1
                    break
                else:
                    regex += pat[ptr2]
                    ptr2 += 1

            # now ptr2 points to the thing after }
            ptr = ptr2

        else:
            regex += re.escape(pat[ptr])
            ptr += 1

    regex += '$'

    return regex, dironly, negate


class ZgitIgnore():

    def __init__(self, lines=None, ignore_case=False):
        self.lines = lines
        self.ignore_case = ignore_case
        self.patterns = []  # order is important

        if lines:
            self.add_patterns(lines)

    def add_patterns(self, lines):
        for line in lines:
            pattern = convert_pattern(line)
            if pattern:
                self.patterns.append(pattern)

    def is_ignored(self, what, is_directory=False):
        what = normalize_path(what)

        ignored = False

        for pattern, directory_only, negated in self.patterns:
            if (not directory_only or is_directory) and re.match(
                    pattern, what, re.DOTALL | (re.IGNORECASE if self.ignore_case else 0)):
                ignored = not negated

        return ignored
