import unittest

from dep import extract_cdn_version, parse_content


class VersionTests(unittest.TestCase):
    def test_native_and_iris_keep_complete_versions(self):
        for version in ('4.5.3.135', '4.5.3.135-fav.1', '4.5.2.211.FAV',
                        '4.5.3.1.BASIC1', '4.7.0-dev.2', '4.5.3-build.1+customer.7'):
            for filename in (
                f'Agora_Native_SDK_for_Windows_rel.v{version}_33843_FAV_20261102_1517_1370937.zip',
                f'iris_{version}_DCG_Windows_Video_Standalone_20261102_1517_1.zip',
                f'AgoraRtcEngine_macOS_Preview_{version}.zip',
            ):
                with self.subTest(filename=filename):
                    self.assertEqual(extract_cdn_version('https://download.agora.io/old/1.2.3/' + filename), version)

    def test_all_platforms_use_same_version_extraction(self):
        for platform, output in (('Android', 'Android'), ('iOS', 'iOS'), ('Windows', 'Windows'),
                                 ('Mac', 'macOS'), ('Linux', 'Linux')):
            version = '4.5.3.135-fav.1'
            native = f'https://download.agora.io/sdk/Agora_Native_SDK_for_{platform}_rel.v{version}_1_FAV_20261102_1517_1.zip'
            iris = f'https://download.agora.io/sdk/iris_{version}_DCG_{platform}_Video_Standalone_20261102_1517_1.zip'
            row = next(r for r in parse_content(native + '\n' + iris) if r['platform'] == output)
            self.assertEqual(row['cdn'], [native])
            self.assertEqual(row['iris_cdn'], [iris])
            self.assertEqual((row['version'], row['iris_version']), (version, version))

    def test_compact_url_boundary_and_unknown_filename(self):
        urls = [f'https://download.agora.io/sdk/Agora_Native_SDK_for_Windows_v4.5.3.{n}_FAV.zip' for n in (1, 2)]
        row = next(r for r in parse_content(''.join(urls)) if r['platform'] == 'Windows')
        self.assertEqual(row['cdn'], urls)
        self.assertEqual(extract_cdn_version('https://download.agora.io/4.5.3/unknown.zip'), '')


if __name__ == '__main__':
    unittest.main()
