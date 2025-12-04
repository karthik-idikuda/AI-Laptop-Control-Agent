"""
Configuration Validator - Ensures valid setup before running agent
"""

import os
import sys
from dotenv import load_dotenv


class ConfigValidator:
    """Validates configuration and provides helpful error messages"""
    
    @staticmethod
    def validate_all():
        """Run all validation checks"""
        print("🔍 Validating configuration...")
        
        # Check 1: .env file exists
        if not os.path.exists('.env'):
            ConfigValidator._error_no_env_file()
            return False
        
        # Load environment
        load_dotenv()
        
        # Check 2: API key is set
        api_key = os.getenv('OPENROUTER_API_KEY')
        if not api_key:
            ConfigValidator._error_no_api_key()
            return False
        
        # Check 3: API key format
        if not ConfigValidator._validate_api_key_format(api_key):
            ConfigValidator._error_invalid_api_key()
            return False
        
        # Check 4: Required directories
        if not ConfigValidator._check_directories():
            return False
        
        # Check 5: Dependencies
        if not ConfigValidator._check_dependencies():
            return False
        
        print("✅ Configuration validated successfully!\n")
        return True
    
    @staticmethod
    def _validate_api_key_format(api_key):
        """Check if API key looks valid"""
        # Gemini API keys typically start with AIza
        if not api_key.startswith('AIza'):
            return False
        # Should be at least 30 characters
        if len(api_key) < 30:
            return False
        return True
    
    @staticmethod
    def _check_directories():
        """Ensure required directories exist"""
        dirs = ['screenshots', 'recordings', 'screenshots/errors']
        for dir_path in dirs:
            os.makedirs(dir_path, exist_ok=True)
        return True
    
    @staticmethod
    def _check_dependencies():
        """Check if required packages are installed"""
        required = {
            'PyQt5': 'GUI framework',
            'pyautogui': 'Computer control',
            'PIL': 'Image processing',
            'cv2': 'Computer vision',
        }
        
        missing = []
        for module, description in required.items():
            try:
                if module == 'PIL':
                    __import__('PIL')
                elif module == 'cv2':
                    __import__('cv2')
                else:
                    __import__(module)
            except ImportError:
                missing.append(f"{module} ({description})")
        
        if missing:
            print("\n❌ Missing required dependencies:")
            for dep in missing:
                print(f"   - {dep}")
            print("\n💡 Install with: pip install -r requirements.txt\n")
            return False
        
        return True
    
    @staticmethod
    def _error_no_env_file():
        """Show helpful message for missing .env file"""
        print("\n" + "="*60)
        print("❌ ERROR: Missing .env file")
        print("="*60)
        print("\n📝 The .env file contains your API configuration.")
        print("\n🔧 To fix this:\n")
        print("1. Create a file named '.env' in this directory:")
        print(f"   {os.getcwd()}")
        print("\n2. Add your Gemini API key:")
        print("   OPENROUTER_API_KEY=your_api_key_here")
        print("\n3. Get a free API key from:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n" + "="*60 + "\n")
    
    @staticmethod
    def _error_no_api_key():
        """Show helpful message for missing API key"""
        print("\n" + "="*60)
        print("❌ ERROR: Missing API Key in .env file")
        print("="*60)
        print("\n📝 Your .env file exists but doesn't contain the API key.")
        print("\n🔧 To fix this:\n")
        print("1. Open the .env file")
        print("2. Add this line:")
        print("   OPENROUTER_API_KEY=your_api_key_here")
        print("\n3. Replace 'your_api_key_here' with your actual key from:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n" + "="*60 + "\n")
    
    @staticmethod
    def _error_invalid_api_key():
        """Show helpful message for invalid API key format"""
        print("\n" + "="*60)
        print("⚠️  WARNING: API Key format looks incorrect")
        print("="*60)
        print("\n📝 Gemini API keys should:")
        print("   - Start with 'AIza'")
        print("   - Be at least 30 characters long")
        print("\n🔧 Please verify your API key from:")
        print("   https://aistudio.google.com/app/apikey")
        print("\n💡 Make sure you copied the entire key")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Test the validator
    if ConfigValidator.validate_all():
        print("✅ All checks passed!")
    else:
        print("❌ Validation failed")
        sys.exit(1)
