This is the main repository of the [NOMAD](http://nomad-lab.eu) parser for
[BigDFT](http://bigdft.org/).

# Standalone Installation
The parser is designed to be usable as a separate python package. Here is an
example of the call syntax:

```python
    from bigdftparser import bigdftparser
    import matplotlib.pyplot as mpl

    # 0. Initialize a parser by giving a path to the BigDFT output file and a list of
    # default units
    path = "path/to/main.file"
    default_units = ["eV"]
    parser = bigdftparser(path, default_units=default_units)

    # 1. Parse
    results = parser.parse()

    # 2. Query the results with using the id's created specifically for NOMAD.
    scf_energies = results["energy_total_scf_iteration"]
    mpl.plot(scf_energies)
    mpl.show()
```

To install this standalone version, you need to first clone the
*git@gitlab.mpcdf.mpg.de:nomad-lab/python-common.git* repository and the
*git@gitlab.mpcdf.mpg.de:nomad-lab/nomad-meta-info.git* repository into the
same folder. Then install the *python-common* package according to the
instructions found in the README. After that, you can install this package by
running either of the following two commands depending on your python version:

```sh
python setup.py develop --user  # for python2
python3 setup.py develop --user # for python3
```

# Scala access
The scala layer in the Nomad infrastructure can access the parser functionality
through the scalainterface.py file, by calling the following command:

```python
    python scalainterface.py path/to/main/file
```

This scala interface is in it's own file to separate it from the rest of the
code.

# Support of different versions
The parser is designed to support multiple versions of BigDFT with a
[DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) approach: The
initial parser class is based on BigDFT 1.8.0, and other versions will be
subclassed from it. By sublassing, all the previous functionality will be
preserved, new functionality can be easily created, and old functionality
overridden only where necesssary.

# Developer Info
This section describes some of the guidelines that are used in the development
of this parser.

## Documentation
This parser tries to follow the [google style
guide](https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments)
for documenting python code. Documenting makes it much easier to follow the
logic behind your parser.

## Testing
The parsers can become quite complicated and maintaining them without
systematic testing is impossible. There are general tests that are
performed automatically in the scala layer for all parsers. This is essential,
but can only test that the data is outputted in the correct format and
according to some general rules. These tests cannot verify that the contents
are correct.

In order to truly test the parser output, regression testing is needed. The
tests for this parser are located in the **regtest** folder. Tests provide one
way to test each parseable quantity and python has a very good [library for
unit testing](https://docs.python.org/2/library/unittest.html). When the parser
supports a new quantity it is quite fast to create unit tests for it. These
tests will validate the parsing, and also easily detect bugs that may rise when
the code is modified in the future.

## Profiling
The parsers have to be reasonably fast. For some codes there is already
significant amount of data in the NoMaD repository and the time taken to parse
it will depend on the performance of the parser. Also each time the parser
evolves after system deployment, the existing data may have to be reparsed at
least partially.

By profiling what functions take the most computational time and memory during
parsing you can identify the bottlenecks in the parser. There are already
existing profiling tools such as
[cProfile](https://docs.python.org/2/library/profile.html#module-cProfile)
which you can plug into your scripts very easily.
