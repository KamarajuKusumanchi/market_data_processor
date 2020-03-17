import pandas as pd

if __name__ == '__main__':
    df = pd.read_html('https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/testing-in-us.html')[0]
    # Remove the footnote symbols
    df = df.replace(to_replace='‡', value='', regex=True)
    df = df.astype({'CDC Labs': int, 'US Public Health Labs': int})

    print('As of {date}, CDC Labs tested {cdc} specimens and US Public Health Labs tested {usph} specimens.'.format(
        date=df.iloc[-1]['Date Collected'], cdc=df['CDC Labs'].sum(), usph=df['US Public Health Labs'].sum()))
