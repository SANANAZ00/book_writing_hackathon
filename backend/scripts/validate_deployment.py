"""
Validation script to test the deployed functionality
"""
import asyncio
import requests
import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

async def validate_backend():
    """
    Validate backend API endpoints
    """
    print("Validating backend endpoints...")

    # Test base API
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✓ Base API endpoint is accessible")
        else:
            print(f"✗ Base API endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing base API: {str(e)}")

    # Test health endpoint
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            health_data = response.json()
            if "status" in health_data and health_data["status"] == "healthy":
                print("✓ Health endpoint is working correctly")
            else:
                print(f"✗ Health endpoint returned unexpected data: {health_data}")
        else:
            print(f"✗ Health endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing health endpoint: {str(e)}")

    # Test agents endpoint
    try:
        response = requests.get("http://localhost:8000/api/agents/available")
        if response.status_code == 200:
            agents_data = response.json()
            if "subagents" in agents_data and "skills" in agents_data:
                print(f"✓ Agents endpoint is working correctly")
                print(f"  Available subagents: {len(agents_data['subagents']['names'])}")
                print(f"  Available skills: {len(agents_data['skills']['names'])}")
            else:
                print(f"✗ Agents endpoint returned unexpected data structure: {agents_data}")
        else:
            print(f"✗ Agents endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing agents endpoint: {str(e)}")

def validate_frontend():
    """
    Validate frontend functionality
    """
    print("\nValidating frontend components...")

    # Check if required directories exist
    required_dirs = ["docs", "src", "src/components"]
    all_exist = True

    for directory in required_dirs:
        if not Path(directory).exists():
            print(f"✗ Required directory missing: {directory}")
            all_exist = False
        else:
            print(f"✓ Directory exists: {directory}")

    if all_exist:
        print("✓ All required frontend directories exist")

    # Check for custom components
    components = ["ChatbotWidget", "CalloutBox", "ConceptCard", "StepFlow", "SelectTextOverlay"]
    for component in components:
        component_file = Path(f"src/components/{component}.js")
        if component_file.exists():
            print(f"✓ Component exists: {component}")
        else:
            print(f"✗ Component missing: {component}")

def validate_content():
    """
    Validate that documentation content exists
    """
    print("\nValidating documentation content...")

    docs_path = Path("docs")
    if docs_path.exists():
        mdx_files = list(docs_path.rglob("*.mdx"))
        md_files = list(docs_path.rglob("*.md"))
        total_files = len(mdx_files) + len(md_files)

        if total_files > 0:
            print(f"✓ Documentation content exists: {total_files} files")
            print(f"  - MDX files: {len(mdx_files)}")
            print(f"  - MD files: {len(md_files)}")
        else:
            print("✗ No documentation content found")
    else:
        print("✗ Documentation directory does not exist")

def validate_structure():
    """
    Validate project structure
    """
    print("\nValidating project structure...")

    expected_files = [
        "docusaurus.config.js",
        "package.json",
        "README.md",
        "backend/app/main.py",
        "backend/app/agents/__init__.py",
        "backend/app/routes/agents.py",
        "src/components/ChatbotWidget.js",
        "src/theme/Layout.js"
    ]

    all_exist = True
    for file in expected_files:
        if not Path(file).exists():
            print(f"✗ Missing file: {file}")
            all_exist = False
        else:
            print(f"✓ File exists: {file}")

    if all_exist:
        print("✓ All expected files exist in the project structure")

async def main():
    """
    Main validation function
    """
    print("AI-Powered Book - Deployment Validation")
    print("=" * 50)

    validate_structure()
    validate_content()
    validate_frontend()
    await validate_backend()

    print("\n" + "=" * 50)
    print("Validation completed!")
    print("Note: Backend validation requires the server to be running on http://localhost:8000")

if __name__ == "__main__":
    asyncio.run(main())