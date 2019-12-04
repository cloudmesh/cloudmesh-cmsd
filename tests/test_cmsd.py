###############################################################
# pytest -v --capture=no tests/test_cmsd.py
# pytest -v  tests/test_cmsd.py
# pytest -v --capture=no  tests/test_cmsd.py:Test_cmsd.<METHIDNAME>
###############################################################
import pytest
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common3.Benchmark import Benchmark
Benchmark.debug()


@pytest.mark.incremental
class TestCmsd:

    def test_help(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_version(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd version", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_update(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd update", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result


    def test_setup(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd setup", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "['sample1', 'sample2', 'sample3', 'sample18']" in result

    def test_clean(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd clean", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "['sample1', 'sample2', 'sample3', 'sample18']" in result

    def test_benchmark(self):
        Benchmark.print()
