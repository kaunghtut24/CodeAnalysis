

import unittest
import os
import tempfile
from git import Repo
from changelog_tool import generate_changelog

class TestChangelogTool(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create a test repo
        cls.test_repo_path = os.path.join(tempfile.gettempdir(), "test_repo")
        os.makedirs(cls.test_repo_path, exist_ok=True)
        repo = Repo.init(cls.test_repo_path)
        
        # Create test file
        with open(os.path.join(cls.test_repo_path, "test.txt"), "w") as f:
            f.write("test")
            
        # Create initial commit
        repo.index.add(["test.txt"])
        repo.index.commit("Initial commit")

    def test_local_repo(self):
        """Test with local repository path"""
        result = generate_changelog(self.test_repo_path)
        self.assertIn("Initial commit", result)
        
    def test_github_url(self):
        """Test with GitHub URL (mocked)"""
        # This would actually test a real GitHub URL in practice
        with self.assertRaises(ValueError):
            generate_changelog("https://github.com/invalid_url")
            
    def test_invalid_path(self):
        """Test with invalid local path"""
        with self.assertRaises(ValueError):
            generate_changelog("/invalid/path")

if __name__ == "__main__":
    unittest.main()

