zgitignore
==========
zgitignore is a small library to check if a file has been excluded by a ``.zgitignore`` file (those are compatible with ``.gitignore`` / ``.dockerignore`` files).


Installation
------------

As simple as it can be via pip::

    $ pip install zgitignore

Or direct installation from source::

    $ git clone git://github.com/zb3/zgitignore.git
    $ cd zgitignore
    $ python setup.py install


Usage
-----

.. code:: python

    import zgitignore

    # ZgitIgnore class stores the patterns, optionally takes two parameters: ignore_case and docker
    # by default, it is case sensitive to match .gitignore behaviour
    # for .dockerignore compatibility, use docker=True
    f = zgitignore.ZgitIgnore(['build/', 'dist/', '*egg-info'])

    # Patterns ending with / will match folders only:
    print('build file ignored?: ', f.is_ignored('build')) # False

    # When matching directories, set second parameter to True:
    print('build folder ignored?: ', f.is_ignored('build', True)) # True

    # It is case sensitive by default:
    print('BUILD folder ignored?: ', f.is_ignored('BUILD', True)) # False

    # Want it to be case-insensitive? No problem
    f = zgitignore.ZgitIgnore(['*pycache*', '*pyc'], True) # second parameter is ignore_case
    
    print('PYCACHE file ignored?', f.is_ignored('PYCACHE')) # True

    # You can also add patterns later
    ignorefile = zgitignore.ZgitIgnore(ignore_case=True, docker=True) # this is compatible with .dockerignore files
  
    try:
        with open('.gitignore', 'r') as f:
            ignorefile.add_patterns(f.read().splitlines())
    except:
        pass

    # You can start paths with ./ or not.
    # Paths are normalized to match Unix style paths
    print('./a/b/c/d/e ignored?', ignorefile.is_ignored('./a/b/c/d/e'))

    # But by default, parent directories aren't checked recursively
    # To check them, use check_parents=True
    f = zgitignore.ZgitIgnore(['build/'])
    
    print('build/test ignored?', f.is_ignored('build/test')) # False
    print('build/test ignored when check_parents=True?', f.is_ignored('build/test', check_parents=True)) # True

Format
------
zgitignore supports format similar to ``.gitignore`` file format. Differences are:


- ``**`` works everywhere
  ::

    ``aaa**ooo``

  Will match ``aaapotato2000/beeeee/llllll/sdsdooo``
- It can embed custom regex via ``{}``. You can use ``\}`` to pass ``}`` to regex and ``\\`` to pass ``\`` to regex
  ::

    aaa{12(34|56|78)oo(aa|bb|dd)ii}888

  Will match ``aaa1256oobbii888``
  ::

    aaa{#[0-9a-f]{3,6\}}888

  Will match ``aaa#00ffff888``
