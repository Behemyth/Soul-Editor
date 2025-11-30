"""Configuration management for Soul Editor."""

import json
from pathlib import Path


class Config:
    """Manages application configuration including recent projects."""

    APP_NAME = 'SoulEditor'
    CONFIG_FILE = 'config.json'

    def __init__(self) -> None:
        """Initialize the configuration manager."""
        self._config_dir = Path.home() / f'.{self.APP_NAME.lower()}'
        self._config_file = self._config_dir / self.CONFIG_FILE
        self._recent_projects: list[Path] = []
        self._load()

    @property
    def config_dir(self) -> Path:
        """Return the configuration directory path."""
        return self._config_dir

    @property
    def recent_projects(self) -> list[Path]:
        """Return the list of recent projects."""
        return self._recent_projects.copy()

    def _ensure_config_dir(self) -> None:
        """Ensure the configuration directory exists."""
        self._config_dir.mkdir(parents=True, exist_ok=True)

    def _load(self) -> None:
        """Load configuration from disk."""
        if self._config_file.exists():
            try:
                with self._config_file.open('r', encoding='utf-8') as f:
                    data = json.load(f)
                    projects = data.get('recent_projects', [])
                    # Filter out projects that no longer exist
                    self._recent_projects = [Path(p) for p in projects if Path(p).exists()]
            except (json.JSONDecodeError, OSError):
                self._recent_projects = []
        else:
            self._recent_projects = []

    def _save(self) -> None:
        """Save configuration to disk."""
        self._ensure_config_dir()
        data = {'recent_projects': [str(p) for p in self._recent_projects]}
        with self._config_file.open('w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)

    def add_recent_project(self, project_path: Path) -> None:
        """Add a project to the recent projects list.

        Args:
            project_path: Path to the project directory.
        """
        project_path = project_path.resolve()

        # Remove if already exists to move to front
        if project_path in self._recent_projects:
            self._recent_projects.remove(project_path)

        # Add to front of list
        self._recent_projects.insert(0, project_path)

        # Keep only last 10 projects
        self._recent_projects = self._recent_projects[:10]

        self._save()

    def remove_recent_project(self, project_path: Path) -> None:
        """Remove a project from the recent projects list.

        Args:
            project_path: Path to the project directory.
        """
        project_path = project_path.resolve()
        if project_path in self._recent_projects:
            self._recent_projects.remove(project_path)
            self._save()

    def clear_recent_projects(self) -> None:
        """Clear all recent projects."""
        self._recent_projects.clear()
        self._save()
