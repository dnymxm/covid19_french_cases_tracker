# Imports
import requests
import datetime
import json
import click
import re
import logging

# Constants
YESTERDAY = str(datetime.date.today() - datetime.timedelta(days=1))
TODAY = str(datetime.date.today())
DATAS_LINK = "https://raw.githubusercontent.com/opencovid19-fr/data/master/dist/chiffres-cles.json"
DATAS_FILE = "covid19_french_datas.json"
LOGS_FILE = "logs.txt"
SOURCE = "opencovid19-fr"


# Private Functions
def __get_datas(link):
    """Retrieve covid10 informations from LINK and save it in DATAS_FILE  

    Args:
        link (str): Informations about COVID-19 in .JSON
    """
    r = requests.get(link)

    if r.ok:
        datas = r.json()
        liste = []
        with open(DATAS_FILE, "w") as f:
            for data in datas:
                data_source = data.get("sourceType")
                data_date = data.get("date")
                if data_source == SOURCE and data_date == YESTERDAY:
                    liste.append(data)
            json.dump(liste, f, indent=4, ensure_ascii=False)
        with open(LOGS_FILE, "w") as f:
            f.write(TODAY)
    else:
        logging.info(
            (f"We haven't been able to retrieve datas: {r.status_code}"))


def __get_regions(ctx, args, incomplete):
    """Get list of all French Regions from DATAS_FILE for autocomplete

    Args:
        ctx (click.core.Context): The current command context
        args (list): The list of arguments passed in
        incomplete (str): The partial word that is being completed. May be an empty string if no characters have been entered yet

    Returns:
        list: All French regions
    """
    with open(DATAS_FILE, "r") as f:
        datas = json.load(f)
    regions = [data.get("nom") for data in datas if re.match(
        incomplete.capitalize(), data["nom"])]
    return regions

# Commands
@click.group()
def cli():
    """Simple CLI app to track french covid-19 cases."""
    with open(LOGS_FILE, "r") as f:
        logs = f.read()
        if TODAY not in logs:
            __get_datas(DATAS_LINK)


@cli.command()
@click.argument("region", type=click.STRING, autocompletion=__get_regions)
def get(region):
    """Get informations about REGION"""
    with open(DATAS_FILE, "r") as f:
        datas = json.load(f)
    for data in datas:
        if data.get("nom") == region:
            click.echo(f"🏥 Hospitalized: {data.get('hospitalises')}")
            click.echo(f"💔 Reanimations: {data.get('reanimation')}")
            click.echo(f"💀 Deaths: {data.get('deces')}")
            click.echo(f"😁 Recovered: {data.get('gueris')}")
        else:
            logging.info(f"{region} isn't a French Region")


@cli.command()
@click.argument('regions', nargs=-1, type=click.STRING, autocompletion=__get_regions)
def compare(regions):
    """Compare cases between REGIONS"""
    with open(DATAS_FILE, "r") as f:
        datas = json.load(f)
    for data in datas:
        if data["nom"] in regions:
            click.echo("============================================")
            click.echo(f"🌍 Region: {data.get('nom')}")
            click.echo(f"🏥 Hospitalized: {data.get('hospitalises')}")
            click.echo(f"💔 Reanimations: {data.get('reanimation')}")
            click.echo(f"💀 Deaths: {data.get('deces')}")
            click.echo(f"😁 Recovered: {data.get('gueris')}")


@cli.command()
def all():
    """Print informations on all of France regions"""
    with open(DATAS_FILE, "r") as f:
        datas = json.load(f)
    for data in sorted(datas, key=lambda x: (x['nom'])):
        if data["nom"] != "France":
            click.echo("============================================")
            click.echo(f"🌍 Region: {data.get('nom')}")
            click.echo(f"🏥 Hospitalized: {data.get('hospitalises')}")
            click.echo(f"💔 Reanimations: {data.get('reanimation')}")
            click.echo(f"💀 Deaths: {data.get('deces')}")
            click.echo(f"😁 Recovered: {data.get('gueris')}")
