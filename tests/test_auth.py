"""
Authentication and User Repository Tests
"""
import unittest
import time
from database.user_repo import register_user, authenticate_user, reset_user_password

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.test_username = f"test_user_{int(time.time() * 1000)}"
        self.test_password = "securePassword123"
        self.test_fullname = "Test Student"

    def test_registration_and_authentication(self):
        # 1. Register
        reg_res = register_user(self.test_username, self.test_password, self.test_fullname, "Canada")
        self.assertTrue(reg_res["success"])
        self.assertEqual(reg_res["username"], self.test_username)

        # 2. Duplicate registration should fail gracefully
        dup_res = register_user(self.test_username, "otherpass123", "Duplicate User")
        self.assertFalse(dup_res["success"])

        # 3. Authenticate with correct password
        auth_res = authenticate_user(self.test_username, self.test_password)
        self.assertTrue(auth_res["success"])
        self.assertEqual(auth_res["full_name"], self.test_fullname)

        # 4. Authenticate with wrong password
        fail_res = authenticate_user(self.test_username, "wrongpass")
        self.assertFalse(fail_res["success"])

    def test_password_reset(self):
        user = f"reset_user_{int(time.time() * 1000)}"
        register_user(user, "oldPass123", "Reset User")
        
        # Reset
        reset_res = reset_user_password(user, "newSecurePass123")
        self.assertTrue(reset_res["success"])

        # Authenticate with new password
        auth_new = authenticate_user(user, "newSecurePass123")
        self.assertTrue(auth_new["success"])

if __name__ == "__main__":
    unittest.main()
