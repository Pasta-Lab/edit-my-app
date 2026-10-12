"""Offline maintainer checks; Python is not needed by the installers."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/edit-my-app'
FILES = ['SKILL.md', 'references/workflow.md', 'references/tools.md',
         'references/macos.md', 'references/ios.md', 'references/windows.md',
         'references/linux.md', 'references/android.md', 'LICENSE']
MARKDOWN_FILES = ['README.md', 'INSTALL.md', 'AGENTS.md'] + [
    'skills/edit-my-app/' + name for name in FILES if name.endswith('.md')]


class PackageTests(unittest.TestCase):
    def test_package_shape(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertTrue(text.startswith('---\nname: edit-my-app\n'))
        self.assertIn('description:', text.split('---', 2)[1])
        self.assertLess(len(text.split()), 900)
        self.assertEqual({p.relative_to(SKILL).as_posix() for p in SKILL.rglob('*') if p.is_file()},
                         set(FILES))
        self.assertEqual((SKILL / 'LICENSE').read_bytes(), (ROOT / 'LICENSE').read_bytes())
        plugin = json.loads((ROOT / 'plugin.json').read_text())
        self.assertEqual(plugin['name'], 'edit-my-app')
        self.assertEqual(plugin['license'], 'MIT')
        self.assertNotIn('hooks', plugin)
        self.assertNotIn('mcpServers', plugin)
        # Five platform catalogs and shared references still fit in 64 KiB of text.
        self.assertLess(sum(p.stat().st_size for p in SKILL.rglob('*') if p.is_file()), 64 * 1024)

    def test_local_markdown_links(self):
        for relative_path in MARKDOWN_FILES:
            document = ROOT / relative_path
            for link in re.findall(r'\]\(([^)]+)\)', document.read_text()):
                if '://' in link or link.startswith('#'):
                    continue
                target = (document.parent / link.split('#')[0]).resolve()
                self.assertTrue(target.is_relative_to(ROOT), f'Escaping link in {document}: {link}')
                self.assertTrue(target.exists(), f'Broken link in {document}: {link}')

    def test_platform_routing_and_status(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertIn('one target-platform', text)
        for target in ('macos', 'ios', 'windows', 'linux', 'android'):
            self.assertIn(f'references/{target}.md', text)
        for target in ('ios', 'windows', 'linux', 'android'):
            self.assertIn('unverified', (SKILL / f'references/{target}.md').read_text().splitlines()[0])
        self.assertIn('MyPreview', (SKILL / 'references/macos.md').read_text())

    def test_installer_allowlists_match(self):
        for installer in ('install.sh', 'install.ps1'):
            text = (ROOT / installer).read_text()
            for name in FILES:
                self.assertIn(name, text, f'{installer} omits {name}')
        subprocess.run(['bash', '-n', str(ROOT / 'install.sh')], check=True)

    def test_platform_tool_catalogs(self):
        format_tools = {'macos': 'macholib', 'ios': 'macholib', 'windows': 'pefile',
                        'linux': 'pyelftools', 'android': 'Androguard'}
        for target, format_tool in format_tools.items():
            text = (SKILL / f'references/{target}.md').read_text()
            catalog = text.split('## Tools for this target', 1)[1].split('\n## ', 1)[0]
            self.assertIn('[Ghidra](https://github.com/NationalSecurityAgency/ghidra)', catalog)
            self.assertIn('[Capstone](https://www.capstone-engine.org/)', catalog)
            self.assertIn(format_tool, catalog)
            self.assertIn('tools.md#python-packages', catalog)

    def test_python_package_catalog(self):
        text = (SKILL / 'references/tools.md').read_text()
        for package in ('capstone', 'keystone-engine', 'unicorn', 'lief', 'pyghidra',
                        'macholib', 'pyelftools', 'pefile', 'dnfile', 'dncil',
                        'androguard', 'angr', 'construct', 'yara-python'):
            self.assertIn(f'`{package}`', text)
        self.assertIn('<tools-dir>/python/<environment-name>/', text)
        self.assertIn('not a bulk `pip install` command', text)

    def test_readme_status_permissions_and_style(self):
        text = (ROOT / 'README.md').read_text()
        self.assertIn('| [macOS](skills/edit-my-app/references/macos.md) | Verified |', text)
        self.assertIn('Only macOS has been verified so far.', text)
        self.assertIn('## Permissions', text)
        self.assertIn('administrator approval', text)
        self.assertLessEqual(len(text.split()), 400)
        # Keep required syntax in commands, URLs, the skill name, and table rules.
        prose = re.sub(r'```[\s\S]*?```', '', text)
        prose = re.sub(r'\]\([^)]+\)', ']', prose)
        prose = re.sub(r'^\|[ |:-]+\|$', '', prose, flags=re.MULTILINE)
        prose = prose.replace('edit-my-app', '')
        self.assertNotRegex(prose, r'[;\u2013\u2014-]')


class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='edit-my-app-test-')
        self.directory = Path(self.temporary.name).resolve()
        self.parent = self.directory / 'skills with spaces'

    def tearDown(self):
        self.temporary.cleanup()

    def install(self, *args, source=ROOT):
        return subprocess.run(['bash', str(ROOT / 'install.sh'), '--source', str(source),
                               '--dest', str(self.parent), *args],
                              text=True, capture_output=True, timeout=20)

    def test_offline_install_and_no_overwrite(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stderr)
        target = self.parent / 'edit-my-app'
        self.assertEqual({p.relative_to(target).as_posix() for p in target.rglob('*') if p.is_file()}, set(FILES))
        for name in FILES:
            source = SKILL / name
            self.assertEqual((target / name).read_bytes(), source.read_bytes())
        # An existing installation, including user modifications, is never replaced.
        sentinel = target / 'user-note.txt'
        sentinel.write_text('Leave this alone.')
        previous = {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob('*') if p.is_file()}
        again = self.install()
        self.assertEqual(again.returncode, 0, again.stderr)
        self.assertIn('left untouched', again.stdout)
        self.assertEqual(previous, {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob('*') if p.is_file()})
        self.assertEqual(list(self.parent.iterdir()), [target])

    def test_claude_and_custom_destination(self):
        result = self.install('--agent', 'claude')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.parent / 'edit-my-app/SKILL.md').exists())

    def test_invalid_arguments_are_nonmutating(self):
        for args in (('--agent', 'unknown'), ('--dest', 'relative'), ('--dest', '/'), ('--unknown',), ('--dest',)):
            result = self.install(*args)
            self.assertNotEqual(result.returncode, 0, args)
            self.assertFalse(self.parent.exists())

    def test_symlink_destination_refused(self):
        elsewhere = self.directory / 'elsewhere'
        elsewhere.mkdir()
        self.parent.mkdir()
        (self.parent / 'edit-my-app').symlink_to(elsewhere, target_is_directory=True)
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_symlink_parent_refused(self):
        elsewhere = self.directory / 'elsewhere'
        elsewhere.mkdir()
        self.parent.symlink_to(elsewhere, target_is_directory=True)
        self.assertNotEqual(self.install().returncode, 0)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_incomplete_source_does_not_leave_partial_skill(self):
        checkout = self.directory / 'incomplete-checkout'
        shutil.copytree(SKILL, checkout / 'skills/edit-my-app')
        (checkout / 'skills/edit-my-app/references/android.md').unlink()
        result = self.install(source=checkout)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.parent / 'edit-my-app').exists())
        self.assertEqual(list(self.parent.iterdir()), [])

    def test_lock_does_not_get_deleted_by_another_installer(self):
        lock = self.parent / '.edit-my-app-install.lock'
        lock.mkdir(parents=True)
        self.assertNotEqual(self.install().returncode, 0)
        self.assertTrue(lock.is_dir())
        self.assertEqual(list(self.parent.iterdir()), [lock])

    def remote_install(self, fail_at=''):
        # Exercise the public one-liner's stdin mode with a local curl stand-in.
        # No HTTP request, tool install, HOME override, or real agent mutation.
        mockbin = self.directory / 'mockbin'
        mockbin.mkdir()
        curl = mockbin / 'curl'
        curl.write_text('''#!/bin/bash
set -eu
source_file=''
destination=''
while [[ $# -gt 0 ]]; do
    case "$1" in
        https://raw.githubusercontent.com/Pasta-Lab/edit-my-app/main/*)
            source_file=${1#https://raw.githubusercontent.com/Pasta-Lab/edit-my-app/main/}; shift ;;
        --output) destination=$2; shift 2 ;;
        *) shift ;;
    esac
done
[[ -n "$source_file" && -n "$destination" ]] || exit 98
[[ "$source_file" != "${OMNIFORM_TEST_FAIL_AT:-}" ]] || exit 22
printf '%s\\n' "$source_file" >> "$OMNIFORM_TEST_LOG"
/bin/cp "$OMNIFORM_TEST_SOURCE/$source_file" "$destination"
''')
        curl.chmod(0o700)
        environment = dict(os.environ, PATH=str(mockbin) + os.pathsep + os.environ['PATH'],
                           OMNIFORM_TEST_SOURCE=str(ROOT), OMNIFORM_TEST_LOG=str(self.directory / 'fetches'),
                           OMNIFORM_TEST_FAIL_AT=fail_at)
        return subprocess.run(['bash', '-s', '--', '--dest', str(self.parent)],
                              input=(ROOT / 'install.sh').read_text(), env=environment,
                              text=True, capture_output=True, timeout=20)

    def test_piped_install_downloads_only_instruction_files(self):
        result = self.remote_install()
        self.assertEqual(result.returncode, 0, result.stderr)
        fetched = set((self.directory / 'fetches').read_text().splitlines())
        self.assertEqual(fetched, {'skills/edit-my-app/' + name for name in FILES})
        for name in FILES:
            source = SKILL / name
            self.assertEqual((self.parent / 'edit-my-app' / name).read_bytes(), source.read_bytes())

    def test_failed_download_leaves_no_partial_install(self):
        result = self.remote_install(fail_at='skills/edit-my-app/references/android.md')
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(list(self.parent.iterdir()), [])


if __name__ == '__main__':
    unittest.main(verbosity=2)
