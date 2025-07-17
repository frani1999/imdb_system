import typer
import requests

app = typer.Typer()
api_url_option = typer.Option("http://localhost:8000", help="Base URL of the REST API")


@app.command()
def people(name: str, api_url: str = api_url_option):
    url = f"{api_url}/people/{name}"
    try:
        response = requests.get(url)
    except Exception as e:
        typer.echo("Error: " + str(e), err=True)
        raise typer.Exit(code=1)
    if response.status_code == 200:
        data = response.json()
        print(data.get("summary") or data.get("error"))
    else:
        print("Error: ", response.text)


@app.command()
def films(title: str, api_url: str = api_url_option):
    url = f"{api_url}/films/{title}"
    try:
        response = requests.get(url)
    except Exception as e:
        typer.echo("Error: " + str(e), err=True)
        raise typer.Exit(code=1)
    if response.status_code == 200:
        data = response.json()
        print(data.get("summary") or data.get("error"))
    else:
        print("Error: ", response.text)


if __name__ == "__main__":
    app()
