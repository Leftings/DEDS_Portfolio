import pandas as pd
import sqlite3 as sqlite
import warnings

def run():
    # %% [markdown]
    # # Werkcollege-opdrachten Week 1.3

    # %% [markdown]
    # ## Dependencies importeren

    # %% [markdown]
    # Kopieer in het codeblok hieronder van het vorige practicum de import-code voor de dependencies die het vaakst worden gebruikt om data in te lezen. Geef er ook de gebruikelijke aliassen aan.<br>
    # Zet eventuele warnings uit.

    # %%
    warnings.simplefilter('ignore')

    # %% [markdown]
    # Zet het bestand go_sales_train.sqlite in een makkelijk te vinden map

    # %% [markdown]
    # ## Databasetabellen inlezen

    # %% [markdown]
    # Kopieer in het codeblok hieronder van het vorige practicum de code om een connectie met het bestand go_sales_train.sqlite te maken.

    # %%
    sqliteConnection = sqlite.connect(r'C:\Users\bdebr\OneDrive\Documents\DEDS_Portfolio\data\raw\go_sales_train.sqlite')
    cursor = sqliteConnection.cursor()

    # %% [markdown]
    # Lees van de ingelezen go_sales_train-database te volgende tabellen in met behulp van "SELECT * FROM *tabel*".
    # - product
    # - product_type
    # - product_line
    # - sales_staff
    # - sales_branch
    # - retailer_site
    # - country
    # - order_header
    # - order_details
    # - returned_item
    # - return_reason

    # %%
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    cursor.execute(sql_query)
    tables = cursor.fetchall()
    for table in tables:
        table_name = table[0]
        df = pd.read_sql(f"SELECT * FROM {table_name}", sqliteConnection)
        print({table_name})
        print(df)

    # %% [markdown]
    # Krijg je een "no such table" error? Dan heb je misschien met .connect() per ongeluk een leeg  databasebestand (.sqlite) aangemaakt. <u>Let op:</u> lees eventueel de informatie uit het Notebook van werkcollege 1.1b nog eens goed door.

    # %% [markdown]
    # Als je tijdens onderstaande opdrachten uit het oog verliest welke tabellen er allemaal zijn, kan je deze Pythoncode uitvoeren:

    # %%
    sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
    #Vul dit codeblok verder in
    pd.read_sql(sql_query, sqliteConnection)
    #Op de puntjes hoort de connectie naar go_sales_train óf go_staff_train óf go_crm_train te staan.

    # %% [markdown]
    # erachter 

    # %% [markdown]
    # Let op! Voor alle onderstaande opdrachten mag je <u>alleen Python</u> gebruiken, <u>geen SQL!</u>

    # %% [markdown]
    # ## Selecties op één tabel zonder functies

    # %% [markdown]
    # Geef een overzicht met daarin de producten en hun productiekosten waarvan de productiekosten lager dan 100 dollar en hoger dan 50 dollar ligt. (2 kolommen, 23 rijen)

    # %%
    df = pd.read_sql("SELECT * FROM product", sqliteConnection)
    df_res = df.loc[(df['PRODUCTION_COST'] > 50) & (df['PRODUCTION_COST'] < 100), ['PRODUCT_NAME', 'PRODUCTION_COST']]

    df_res.to_excel(r"C:\Users\bdebr\OneDrive\Documents\DEDS_Portfolio\data\processed\product.xlsx", index=False)
    print(df_res)

    # %% [markdown]
    # Geef een overzicht met daarin de producten en hun marge waarvan de marge lager dan 20 % of hoger dan 60 % ligt. (2 kolommen, 7 rijen) 

    # %%
    df = pd.read_sql("SELECT * FROM product", sqliteConnection)
    df_res = df.loc[(df['MARGIN'] < 0.20) | (df['MARGIN'] > 0.60), ['PRODUCT_NAME', 'MARGIN']]
    df_res.to_excel(r"C:\Users\bdebr\OneDrive\Documents\DEDS_Portfolio\data\processed\productMargin.xlsx", index=False)
    print(df_res)

    # %% [markdown]
    # Geef een overzicht met daarin de landen waar met francs wordt betaald. Sorteer de uitkomst op land.  (1 kolom, 3 rijen)

    # %%
    df = pd.read_sql("SELECT * FROM country", sqliteConnection)
    df_res = df.loc[(df['CURRENCY_NAME'] == 'francs'), ['COUNTRY']]
    df_res.to_excel(r"C:\Users\bdebr\OneDrive\Documents\DEDS_Portfolio\data\processed\countryCurrency.xlsx", index=False)
    print(df_res)

    # %% [markdown]
    # Geef een overzicht met daarin de verschillende introductiedatums waarop producten met meer dan 50% marge worden geïntroduceerd (1 kolom, 7 rijen) 

    # %%
    df = pd.read_sql("SELECT * FROM product", sqliteConnection)
    df_res = df.loc[(df['MARGIN'] > 0.50), ['INTRODUCTION_DATE']]
    df_res_unique = df_res['INTRODUCTION_DATE'].drop_duplicates()

    df_res_unique.to_excel(r"C:\Users\bdebr\OneDrive\Documents\DEDS_Portfolio\data\processed\productIntroDate.xlsx", index=False)
    print(df_res_unique)

    # %% [markdown]
    # Geef een overzicht met daarin het eerste adres en de stad van verkoopafdelingen waarvan zowel het tweede adres als de regio bekend is (2 kolommen, 7 rijen)

    # %%
    df = pd.read_sql("SELECT * FROM sales_branch", sqliteConnection)
    df_res = df.loc[(df['ADDRESS2'].notna()) & (df['REGION'].notna()), ['ADDRESS1', 'CITY']]
    df_res.to_excel(r"C:\Users\bdebr\OneDrive\Documents\DEDS_Portfolio\data\processed\sales_branch.xlsx", index=False)
    print(df_res)


    # %% [markdown]
    # Geef een overzicht met daarin de landen waar met dollars (dollars of new dollar) wordt betaald. Sorteer de uitkomst op land. (1 kolom, 4 rijen) 

    # %%
    df = pd.read_sql("SELECT * FROM country", sqliteConnection)
    df_res = df.loc[(df['CURRENCY_NAME'] == 'dollars') | (df['CURRENCY_NAME'] == 'new dollar'), ['COUNTRY']]
    print(df_res)

    # %% [markdown]
    # Geef een overzicht met daarin beide adressen en de stad van vestigingen van klanten waarvan de postcode begint met een ‘D’ (van duitsland). Filter op vestigingen die een tweede adres hebben. (3 kolommen, 2 rijen) 

    # %%
    df = pd.read_sql("SELECT * FROM retailer_site", sqliteConnection)
    df_res = df.loc[(df['POSTAL_ZONE'].str.startswith('D')) & (df['ADDRESS2'].notna()), ['ADDRESS1', 'ADDRESS2', 'CITY']]
    print(df_res)

    # %% [markdown]
    # ## Selecties op één tabel met functies

    # %% [markdown]
    # Geef het totaal aantal producten dat is teruggebracht (1 waarde) 

    # %%
    df = pd.read_sql("SELECT * FROM returned_item", sqliteConnection)
    df_res = df.shape[0]
    print(df_res)

    # %% [markdown]
    # Geef het aantal regio’s waarin verkoopafdelingen gevestigd zijn. (1 waarde)

    # %%
    df = pd.read_sql("SELECT * FROM sales_branch", sqliteConnection)
    df_res = df['REGION'].nunique()
    print(df_res)


    # %% [markdown]
    # Maak 3 variabelen:
    # - Een met de laagste
    # - Een met de hoogste
    # - Een met de gemiddelde (afgerond op 2 decimalen)
    # 
    # marge van producten (3 kolommen, 1 rij) 

    # %%
    df = pd.read_sql("SELECT * FROM product", sqliteConnection)

    laagste = df['MARGIN'].min()
    hoogste = df['MARGIN'].max()
    gem = round(df['MARGIN'].mean(), 2)

    print(laagste)
    print(hoogste)
    print(gem)


    # %% [markdown]
    # Geef het aantal vestigingen van klanten waarvan het 2e adres niet bekend is (1 waarde)

    # %%
    df = pd.read_sql("SELECT * FROM sales_branch", sqliteConnection)

    df_res = df['ADDRESS2'].isna().sum()
    print(df_res)


    # %% [markdown]
    # Geef de gemiddelde kostprijs van de verkochte producten waarop korting (unit_sale_price < unit_price) is verleend (1 waarde) 

    # %%
    df = pd.read_sql("SELECT * FROM order_details", sqliteConnection)

    df_disc = df[df['UNIT_SALE_PRICE'] < df['UNIT_PRICE']]
    avg_price = round(df_disc['UNIT_PRICE'].mean(), 2)

    print(avg_price)


    # %% [markdown]
    # Geef een overzicht met daarin het aantal medewerkers per medewerkersfunctie (2 kolommen, 7 rijen) 

    # %%
    df = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)

    df_res = df.groupby('POSITION_EN', as_index=False)['SALES_STAFF_CODE'].count()
    df_res

    # %% [markdown]
    # Geef een overzicht met daarin per telefoonnummer het aantal medewerkers dat op dat telefoonnummer bereikbaar is. Toon alleen de telefoonnummer waarop meer dan 4 medewerkers bereikbaar zijn. (2 kolommen, 10 rijen) 

    # %%
    df = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)

    df_res = df.groupby('WORK_PHONE', as_index=False)['SALES_STAFF_CODE'].count()
    df_res_filter = df_res[df_res['SALES_STAFF_CODE'] > 4]
    df_res_filter


    # %% [markdown]
    # ## Selecties op meerdere tabellen zonder functies

    # %% [markdown]
    # Geef een overzicht met daarin het eerste adres en de stad van vestigingen van klanten uit ‘Netherlands’ (2 kolommen, 20 rijen) 

    # %%
    retailer = pd.read_sql("SELECT * FROM retailer_site", sqliteConnection)
    country = pd.read_sql("SELECT * FROM country", sqliteConnection)

    df_merge = pd.merge(retailer, country, left_on='COUNTRY_CODE', right_on='COUNTRY_CODE', how='left')
    df_nl = df_merge['COUNTRY'] == 'Netherlands'
    df_merge.loc[(df_nl), ['ADDRESS1', 'CITY']]



    # %% [markdown]
    # Geef een overzicht met daarin de productnamen die tot het producttype ‘Eyewear’ behoren. (1 kolom, 5 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    type = pd.read_sql("SELECT * FROM product_type", sqliteConnection)

    df_merge = pd.merge(product, type, left_on='PRODUCT_TYPE_CODE', right_on='PRODUCT_TYPE_CODE', how='left')
    df_nl = df_merge['PRODUCT_TYPE_EN'] == 'Eyewear'
    df_merge.loc[(df_nl), ['PRODUCT_NAME']]



    # %% [markdown]
    # Geef een overzicht met daarin alle unieke eerste adressen van klantvestigingen en de voornaam en achternaam van de verkopers die ‘Branch Manager’ zijn en aan deze vestigingen hebben verkocht (3 kolommen, 1 rij) 

    # %%
    sales_staff = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)
    sales_branch = pd.read_sql("SELECT * FROM sales_branch", sqliteConnection)
    order_header = pd.read_sql("SELECT * FROM order_header", sqliteConnection)

    df_merge = pd.merge(sales_branch, order_header, left_on='SALES_BRANCH_CODE', right_on='SALES_BRANCH_CODE')
    df_merge2 = pd.merge(df_merge, sales_staff, left_on='SALES_STAFF_CODE', right_on='SALES_STAFF_CODE')

    df_filter = df_merge2[df_merge2['POSITION_EN'] == 'Branch Manager']
    df_res = df_filter[['ADDRESS1', 'FIRST_NAME', 'LAST_NAME']].drop_duplicates()
    df_res




    # %% [markdown]
    # Geef een overzicht met daarin van de verkopers hun functie en indien zij iets hebben verkocht de datum waarop de verkoop heeft plaatsgevonden. Laat alleen de verschillende namen van de posities zien van de verkopers die het woord ‘Manager’ in hun positienaam hebben staan. (2 kolommen, 7 rijen) 

    # %%
    sales_staff = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)
    order_header = pd.read_sql("SELECT * FROM order_header", sqliteConnection)

    df_merge = pd.merge(order_header, sales_staff, left_on='SALES_STAFF_CODE', right_on='SALES_STAFF_CODE', how='right')

    df_filter = df_merge[df_merge['POSITION_EN'].str.contains('Manager', case=False, na=False)]

    df_res = df_filter[['POSITION_EN', 'ORDER_DATE']].drop_duplicates()
    df_res




    # %% [markdown]
    # Geef een overzicht met daarin de verschillende namen van producten en bijbehorende namen van producttypen van de producten waarvoor ooit meer dan 750 stuks tegelijk verkocht zijn. (2 kolommen, 9 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    type = pd.read_sql("SELECT * FROM product_type", sqliteConnection)
    order_details = pd.read_sql("SELECT * FROM order_details", sqliteConnection)

    df_merge = pd.merge(product, type, left_on='PRODUCT_TYPE_CODE', right_on='PRODUCT_TYPE_CODE')
    df_merge = pd.merge(df_merge, order_details, left_on='PRODUCT_NUMBER', right_on='PRODUCT_NUMBER')

    df_filter = df_merge[df_merge['QUANTITY'] > 750]

    df_res = df_filter[['PRODUCT_NAME', 'PRODUCT_TYPE_EN']].drop_duplicates()
    df_res




    # %% [markdown]
    # Geef een overzicht met daarin de productnamen waarvan ooit meer dan 40% korting is verleend. De formule voor korting is: (unit_price - unit_sale_price) / unit_price (1 kolom, 8 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    order_details = pd.read_sql("SELECT * FROM order_details", sqliteConnection)

    df_merge = pd.merge(product, order_details, on='PRODUCT_NUMBER')
    df_merge['DISCOUNT'] = (df_merge['UNIT_PRICE'] - df_merge['UNIT_SALE_PRICE']) / df_merge['UNIT_PRICE']

    df_filter = df_merge[df_merge['DISCOUNT'] > 0.40]

    df_res = df_filter[['PRODUCT_NAME']].drop_duplicates()
    df_res


    # %% [markdown]
    # Geef een overzicht met daarin de retourreden van producten waarvan ooit meer dan 90% van de aangeschafte hoeveelheid is teruggebracht (return_quantity/quantity). (1 kolom, 3 rijen) 

    # %%
    order_details = pd.read_sql("SELECT * FROM order_details", sqliteConnection)
    returned_item = pd.read_sql("SELECT * FROM returned_item", sqliteConnection)
    return_reason = pd.read_sql("SELECT * FROM return_reason", sqliteConnection)

    df_merge = pd.merge(order_details, returned_item, on='ORDER_DETAIL_CODE')
    df_merge = pd.merge(df_merge, return_reason, on='RETURN_REASON_CODE')

    df_merge['RETOUR'] = df_merge['RETURN_QUANTITY'] / df_merge['QUANTITY']

    df_filter = df_merge[df_merge['RETOUR'] > 0.9]

    df_res = df_filter[['RETURN_DESCRIPTION_EN']].drop_duplicates()
    df_res

    # %% [markdown]
    # ## Selecties op meerdere tabellen met functies

    # %% [markdown]
    # Geef een overzicht met daarin per producttype het aantal producten die tot dat producttype behoren. (2 kolommen, 21 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    type = pd.read_sql("SELECT * FROM product_type", sqliteConnection)

    df_merge = pd.merge(product, type, on='PRODUCT_TYPE_CODE')

    df_res = df_merge.groupby('PRODUCT_TYPE_EN', as_index=False)['PRODUCT_NUMBER'].count()
    df_res


    # %% [markdown]
    # Geef een overzicht met daarin per land het aantal vestigingen van klanten die zich in dat land bevinden. (2 kolommen, 21 rijen) 

    # %%
    country = pd.read_sql("SELECT * FROM country", sqliteConnection)
    retailer = pd.read_sql("SELECT * FROM retailer_site", sqliteConnection)

    df_merge = pd.merge(country, retailer, on='COUNTRY_CODE')

    df_res = df_merge.groupby('COUNTRY', as_index=False)['RETAILER_SITE_CODE'].count()
    df_res


    # %% [markdown]
    # Geef een overzicht met daarin van de producten behorend tot het producttype ‘Cooking Gear’ per productnaam de totaal verkochte hoeveelheid en de gemiddelde verkoopprijs. Sorteer de uitkomst op totaal verkochte hoeveelheid. (4 kolommen, 10 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    product_type = pd.read_sql("SELECT * FROM product_type", sqliteConnection)
    details = pd.read_sql("SELECT * FROM order_details", sqliteConnection)

    df_merge = pd.merge(product, product_type, on='PRODUCT_TYPE_CODE')
    df_merge = pd.merge(df_merge, details, on='PRODUCT_NUMBER')

    df_filter = df_merge[df_merge['PRODUCT_TYPE_EN'] == 'Cooking Gear']

    df_res = df_filter.groupby('PRODUCT_NAME').agg(
        TOTAL = ('QUANTITY', 'sum'),
        AVG = ('UNIT_SALE_PRICE', 'mean')
    )

    df_res['AVG'] = df_res['AVG'].round(2)
    df_res = df_res.sort_values(by='TOTAL', ascending=False)
    df_res


    # %% [markdown]
    # Geef een overzicht met daarin per land de naam van het land, de naam van de stad waar de verkoopafdeling is gevestigd (noem de kolomnaam in het overzicht ‘verkoper’) en het aantal steden waar zich klanten bevinden in dat land (noem de kolomnaam in het overzicht ‘klanten’) (3 kolommen, 29 rijen) 

    # %%
    country = pd.read_sql("SELECT * FROM COUNTRY", sqliteConnection)
    sales_branch = pd.read_sql("SELECT * FROM sales_branch", sqliteConnection)
    retailer_site = pd.read_sql("SELECT * FROM retailer_site", sqliteConnection)

    df_sales = pd.merge(country, sales_branch, on='COUNTRY_CODE')

    df_customers = retailer_site.groupby('COUNTRY_CODE', as_index=False)['CITY'].nunique()
    df_customers.rename(columns={'CITY' : 'klanten'}, inplace=True)

    df_res = pd.merge(df_sales[['COUNTRY', 'CITY', 'COUNTRY_CODE']], df_customers, on='COUNTRY_CODE')
    df_res = df_res[['COUNTRY', 'CITY', 'klanten']].rename(columns={'CITY' : 'verkoper'})
    df_res

    #28 rijen inplaats van 29?

    # %% [markdown]
    # ## Pythonvertalingen van SUBSELECT en UNION met o.a. for-loops

    # %% [markdown]
    # Geef een overzicht met daarin de voornaam en de achternaam van de medewerkers die nog nooit wat hebben verkocht (2 kolommen, 25 rijen) 

    # %%
    sales_staff = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)
    order_header = pd.read_sql("SELECT * FROM order_header", sqliteConnection)

    verkoper = set(order_header['SALES_STAFF_CODE'])

    nooit_verkocht = []
    for _, row in sales_staff.iterrows():
        if row['SALES_STAFF_CODE'] not in verkoper:
            nooit_verkocht.append((row['FIRST_NAME'], row['LAST_NAME']))

    df_res = pd.DataFrame(nooit_verkocht, columns=['FIRST_NAME', 'LAST_NAME'])
    df_res

    # %% [markdown]
    # Geef een overzicht met daarin het aantal producten waarvan de marge lager is dan de gemiddelde marge van alle producten samen. Geef in het overzicht tevens aan wat de gemiddelde marge is van dit aantal producten waarvan de marge lager dan de gemiddelde marge van alle producten samen is. (1 kolom, 2 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    order_details = pd.read_sql("SELECT * FROM order_details", sqliteConnection)

    df_merge = pd.merge(product, order_details, on='PRODUCT_NUMBER')
    df_merge['MARGIN'] = (df_merge['UNIT_SALE_PRICE'] - df_merge['UNIT_COST']) / df_merge['UNIT_SALE_PRICE']

    avg_margin_all = product['MARGIN'].mean()
    df_filter = product[product['MARGIN'] < avg_margin_all]

    df_res = pd.DataFrame({
        'Aantal producten': [df_filter.shape[0]],
        'Gemiddelde marge': [df_filter['MARGIN'].mean()]
    })

    df_res


    # %% [markdown]
    # Geef een overzicht met daarin de namen van de producten die voor meer dan 500 (verkoopprijs) zijn verkocht maar nooit zijn teruggebracht. (1 kolom, 13 rijen) 

    # %%
    product = pd.read_sql("SELECT * FROM product", sqliteConnection)
    order_details = pd.read_sql("SELECT * FROM order_details", sqliteConnection)
    returned_item = pd.read_sql("SELECT * FROM returned_item", sqliteConnection)

    df_merge = pd.merge(product, order_details, on='PRODUCT_NUMBER')

    df_filter = df_merge[df_merge['UNIT_SALE_PRICE'] > 500]
    df_no_return = df_filter[~df_filter['ORDER_DETAIL_CODE'].isin(returned_item['ORDER_DETAIL_CODE'])]

    df_res = df_no_return[['PRODUCT_NAME']].drop_duplicates()
    df_res


    # %% [markdown]
    # Geef een overzicht met daarin per (achternaam van) medewerker of hij/zij manager is of niet, door deze informatie toe te voegen als extra 'Ja/Nee'-kolom.<br>
    # Hint: gebruik een for-loop waarin je o.a. bepaalt of het woord 'Manager' in de functie (position_en) staat. (2 kolommen, 102 rijen).

    # %%
    sales_staff = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)

    sales_staff['Is_Manager'] = ['Yes' if 'Manager' in position else 'No' for position in sales_staff['POSITION_EN']]

    df_res = sales_staff[['LAST_NAME', 'Is_Manager']]
    df_res


    # %% [markdown]
    # Met de onderstaande code laat je Python het huidige jaar uitrekenen.

    # %%
    from datetime import date
    date.today().year

    # %% [markdown]
    # Met de onderstaande code selecteer je op een bepaald jaartal uit een datum.

    # %%
    from datetime import datetime

    date_str = '16-8-2013'
    date_format = '%d-%m-%Y'
    date_obj = datetime.strptime(date_str, date_format)

    date_obj.year

    # %% [markdown]
    # Geef met behulp van bovenstaande hulpcode een overzicht met daarin op basis van het aantal jaar dat iemand in dienst is of een medewerker ‘kort in dienst’ (minder dan 25 jaar in dienst) of een ‘lang in dienst’ (groter gelijk dan 12 jaar in dienst) is. Geef daarbij per medewerker in een aparte kolom zowel ‘kort in dienst’ als ‘lang in dienst’ aan. Gebruik (wederom) een for-loop.<br>
    # (2 kolommen, 102 rijen) 

    # %%
    from datetime import datetime

    sales_staff = pd.read_sql("SELECT * FROM sales_staff", sqliteConnection)

    dienst_status = []

    for index, row in sales_staff.iterrows():
        in_dienst_str = row['DATE_HIRED']
        in_dienst = datetime.strptime(in_dienst_str, '%Y-%m-%d')
        years_in_service = (datetime.today() - in_dienst).days // 365
        
        if years_in_service < 25:
            dienst_status.append('kort in dienst')
        elif years_in_service >= 12:
            dienst_status.append('lang in dienst')
        else:
            dienst_status.append('')

    sales_staff['Dienst_Status'] = dienst_status

    df_res = sales_staff[['LAST_NAME', 'Dienst_Status']]
    df_res


    # %% [markdown]
    # ## Van Jupyter Notebook naar Pythonproject

    # %% [markdown]
    # 1. Richt de map waarin jullie tot nu toe hebben gewerkt in volgens de mappenstructuur uit de slides.
    # 2. Maak van de ontstane mappenstructuur een Pythonproject dat uitvoerbaar is vanuit de terminal. Maak daarin een .py-bestand dat minstens 5 antwoorden uit dit notebook (in de vorm van een DataFrame) exporteert naar Excelbestanden. Alle notebooks mogen als notebook blijven bestaan.
    # 3. Zorg ervoor dat dit Pythonproject zijn eigen repo heeft op Github. Let op: je virtual environment moet <b><u>niet</u></b> meegaan naar Github.
    # 
    # Je mag tijdens dit proces je uit stap 1 ontstane mappenstructuur aanpassen, zolang je bij het beoordelingsmoment kan verantwoorden wat de motivatie hierachter is. De slides verplichten je dus nergens toe.


