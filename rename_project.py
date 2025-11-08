#!/usr/bin/env python3
"""
Project Rename Script for Django Boilerplate

This script renames the Django project from 'hcot' to a custom name.
It updates:
- Directory names
- File contents
- Settings
- HTML templates
- manage.py
- All references to the old project name

Usage:
    python rename_project.py <new_project_name>

Example:
    python rename_project.py myproject
"""

import os
import re
import sys
from pathlib import Path


def validate_project_name(name):
    """
    Validate the new project name.

    Args:
        name: The proposed project name

    Returns:
        bool: True if valid, False otherwise
    """
    if not name:
        print("❌ Error: Project name cannot be empty")
        return False

    if not re.match(r'^[a-z][a-z0-9_]*$', name):
        print("❌ Error: Project name must start with a letter and contain only lowercase letters, numbers, and underscores")
        return False

    if name in ['test', 'tests', 'django', 'site', 'admin']:
        print(f"❌ Error: '{name}' is a reserved name")
        return False

    return True


def replace_in_file(file_path, old_name, new_name):
    """
    Replace all occurrences of old_name with new_name in a file.

    Args:
        file_path: Path to the file
        old_name: Old project name
        new_name: New project name
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Replace various forms of the project name
        replacements = [
            (old_name, new_name),  # lowercase
            (old_name.upper(), new_name.upper()),  # UPPERCASE
            (old_name.capitalize(), new_name.capitalize()),  # Capitalized
        ]

        for old, new in replacements:
            content = content.replace(old, new)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not update {file_path}: {e}")
        return False


def rename_project(old_name, new_name):
    """
    Rename the Django project.

    Args:
        old_name: Current project name
        new_name: New project name
    """
    base_dir = Path(__file__).resolve().parent

    print(f"\n🔄 Renaming project from '{old_name}' to '{new_name}'...\n")

    # Files to update
    files_to_update = [
        base_dir / "manage.py",
        base_dir / old_name / "settings.py",
        base_dir / old_name / "urls.py",
        base_dir / old_name / "wsgi.py",
        base_dir / old_name / "asgi.py",
    ]

    # Update file contents
    print("📝 Updating file contents...")
    for file_path in files_to_update:
        if file_path.exists():
            if replace_in_file(file_path, old_name, new_name):
                print(f"   ✅ {file_path.relative_to(base_dir)}")
        else:
            print(f"   ⚠️  {file_path.relative_to(base_dir)} not found")

    # Update HTML templates
    print("\n📄 Updating HTML templates...")
    template_dirs = [
        base_dir / "core" / "templates",
        base_dir / "users" / "templates",
        base_dir / "theme" / "templates",
        base_dir / "templates",
    ]

    for template_dir in template_dirs:
        if template_dir.exists():
            for html_file in template_dir.rglob("*.html"):
                if replace_in_file(html_file, old_name, new_name):
                    print(f"   ✅ {html_file.relative_to(base_dir)}")

    # Rename project directory
    print(f"\n📁 Renaming project directory...")
    old_dir = base_dir / old_name
    new_dir = base_dir / new_name

    if old_dir.exists():
        old_dir.rename(new_dir)
        print(f"   ✅ {old_name}/ → {new_name}/")
    else:
        print(f"   ⚠️  Directory {old_name}/ not found")

    print(f"\n✨ Project successfully renamed to '{new_name}'!")
    print(f"\n📋 Next steps:")
    print(f"   1. Update your database settings if needed")
    print(f"   2. Run: python manage.py migrate")
    print(f"   3. Run: python manage.py createsuperuser")
    print(f"   4. Run: python manage.py runserver")
    print(f"\n💡 Don't forget to update your README and documentation!")


def main():
    """Main entry point for the script."""
    if len(sys.argv) != 2:
        print("Usage: python rename_project.py <new_project_name>")
        print("Example: python rename_project.py myproject")
        sys.exit(1)

    old_name = "hcot"
    new_name = sys.argv[1].lower()

    if not validate_project_name(new_name):
        sys.exit(1)

    if new_name == old_name:
        print(f"⚠️  The new name '{new_name}' is the same as the current name.")
        sys.exit(1)

    # Confirm with user
    print(f"\n⚠️  This will rename the project from '{old_name}' to '{new_name}'")
    print("   This operation will modify files and directories.")
    response = input("\nDo you want to continue? (yes/no): ")

    if response.lower() not in ['yes', 'y']:
        print("❌ Operation cancelled.")
        sys.exit(0)

    rename_project(old_name, new_name)


if __name__ == "__main__":
    main()
