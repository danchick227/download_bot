import unittest

from download_bot.services.downloader import YouTubeDownloader


class YouTubeDownloaderFallbackTest(unittest.TestCase):
    def test_quality_candidates_use_lower_resolutions_after_large_file_limit(self):
        candidates = YouTubeDownloader().build_quality_candidates()

        self.assertEqual(len(candidates), 4)
        self.assertIn("720", candidates[0])
        self.assertIn("480", candidates[1])
        self.assertIn("360", candidates[2])
        self.assertIn("240", candidates[3])


if __name__ == "__main__":
    unittest.main()
