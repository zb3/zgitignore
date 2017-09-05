import unittest
import zgitignore
import re


class ZgitIgnoreTest(unittest.TestCase):
  def test_normalize(self):
    self.assertEqual(zgitignore.normalize_path('./ert/dr/td/t'), 'ert/dr/td/t')
    self.assertEqual(zgitignore.normalize_path('ert/dr/td/t'), 'ert/dr/td/t')
    self.assertEqual(zgitignore.normalize_path('.\\alb\\dld', sep='\\'), 'alb/dld')
    self.assertEqual(zgitignore.normalize_path('/foo/fighters', sep='/'), 'foo/fighters')


  def test_convert_negate(self):
    pat, dir, negate = zgitignore.convert_pattern('!a')
    self.assertEqual(negate, True)

    pat, dir, negate = zgitignore.convert_pattern('a')
    self.assertEqual(negate, False)

    pat, dir, negate = zgitignore.convert_pattern('\\!a')
    self.assertEqual(negate, False)


  def test_convert_spaces(self):
    pat, dir, negate = zgitignore.convert_pattern('aaaaaa      ')
    self.assertEqual('\\ \\ \\ \\ \\ \\ ' in pat, False)
    
    pat, dir, negate = zgitignore.convert_pattern('aaaaaa     \\ ')
    self.assertEqual('\\ \\ \\ \\ \\ \\ ' in pat, True)

    pat, dir, negate = zgitignore.convert_pattern('aaaaaa     \\\\ ')
    self.assertEqual('\\ \\ \\ \\ \\ \\ ' in pat, False)
    self.assertEqual('\\ \\ \\ \\ \\ ' in pat, True)

  def test_convert_escapes(self):
    pat, dir, negate = zgitignore.convert_pattern('\\!important')
    self.assertEqual(pat, '^(?:.+/)?\\!important$')

    pat, dir, negate = zgitignore.convert_pattern('\\#test#')
    self.assertEqual(pat, '^(?:.+/)?\\#test\\#$')

    pat, dir, negate = zgitignore.convert_pattern('g\\zzzzz\\gzzzzz')
    self.assertEqual(pat, '^(?:.+/)?gzzzzzgzzzzz$')

    pat, dir, negate = zgitignore.convert_pattern('a\\{[0-9]{3,6\\}}|')
    self.assertEqual(pat, '^(?:.+/)?a\\{[0-9]3,6}\\|$')

  def test_convert_slash(self):
    pat, dir, negate = zgitignore.convert_pattern('lolo/rosso')
    self.assertEqual(pat.startswith('^(?:'), False)

    pat, dir, negate = zgitignore.convert_pattern('lolo/')
    self.assertEqual(pat.startswith('^(?:'), True)

    pat, dir, negate = zgitignore.convert_pattern('lolo/rosso/**')
    self.assertEqual(pat.startswith('^(?:'), False)

    pat, dir, negate = zgitignore.convert_pattern('/rosso')
    self.assertEqual(pat.startswith('^(?:'), False)


  def test_convert(self):
    pat, dir, negate = zgitignore.convert_pattern('lolo/')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('lolo/rosso')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('lolo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('wolo/lolo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('lolo/')))

    pat, dir, negate = zgitignore.convert_pattern('*lolo')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('lolo/')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('ugabuga/folor/lolo')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('w/r/lolos')))

    pat, dir, negate = zgitignore.convert_pattern('po*lolo')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('pololo')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('po/wa/wo/lolo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('ugabuga/polorewrlolo')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('pololo5')))

    pat, dir, negate = zgitignore.convert_pattern('po\\*lolo')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('pololo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('po*lolo')))

    pat, dir, negate = zgitignore.convert_pattern('hopsasa/dolasa')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('hopsasa/dolasaf')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('ooo/hopsasa/dolasa')))

    pat, dir, negate = zgitignore.convert_pattern('/hopsasa')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('booga/hopsasa')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('hopsasa')))

    pat, dir, negate = zgitignore.convert_pattern('*/hopsasa/dolasa')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('ooo/hopsasa/dolasa')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('ooo/woo/hopsasa/dolasa')))

    pat, dir, negate = zgitignore.convert_pattern('**/hopsasa/dolasa')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('ooo/hopsasa/dolasa')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('ooo/woo/hopsasa/dolasa')))

    pat, dir, negate = zgitignore.convert_pattern('aaa/**/bee')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('aaa/bee')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('aaa/x/bee')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('aaa/b/d/d/bee')))

    pat, dir, negate = zgitignore.convert_pattern('aaa/**')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('aaa')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('aaa/b/d/d/bee')))

    pat, dir, negate = zgitignore.convert_pattern('aaa**')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('aaa')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('aaa/b/d/d/bee')))


  def test_convert_from_gitignore(self): #stolen from gitignore manual
    pat, dir, negate = zgitignore.convert_pattern('Documentation/*.html')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('Documentation/git.html')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('Documentation/ppc/ppc.html')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('tools/perf/Documentation/perf.html')))

    pat, dir, negate = zgitignore.convert_pattern('/*.c')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('cat-file.c')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('mozilla-sha1/sha1.c')))

    pat, dir, negate = zgitignore.convert_pattern('**/foo')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('s/ds/ds/foo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('foo/foo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('foo')))

    pat, dir, negate = zgitignore.convert_pattern('/**/foo')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('s/ds/ds/foo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('foo/foo')))
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('foo')))

    pat, dir, negate = zgitignore.convert_pattern('**/foo/bar')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('window/ogaboga/foo/bar')))

    pat, dir, negate = zgitignore.convert_pattern('/bar/**')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('bar/df/dfd/f')))
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('bar')))


  def test_convert_from_comments(self):
    pat, dir, negate = zgitignore.convert_pattern('*aaa')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('e/r/cf/x/s/bbbaaa')))

    pat, dir, negate = zgitignore.convert_pattern('*aaa/')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('e/r/cf/x/s/bbbaaa')))

    pat, dir, negate = zgitignore.convert_pattern('*aaa/cf')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('asasas/baaa/cf')))

    pat, dir, negate = zgitignore.convert_pattern('*/lol.mw')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('lol.mw')))

    pat, dir, negate = zgitignore.convert_pattern('a*n/wat')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('an/wat')))

    pat, dir, negate = zgitignore.convert_pattern('a*n')
    self.assertIsNotNone(re.search(pat, zgitignore.normalize_path('an')))

    pat, dir, negate = zgitignore.convert_pattern('/*/foo')
    self.assertIsNone(re.search(pat, zgitignore.normalize_path('foo')))

  def test_convert_brackets(self):
    pat, dir, negate = zgitignore.convert_pattern('a[]]|')
    self.assertEqual(pat, '^(?:.+/)?a[]]\\|$')
    pat, dir, negate = zgitignore.convert_pattern('a[d]|')
    self.assertEqual(pat, '^(?:.+/)?a[d]\\|$')
    pat, dir, negate = zgitignore.convert_pattern('a[!a]|')
    self.assertEqual(pat, '^(?:.+/)?a[^a]\\|$')
    pat, dir, negate = zgitignore.convert_pattern('a[a-z]|')
    self.assertEqual(pat, '^(?:.+/)?a[a-z]\\|$')
    pat, dir, negate = zgitignore.convert_pattern('a[!o-q]|')
    self.assertEqual(pat, '^(?:.+/)?a[^o-q]\\|$')


  def test_convert_power_regex(self):
    pat, dir, negate = zgitignore.convert_pattern('a{[0-9]{3,6\\}}|')
    self.assertEqual(pat, '^(?:.+/)?a[0-9]{3,6}\\|$')
    pat, dir, negate = zgitignore.convert_pattern('a{\\\\n}|')
    self.assertEqual(pat, '^(?:.+/)?a\\n\\|$')
    pat, dir, negate = zgitignore.convert_pattern('a{(oga|boga)}|')
    self.assertEqual(pat, '^(?:.+/)?a(oga|boga)\\|$')


  def test_class_basic(self):
    test1 = zgitignore.ZgitIgnore(['build/', 'wow*fg'])
    self.assertEqual(test1.is_ignored('ogaboga'), False)
    self.assertEqual(test1.is_ignored('oo/build'), False)
    self.assertEqual(test1.is_ignored('oo/build', True), True)
    test1.add_patterns(['*woul[d]\\[p1r4t3]*'])
    self.assertEqual(test1.is_ignored('would[p1r4t3].mp3'), True)

    test2 = zgitignore.ZgitIgnore(['!exclude', 'exclude', '!exclude'])
    self.assertEqual(test2.is_ignored('exclude'), False)

    test3 = zgitignore.ZgitIgnore(['exclude', '!exclude', 'exclude'])
    self.assertEqual(test3.is_ignored('exclude'), True)

    test4 = zgitignore.ZgitIgnore(['\\#test#', '\\!important'])
    self.assertEqual(test4.is_ignored('#test#'), True)
    self.assertEqual(test4.is_ignored('!important'), True)


  def test_class_case(self):
    test1 = zgitignore.ZgitIgnore(['*readme*'])
    self.assertEqual(test1.is_ignored('readme.txt'), True)
    self.assertEqual(test1.is_ignored('README.rst'), False)

    test2 = zgitignore.ZgitIgnore(['*readme*'], True)
    self.assertEqual(test2.is_ignored('readme.txt'), True)
    self.assertEqual(test2.is_ignored('README.rst'), True)

  def test_class_power(self):
    test1 = zgitignore.ZgitIgnore(['testcolor{#[a-f0-9]{3,6\\}}.test'], True)
    self.assertEqual(test1.is_ignored('testcolor#00ffff.test'), True)
    self.assertEqual(test1.is_ignored('testcolor#FFF.test'), True)
    self.assertEqual(test1.is_ignored('testcolor#4.test'), False)
    self.assertEqual(test1.is_ignored('testcolor#04zzzz.test'), False)

  def test_docker(self):
    pat, dir, negate = zgitignore.convert_pattern('test', docker=True)
    self.assertEqual(pat, '^test$')

    pat, dir, negate = zgitignore.convert_pattern('!test', docker=True)
    self.assertEqual(pat, '^test$')


if __name__ == '__main__':
    unittest.main()
