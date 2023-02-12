from datetime import datetime
import json
import pendulum

from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator

from mgf_imoveis import crawler

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
    # @task.virtualenv(
    #     task_id="virtualenv_python", requirements=["requests", "beautifulsoup4"], system_site_packages=False
    # )
    @task()
    def get_data_mgf_imoveis():
        """ Recupera informações do site da MgfImoveis. """
        re_list = crawler()
        dt_now = pendulum.now("America/Sao_Paulo").strftime('%Y-%m-%d %H:%M:%S')
        if re_list != []:
            for real_estate in re_list:
                real_estate['created_date'] = dt_now
            return re_list[0]
        else:
            return None
    get_data_mgf_imoveis()
get_data_real_estate()