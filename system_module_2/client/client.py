import typer
import requests

'''
python system_module_2/client/client.py people "Bruce Lee"
# Bruce Lee was born in 1940 and was actor and producer.

python system_module_2/client/client.py films "Blacksmith Scene"
# Blacksmith Scene, originally titled 'Les forgerons', is a documentary.
'''

app = typer.Typer()
API_REST_URL = "http://localhost:8000"


@app.command()
def people(name: str):
    url = f"{API_REST_URL}/people/{name}"
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
def films(title: str):
    url = f"{API_REST_URL}/films/{title}"
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
