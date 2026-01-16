# acronym/cli.py
import click
import yaml
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()
DEFAULT_FILE = Path.home() / ".config" / "acronym" / "acronyms.yaml"


def ensure_file(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        with path.open("w") as f:
            yaml.safe_dump({}, f)


def load_acronyms(path: Path):
    ensure_file(path)
    with path.open() as f:
        return yaml.safe_load(f) or {}


def save_acronyms(path: Path, acronyms):
    with path.open("w") as f:
        yaml.safe_dump(acronyms, f, sort_keys=True)


# --- Custom MultiCommand to allow default lookup ---
class AcronymCLI(click.MultiCommand):
    def list_commands(self, ctx):
        return ["add", "delete", "list"]

    def get_command(self, ctx, name):
        # If name matches a subcommand, return that
        commands = {
            "add": add,
            "delete": delete,
            "list": list_acronyms
        }
        cmd = commands.get(name)
        if cmd:
            return cmd

        # Otherwise treat as a default lookup
        acronyms = load_acronyms(DEFAULT_FILE)
        key = name.upper()
        entry = acronyms.get(key)
        if entry:
            def lookup_cmd():
                console.print(f"[bold cyan]{key}[/bold cyan]")
                console.print(f"[bold]Full Name:[/bold] {entry['full_name']}")
                console.print(f"[bold]Description:[/bold] {entry['description']}")
            return click.Command(name, callback=lambda **kwargs: lookup_cmd())

        # If neither a subcommand nor a known acronym
        return None


# --- commands ---
@click.command()
@click.argument("acronym")
@click.option("--full-name", prompt=True)
@click.option("--description", prompt=True)
def add(acronym, full_name, description):
    """Add a new acronym."""
    acronyms = load_acronyms(DEFAULT_FILE)
    key = acronym.upper()
    if key in acronyms and not click.confirm(f"{key} exists. Overwrite?"):
        console.print("[yellow]Add cancelled[/yellow]")
        return
    acronyms[key] = {"full_name": full_name, "description": description}
    save_acronyms(DEFAULT_FILE, acronyms)
    console.print(f"[green]Added[/green] {key}")


@click.command()
@click.argument("acronym")
def delete(acronym):
    """Delete an acronym."""
    acronyms = load_acronyms(DEFAULT_FILE)
    key = acronym.upper()
    if key not in acronyms:
        console.print(f"[red]No entry found for {key}[/red]")
        return
    if click.confirm(f"Are you sure you want to delete {key}?"):
        del acronyms[key]
        save_acronyms(DEFAULT_FILE, acronyms)
        console.print(f"[green]Deleted[/green] {key}")
    else:
        console.print("[yellow]Delete cancelled[/yellow]")


@click.command(name="list")
def list_acronyms():
    """List all acronyms."""
    acronyms = load_acronyms(DEFAULT_FILE)
    if not acronyms:
        console.print("[yellow]No acronyms found[/yellow]")
        return
    table = Table(title="Acronyms")
    table.add_column("Acronym", style="cyan", no_wrap=True)
    table.add_column("Full Name", style="bold")
    table.add_column("Description")
    for key in sorted(acronyms):
        entry = acronyms[key]
        table.add_row(key, entry["full_name"], entry["description"])
    console.print(table)


# --- entry point ---
cli = AcronymCLI(help="Acronym CLI tool.")


def main():
    cli()


if __name__ == "__main__":
    main()

