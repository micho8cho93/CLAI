import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    print(f"Hello {name}!")

@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        print(f"Goodbye Mr.{name}, take care.")
    else: 
        print(f"Peace {name}")


if __name__ == "__main__":
    app()