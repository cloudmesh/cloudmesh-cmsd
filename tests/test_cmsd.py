###############################################################
# pytest -v --capture=no tests/test_cmsd.py
# pytest -v  tests/test_cmsd.py
# pytest -v --capture=no  tests/test_cmsd.py::Test_cmsd::<METHODNAME>
# pytest -v --capture=no  tests/test_cmsd.py::TestCmsd::test_vm_list_json
###############################################################
import pytest
from cloudmesh.common.StopWatch import StopWatch
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING
from cloudmesh.common.Benchmark import Benchmark
Benchmark.debug()


@pytest.mark.incremental
class TestCmsd:

    def test_help(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd --help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_version(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd --version", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_update(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd --update", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result


    def test_setup(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd --setup", shell=True)
        Benchmark.Stop()
        VERBOSE(result)
        raise NotImplementedError
        assert "not implemented" in result

    def test_clean(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd --clean", shell=True)
        Benchmark.Stop()
        VERBOSE(result)
        raise NotImplementedError

        assert "not implemented" in result

    def test_cms_command(self):
        HEADING()
        # commands = (command, asserion_text)*
        commands = [("help", "NOT IMPLEMENTED")
                    ("version", "NOT IMPLEMENTED")]

        for c, txt in commands:
            command = "cmsd " + c
            StopWatch.start(command)
            result = Shell.execute("cmsd help", shell=True)
            StopWatch.start(command)
            Benchmark.Stop()

            assert txt in result

    def test_vm_list_json(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd vm list --refresh --output=json", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert result.endswith("}")

    def test_benchmark(self):
        Benchmark.print()
