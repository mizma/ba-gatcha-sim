ba-gatcha-sim
========================================================================

BlueArchive gatcha monte-carlo simulation

Installation
------------------------------------------------------------------------

~~~shell
> pipx install git+https://github.com/mizma/ba-gatcha-sim.git
~~~

Usage
------------------------------------------------------------------------

Command Line tool description

~~~shell
> basim -n -o -t 2 -c 100000 > result.csv
~~~

* `-o, --old`
  * run old gatcha sim
* `-r, --reset`
  * reset old count after 2 PU pull
* `-n, --new`
  * run new gatcha sim
* `-t, --target <tgt>`
  * simulate up to target pickup count
* `-c, --cycles <cyc>`
  * number of cycles to simulate
* `-C, --count <cnt>`
  * initial count for new gatcha
* `-v, --verbose`
  * output in verbose mode
* `--version`
  * Show the version and exit.
* `--help`
  * Show this message and exit.

Known Issues
------------------------------------------------------------------------

None at the moment

Development
------------------------------------------------------------------------

### Building an Executable

Install pyinstaller and package the project.
May want to use venv when executing the pyinstaller.

First, enter venv and install the local package and pyinstaller

~~~shell
>. .venv/Scripts/activate
(.venv) >pip install .
Processing /path/to/proj/ba-gatcha-sim
~snip~
Installing collected packages: ba_gatcha_sim
    Running setup.py install for ba_gatcha_sim ... done
Successfully installed ba_gatcha_sim-0.1.0

(.venv) >pip install pyinstaller
~snip~
Successfully installed pyinstaller-3.6
~~~

Use pyinstaller to build the exe file.

~~~shell
(.venv) >pyinstaller ba_gatcha_sim\cli.py --onefile --name basim
~snip~
13691 INFO: Building EXE from EXE-00.toc completed successfully.
~~~

Executable should be ready in dist/basim.exe

### Versioning

The project will follow the [semver2.0](http://semver.org/) versioning scheme.
With initial development phase starting at 0.1.0 and increasing
minor/patch versions until we deploy the tool to production
(and reach 1.0.0).
The interface relevant to versioning is whatever defined in this
document's "Usage" section (includes all (sub)commands, and their cli arguments.

