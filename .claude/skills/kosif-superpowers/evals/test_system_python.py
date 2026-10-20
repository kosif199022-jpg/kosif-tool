"""Deterministic tests for architecture sizing and Python package metadata inspection."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch

SCRIPTS=Path(__file__).resolve().parents[1]/"scripts"


def from_file(module_name, file):
    spec=importlib.util.spec_from_file_location(module_name,SCRIPTS/file)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


sizer=from_file("architecture_sizer","architecture_sizer.py")
python_probe=from_file("python_package_probe","python_package_probe.py")


class ArchitectureSizerTests(unittest.TestCase):
    def base(self, **changes):
        d={"daily_requests":86400,"peak_factor":5,"payload_bytes":1000,
           "retention_days":7,"replica_rps":100,"target_utilization":"0.5","copies":2}
        d.update(changes)
        return sizer.size_system(**d)

    def test_exact_integer_sizing(self):
        v=self.base()
        self.assertEqual(v["average_rps"],"1.000000")
        self.assertEqual(v["peak_rps"],"5.000000")
        self.assertEqual(v["minimum_replicas"],1)
        self.assertEqual(v["logical_storage_bytes"],604800000)
        self.assertEqual(v["retained_storage_bytes"],1209600000)
        self.assertFalse(v["executed_benchmark"])

    def test_replica_ceil(self):
        a=self.base(peak_factor=120)
        self.assertEqual(a["minimum_replicas"],3)

    def test_replication_affects_storage_not_rps(self):
        a=self.base(copies=1)
        b=self.base(copies=3)
        self.assertEqual(a["minimum_replicas"],b["minimum_replicas"])
        self.assertEqual(b["retained_storage_bytes"],3*a["retained_storage_bytes"])

    def test_decimal_inputs_are_deterministic(self):
        self.assertEqual(self.base()["retained_storage_bytes"],
                         self.base(daily_requests="86400",payload_bytes="1000")["retained_storage_bytes"])

    def test_peak_factor_cannot_be_below_one(self):
        with self.assertRaises(ValueError):
            self.base(peak_factor="0.9")

    def test_utilization_constraints(self):
        for x in ("0","1.1","NaN","Infinity"):
            with self.subTest(value=x),self.assertRaises(ValueError):
                self.base(target_utilization=x)

    def test_input_zero_and_negative_rejected(self):
        for x in ("0","-1"):
            with self.subTest(value=x),self.assertRaises(ValueError):
                self.base(daily_requests=x)

    def test_copies_must_be_positive_integer(self):
        for x in ("0","1.5","-2"):
            with self.subTest(value=x),self.assertRaises(ValueError):
                self.base(copies=x)

    def test_copies_accepts_integral_decimal(self):
        self.assertEqual(self.base(copies="2")["inputs"]["copies"],2)
        self.assertEqual(self.base(copies="3.0")["inputs"]["copies"],3)

    def test_exclusions_match_docstring(self):
        v=self.base()
        for item in ("database indexes","caching","backups","compression","network"):
            self.assertIn(item,v["exclusions"])

    def test_cli_non_integer_copies_is_clean_error(self):
        for x in ("1.5","two"):
            with self.subTest(value=x):
                run=subprocess.run([sys.executable,str(SCRIPTS/"architecture_sizer.py"),
                                    "--daily-requests","86400","--peak-factor","5",
                                    "--payload-bytes","1000","--retention-days","7",
                                    "--replica-rps","100","--target-utilization","0.5",
                                    "--copies",x],capture_output=True,text=True,timeout=10)
                self.assertEqual(run.returncode,2)
                self.assertIn("copies must be a positive integer",run.stderr)
                self.assertNotIn("invalid literal",run.stderr)

    def test_cli_does_not_guess_missing_inputs(self):
        run=subprocess.run([sys.executable,str(SCRIPTS/"architecture_sizer.py"),
                            "--daily-requests","100"],capture_output=True,text=True,timeout=5)
        self.assertNotEqual(run.returncode,0)


class PythonProbeTests(unittest.TestCase):
    def test_installed_distribution_is_not_executed(self):
        with patch.object(python_probe.metadata,"version",return_value="1.2.3") as metadata_version:
            x=python_probe.probe(["numpy"])
        self.assertEqual(metadata_version.call_count,1)
        self.assertEqual(x["packages"][0]["status"],"distribution_metadata_found")
        self.assertEqual(x["packages"][0]["version"],"1.2.3")
        self.assertFalse(x["packages"][0]["execution_tested"])
        self.assertFalse(x["packages"][0]["ready_for_production"])

    def test_missing_package_is_not_claimed(self):
        with patch.object(python_probe.metadata,"version",
                          side_effect=python_probe.metadata.PackageNotFoundError):
            x=python_probe.probe(["missing_dist"])
        self.assertEqual(x["packages"][0]["status"],"not_found_in_environment")
        self.assertIsNone(x["packages"][0]["version"])

    def test_rejects_command_injection_strings(self):
        for x in ("requests; rm -rf x","foo/bar","../pkg","a\nb",""):
            with self.subTest(value=x),self.assertRaises(ValueError):
                python_probe.probe([x])

    def test_deduplicates_normalized_names(self):
        with patch.object(python_probe.metadata,"version",return_value="0.1") as metadata_version:
            x=python_probe.probe(["import-lib","import_lib","Import.Lib"])
        self.assertEqual(len(x["packages"]),1)
        self.assertEqual(metadata_version.call_count,1)

    def test_max_packages_limit(self):
        with self.assertRaises(ValueError):
            python_probe.probe(["p"+str(i) for i in range(51)])

    def test_cli_read_only_json(self):
        x=subprocess.run([sys.executable,str(SCRIPTS/"python_package_probe.py"),
                          "totally_nonexistent_kosif_probe_dist"],capture_output=True,
                         text=True,timeout=5)
        self.assertEqual(x.returncode,0,x.stderr)
        data=json.loads(x.stdout)
        self.assertEqual(data["packages"][0]["status"],"not_found_in_environment")
        self.assertEqual(data["scope"],"current_environment_only_no_install_no_network")


if __name__=="__main__":
    unittest.main()
