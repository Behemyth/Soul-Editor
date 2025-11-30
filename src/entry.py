"""Entry point for Soul Editor."""

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QMenu, QSizePolicy, QVBoxLayout, QWidget

from src.config import Config
from src.widgets.recent_projects import RecentProjectsWidget


def _get_samples_directory() -> Path | None:
    """Get the samples directory if running from source.

    This will only find the samples directory when running from a cloned
    repository, not when installed as a package.
    """
    # Look for the examples/sample directory relative to the source
    source_dir = Path(__file__).parent.parent
    samples_dir = source_dir / 'examples' / 'sample'
    if samples_dir.exists() and (samples_dir / 'pyproject.toml').exists():
        return samples_dir
    return None


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self, config: Config) -> None:
        """Initialize the main window.

        Args:
            config: Application configuration manager.
        """
        super().__init__()
        self._config = config
        self._current_project: Path | None = None
        self.setWindowTitle('Soul Editor')
        self.setMinimumSize(800, 600)
        self._setup_menu_bar()
        self._setup_project_selector()
        self._setup_development_project()

    def _setup_menu_bar(self) -> None:
        """Set up the menu bar."""
        menu_bar = self.menuBar()

        # File menu
        self._file_menu = menu_bar.addMenu('&File')

        # Recent Projects submenu
        self._recent_projects_menu = QMenu('Recent Projects', self)
        self._file_menu.addMenu(self._recent_projects_menu)
        self._update_recent_projects_menu()

        self._file_menu.addSeparator()

        # Exit action
        exit_action = QAction('E&xit', self)
        exit_action.triggered.connect(self.close)
        self._file_menu.addAction(exit_action)

        # Spacer to push project name to center
        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        menu_bar.setCornerWidget(spacer)

        # Project name label in menu bar
        self._project_name_label = QLabel()
        self._project_name_label.setStyleSheet('padding-right: 10px;')
        menu_bar.setCornerWidget(self._project_name_label, Qt.Corner.TopRightCorner)

    def _update_recent_projects_menu(self) -> None:
        """Update the recent projects submenu."""
        self._recent_projects_menu.clear()

        recent_projects = self._config.recent_projects
        if not recent_projects:
            no_projects_action = QAction('(No recent projects)', self)
            no_projects_action.setEnabled(False)
            self._recent_projects_menu.addAction(no_projects_action)
        else:
            for project_path in recent_projects:
                action = QAction(str(project_path), self)
                action.setData(project_path)
                action.triggered.connect(lambda checked, p=project_path: self._open_project(p))
                self._recent_projects_menu.addAction(action)

    def _setup_project_selector(self) -> None:
        """Set up the project selector view."""
        self._project_selector = QWidget()
        layout = QVBoxLayout(self._project_selector)

        # Title label
        title_label = QLabel('Recent Projects')
        title_label.setStyleSheet('font-size: 18px; font-weight: bold; margin-bottom: 10px;')
        layout.addWidget(title_label)

        # Recent projects widget
        self._recent_projects_widget = RecentProjectsWidget(self._config)
        self._recent_projects_widget.project_selected.connect(self._on_project_selected)
        layout.addWidget(self._recent_projects_widget)

        self.setCentralWidget(self._project_selector)

        # Hide menu bar on project selector screen
        self.menuBar().hide()

    def _setup_development_project(self) -> None:
        """Add the development sample project if in development mode."""
        samples_dir = _get_samples_directory()
        if samples_dir:
            self._recent_projects_widget.add_project(samples_dir)
            self._update_recent_projects_menu()

    def _open_project(self, project_path: Path) -> None:
        """Open a project and switch to the editor view.

        Args:
            project_path: Path to the project directory.
        """
        self._current_project = project_path
        self._config.add_recent_project(project_path)
        self._update_recent_projects_menu()
        self.setWindowTitle(f'Soul Editor - {project_path.name}')
        self._project_name_label.setText(str(project_path))

        # Show menu bar when project is open
        self.menuBar().show()

        # Create the editor view (placeholder for now)
        editor_widget = QWidget()
        self.setCentralWidget(editor_widget)

        # Maximize the window
        self.showMaximized()

    def _on_project_selected(self, project_path: Path) -> None:
        """Handle project selection.

        Args:
            project_path: Path to the selected project.
        """
        self._open_project(project_path)


def main() -> None:
    """Run the application."""
    config = Config()
    app = QApplication(sys.argv)
    window = MainWindow(config)
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
