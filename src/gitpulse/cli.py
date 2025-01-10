import typer

app = typer.Typer(name="gitpulse")

def _version_callback(value: bool) -> None:
    if value:
        print("GitPulse v0.1.0")
        raise typer.Exit()

@app.command()
def hello(
    version: bool = typer.Option(None, "--version", "-v", callback=_version_callback, is_eager=True),
):
    print("Hello from GitPulse!")

if __name__ == "__main__":
    app()
