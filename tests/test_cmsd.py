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
from cloudmesh.common.util import readfile
from cloudmesh.common.Benchmark import Benchmark
Benchmark.debug()


@pytest.mark.incremental
class TestCmsd:

    def test_setup(self):
        HEADING()

        print("WARNING: this will take quite a while ...")
        print()

        Benchmark.Start()
        result = Shell.execute("cmsd --setup", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert  "cloudmesh-mongo container running!" in result
        Benchmark.Status(True)

    def test_version(self):
        HEADING()

        version = readfile("VERSION")
        Benchmark.Start()
        result = Shell.execute("cmsd --version", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        msg = f"cmsd: {version}"
        print ("Version string to be tested:", msg)
        assert  msg in result
        Benchmark.Status(True)

    def exclude_test_update(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cmsd --update", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result
        Benchmark.Status(True)

    def test_banner_hello(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd banner hello", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "# hello" in result
        Benchmark.Status(True)

    """
    def test_vm_list_json_refresh(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd vm list --refresh --output=json", shell=True)
        Benchmark.Stop()
        # VERBOSE(result)

        assert result.endswith("}")
        Benchmark.Status(True)

    def test_vm_list_json(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd vm list --output=json", shell=True)
        Benchmark.Stop()
        # VERBOSE(result)

        assert result.endswith("}")
        Benchmark.Status(True)
    """

    def exclude_test_clean(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cmsd --clean", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "Removing volumes ..." in result
        assert "Removing temp dir" in result
        Benchmark.Status(True)


    def test_benchmark(self):
        Benchmark.print(sysinfo=True)
