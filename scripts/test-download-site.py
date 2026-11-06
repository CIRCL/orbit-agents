"""Offline package metadata and shared-style integration checks."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC=importlib.util.spec_from_file_location('downloads',Path(__file__).with_name('build-download-site.py'))
BUILD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(BUILD)


class DownloadSiteTests(unittest.TestCase):
    def test_native_page_keeps_real_package_targets_and_adds_the_pano_backlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            for suffix in ('pkg','msi','deb'):(root/('example.'+suffix)).write_bytes(b'example')
            BUILD.build(root);page=(root/'index.html').read_text()
            for suffix in ('pkg','msi','deb'):self.assertIn('href="example.'+suffix+'" download',page)
            self.assertIn('--navy:#132f3c',page)
            self.assertIn('href="https://mon01.srv.office.lhc.lu/pano/" target="_blank" rel="noopener noreferrer"',page)
            self.assertEqual(len((root/'SHA256SUMS').read_text().splitlines()),3)
            self.assertNotIn('${pano_tokens}',page)
            self.assertNotIn('${pano_theme}',page)
            self.assertIn('prefers-color-scheme:dark',page)
            self.assertIn((Path(__file__).resolve().parents[1]/'assets/pano-ui/0.2.0/theme.js').read_text(),page)

    def test_missing_installer_still_fails_before_publishing_a_page(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            with self.assertRaises(ValueError):BUILD.build(root)
            self.assertFalse((root/'index.html').exists())


if __name__=='__main__':unittest.main()
