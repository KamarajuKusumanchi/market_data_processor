import pandas as pd

if __name__ == '__main__':
    df = pd.read_html('https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/testing-in-us.html')[0]
    # Remove the footnote symbols
    # The website was initially using '‡' as a footnote symbol.
    # But later changed it to '§'. So we can't use something like
    #     df = df.replace(to_replace='‡', value='', regex=True)
    # which hard codes the symbols. Instead, make it more resilient by
    # deleting any non-digit characters in the columns of interest.
    df[['CDC Labs', 'US Public Health Labs']] = df[['CDC Labs', 'US Public Health Labs']]\
        .replace(to_replace='[^0-9]', value='', regex=True)\
        .replace(to_replace='', value='0', regex=True)
    df = df.astype({'CDC Labs': int, 'US Public Health Labs': int})

    print('As of {date} CDC Labs tested {cdc:,} specimens and US Public Health Labs tested {usph:,} specimens.'.format(
        date=df.iloc[-1]['Date Collected'], cdc=df['CDC Labs'].sum(), usph=df['US Public Health Labs'].sum()))
