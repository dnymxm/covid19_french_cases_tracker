import requests
import datetime
import json
import click

from pprint import pprint

YESTERDAY = str(datetime.date.today() - datetime.timedelta(days=1))
TODAY = str(datetime.date.today())

DATAS_LINK = "https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.json"
DATAS_FILE = "covid19_french_datas.json"


def _get(link):

    r = requests.get(link)

    if r.ok:
        datas = r.json()
        liste = []
        with open(DATAS_FILE, "w") as f:
            for data in datas:
                data_source = data.get("sourceType")
                data_date = data.get("date")
                if data_source == "opencovid19-fr" and data_date == YESTERDAY:
                    liste.append(data)
            json.dump(liste, f, indent=4, ensure_ascii=False)
    else:
        pprint(r.status_code)


def _list_of_departments(ctx, args, incomplete):
    with open(DATAS_FILE, "r") as f:
        datas = json.load(f)
    departments = [data.get("nom") for data in datas]
    return departments


@click.group()
def cli():
    """Simple CLI app to track french covid-19 cases."""
    # _get(DATAS_LINK)
    pass


@cli.command()
@click.argument("department", type=click.STRING, autocompletion=_list_of_departments)
def get(department):
    """Get informations about DEPARTMENT"""
    with open(DATAS_FILE, "r") as f:
        datas = json.load(f)
    for data in datas:
        if data.get("nom") == department:
            click.echo(f"🏥 Hospitalized: {data.get('hospitalises')}")
            click.echo(f"💔 Reanimations: {data.get('reanimation')}")
            click.echo(f"💀 Deaths: {data.get('deces')}")
            click.echo(f"😁 Cured: {data.get('gueris')}")
