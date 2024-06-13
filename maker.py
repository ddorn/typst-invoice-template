#!/usr/bin/env python

import os
import sys
import time
import shutil
from pathlib import Path

import typer

INVOICES_DIR = Path(__file__).parent.parent / "invoices"
MAKER_DIR = Path(__file__).parent
TEMPLATE = MAKER_DIR / "template.yaml"
METADATA = MAKER_DIR / "metadata.yaml"

app = typer.Typer(no_args_is_help=True, add_completion=False)


def select_file(file: Path):
    METADATA.unlink(missing_ok=True)
    METADATA.symlink_to(file)
    print(f"Selected file: {file}")


@app.command(no_args_is_help=True)
def new(name: str, folder: Path = INVOICES_DIR):
    """Create a new invoice."""
    folder.mkdir(exist_ok=True)
    month = time.strftime("%Y%m")
    invoices_this_month = len(list(folder.glob(f"{month}*.yaml")))
    id_ = f"{month}{invoices_this_month + 1:02d}"
    invoice = folder / f"{id_}-{name}.yaml"

    template = TEMPLATE.read_text()
    template = template.format(id=id_, date=time.strftime("%Y-%m-%d"))
    invoice.write_text(template)

    typer.echo(f"Created invoice: {invoice}")

    select_file(invoice)


@app.command()
def select():
    """Link an invoice to metadata.yaml so that it is the one edited in vscode."""

    # Find the invoices
    invoices = list(INVOICES_DIR.glob("*.yaml"))
    if not invoices:
        print("No invoices found.")
        raise typer.Exit(code=1)
    invoices.sort()

    # Ask the user to select one, most recent last, with most recent 1
    n = len(invoices)
    for i, invoice in enumerate(invoices):
        print(f"{n - i}. {invoice.name}")

    choice = input("Enter number (default 1): ") or "1"
    try:
        choice = int(choice)
    except ValueError:
        print("Invalid choice.")
        raise typer.Exit(code=1)

    if not 1 <= choice <= len(invoices):
        print("Invalid choice.")
        raise typer.Exit(code=1)

    invoice = invoices[len(invoices) - choice]

    # Link metadata.yaml to the invoice
    select_file(invoice)




if __name__ == "__main__":
    app()
