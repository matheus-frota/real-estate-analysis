import json
import pendulum

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

@dag(
    schedule=None,
    dag_id='crawlers_real_estate',
    description="Raspagem de dados de sites de imobiliarias",
    catchup=False,
    start_date=pendulum.datetime(2023, 2, 7, tz="America/Sao_Paulo"),
    tags=['raw', '2_daily']
)
def get_data_real_estate():
    """
    ### Get data Real Estate
    Essa dag é responsável por raspar os dados de imovies e salva-los
    na camada raw do data lake.
    """
    @task.virtualenv(
        task_id="virtualenv_python", requirements=["requests"], system_site_packages=False
    )
    def get_data_mgf_imoveis():
        """
        ### Mgf Imovies
        Raspagem de dados do site da mgf imoveis.
        """
        import requests

        url = 'https://www.mgfimoveis.com.br/aluguel/apartamento/ce-sobral'

        response = requests.get(url)
        print(response.status_code)
    get_data_mgf_imoveis()
get_data_real_estate()