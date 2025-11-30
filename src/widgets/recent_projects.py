"""Recent projects widget for Soul Editor."""

from pathlib import Path

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from src.config import Config


class RecentProjectsWidget(QWidget):
    """Widget displaying and managing recent projects."""

    project_selected = Signal(Path)

    def __init__(self, config: Config, parent: QWidget | None = None) -> None:
        """Initialize the recent projects widget.

        Args:
            config: Application configuration manager.
            parent: Parent widget.
        """
        super().__init__(parent)
        self._config = config
        self._setup_ui()
        self._refresh_list()

    def _setup_ui(self) -> None:
        """Set up the user interface."""
        layout = QVBoxLayout(self)

        # Project list
        self._project_list = QListWidget()
        self._project_list.itemDoubleClicked.connect(self._on_item_double_clicked)
        layout.addWidget(self._project_list)

        # Buttons
        button_layout = QHBoxLayout()

        self._open_button = QPushButton('Open Project')
        self._open_button.clicked.connect(self._on_open_clicked)
        button_layout.addWidget(self._open_button)

        self._add_button = QPushButton('Add Project...')
        self._add_button.clicked.connect(self._on_add_clicked)
        button_layout.addWidget(self._add_button)

        self._remove_button = QPushButton('Remove')
        self._remove_button.clicked.connect(self._on_remove_clicked)
        button_layout.addWidget(self._remove_button)

        self._clear_button = QPushButton('Clear All')
        self._clear_button.clicked.connect(self._on_clear_clicked)
        button_layout.addWidget(self._clear_button)

        layout.addLayout(button_layout)

    def _refresh_list(self) -> None:
        """Refresh the project list from configuration."""
        self._project_list.clear()
        for project_path in self._config.recent_projects:
            item = QListWidgetItem(str(project_path))
            item.setData(256, project_path)  # Qt.UserRole = 256
            self._project_list.addItem(item)

    def _get_selected_project(self) -> Path | None:
        """Get the currently selected project path."""
        current_item = self._project_list.currentItem()
        if current_item:
            return current_item.data(256)
        return None

    def _on_item_double_clicked(self, item: QListWidgetItem) -> None:
        """Handle double-click on a project item."""
        project_path = item.data(256)
        if project_path:
            self.project_selected.emit(project_path)

    def _on_open_clicked(self) -> None:
        """Handle open button click."""
        project_path = self._get_selected_project()
        if project_path:
            self.project_selected.emit(project_path)

    def _on_add_clicked(self) -> None:
        """Handle add button click."""
        directory = QFileDialog.getExistingDirectory(self, 'Select Project Directory')
        if directory:
            project_path = Path(directory)
            # Check for pyproject.toml to validate it's a project
            if (project_path / 'pyproject.toml').exists():
                self._config.add_recent_project(project_path)
                self._refresh_list()
            else:
                QMessageBox.warning(
                    self,
                    'Invalid Project',
                    'The selected directory does not contain a pyproject.toml file.',
                )

    def _on_remove_clicked(self) -> None:
        """Handle remove button click."""
        project_path = self._get_selected_project()
        if project_path:
            self._config.remove_recent_project(project_path)
            self._refresh_list()

    def _on_clear_clicked(self) -> None:
        """Handle clear button click."""
        reply = QMessageBox.question(
            self,
            'Clear Recent Projects',
            'Are you sure you want to clear all recent projects?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self._config.clear_recent_projects()
            self._refresh_list()

    def add_project(self, project_path: Path) -> None:
        """Add a project to the recent projects list.

        Args:
            project_path: Path to the project directory.
        """
        self._config.add_recent_project(project_path)
        self._refresh_list()
