from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path


class PromptManager:
    """
    Manages Jinja2 prompt templates.
    CRITICAL: Template path and rendering must match documentation.
    Reference: REWRITE_SPECIFICATION.md lines 854-885
    """

    def __init__(self, templates_dir: str = None):
        if templates_dir is None:
            templates_dir = Path(__file__).parent / 'templates'

        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(['html', 'xml'])
        )

    def render_template(self, template_name: str, **kwargs) -> str:
        """
        Render a template with provided context.

        Args:
            template_name: Name of template file
            **kwargs: Template variables

        Returns:
            Rendered template string
        """
        template = self.env.get_template(template_name)
        return template.render(**kwargs)
