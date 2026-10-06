from __future__ import annotations
import importlib.util,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(name):
    p=ROOT/'scripts'/f'{name}.py'; s=importlib.util.spec_from_file_location(name,p); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
jsonc=load('validate_jsonc'); skill=load('check_skill'); ext=load('validate_extension')
class Tests(unittest.TestCase):
    def test_jsonc_comments_and_trailing_commas(self):
        raw='{// c\n"url":"https://example.com/a/*b*/", "a":[1,2,], /*x*/}'
        self.assertEqual(jsonc.json.loads(jsonc.strip_jsonc(raw))['a'],[1,2])
    def test_jsonc_unterminated_comment(self):
        with self.assertRaises(ValueError): jsonc.strip_jsonc('{/*')
    def test_invalid_json_fails_main(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json'; p.write_text('{bad}')
            self.assertEqual(jsonc.main([str(p)]),1)
    def test_this_skill(self):
        errors,_=skill.check(ROOT); self.assertEqual(errors,[])
    def test_missing_manifest(self):
        with tempfile.TemporaryDirectory() as d: self.assertIn('missing extension.toml',ext.check(Path(d))[0])
    def test_api_placeholder(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)
            (p/'extension.toml').write_text('id="ok-id"\nname="Okay"\nversion="0.0.1"\nschema_version=1\nauthors=["A"]\ndescription="D"\nrepository="https://example.com"\n[language_servers.x]\nname="X"\nlanguages=["X"]\n')
            (p/'LICENSE').write_text('test')
            (p/'Cargo.toml').write_text('[package]\nname="x"\nversion="0.0.1"\n[dependencies]\nzed_extension_api="<latest>"\n')
            errors,_=ext.check(p); self.assertTrue(any('placeholder' in x for x in errors))
if __name__=='__main__': unittest.main()
