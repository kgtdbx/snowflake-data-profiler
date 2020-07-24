import pandas as pd
from pandas_profiling import ProfileReport
from snowflake import connector

def file_to_df(file_name):
    if file_name.endswith('.csv'):
        df = pd.read_csv(file_name)
    elif file_name.endswith('.xlsx'):
        df = pd.read_excel(file_name)
    elif file_name.endswith('.json'):
        df = pd.read_json(file_name)
    elif file_name.endswith('.sql'):
        df = pd.read_sql(file_name)
    elif file_name.endswith('.html'):
        df = pd.read_html(file_name)
    elif file_name.endswith('.sql'):
        df = pd.read_sql(file_name)
    return df

def connect_to_snowflake(sfUser, sfPswd, sfAccount, sfDatabase, sfSchema, sfTable, sfWarehouse=None, sfRole=None):
    print(f'sfWarehouse: {sfWarehouse}')
    con = connector.connect(
        user=sfUser,
        password=sfPswd,
        account=sfAccount,
        database=sfDatabase,
        schema=sfSchema,
        role=sfRole,
    )
    cur = con.cursor()
    if sfWarehouse is not None:
        cur.execute(f'use warehouse {sfWarehouse};')

    cur.execute(f'select * from {sfDatabase}.{sfSchema}.{sfTable} limit 1000000;')
    df = cur.fetch_pandas_all()
    return df

def get_profile_results(data):
    profile = ProfileReport(data, title='Snowflake Data Profiler', progress_bar=False, minimal=True)
    p = profile.to_html()
    return p

def do_profile():
    pd_df = connect_to_snowflake()
    return get_profile_results(pd_df)

if __name__ == "__main__":
    do_profile()
