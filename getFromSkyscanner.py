import csv
from skyscanner import FlightsCache

flights_cache_service = FlightsCache('')

with open('prices.csv', 'a+') as csvprecos:
    fieldnames = ['Origem', 'Destino', 'DataPesquisa', 'DataCotacao', 'DataViagem', 'Preco', 'Direto']

    writer = csv.DictWriter(csvprecos, fieldnames=fieldnames)

    writer.writeheader()

with open('viagens.csv', 'r') as csvfile:
    csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
    for row in csvreader:

        origem = row[0]
        destino = row[1]
        datapesquisa = row[2]

        result = flights_cache_service.get_cheapest_price_by_date(
            market='BR',
            currency='BRL',
            locale='pt-BR',
            originplace=origem,
            destinationplace=destino,
            outbounddate=datapesquisa).parsed

        data = result

        if ('Quotes' in data and data['Quotes']):
            datacotacao = data['Quotes'][0]['QuoteDateTime']
            dataviagem = data['Quotes'][0]['OutboundLeg']['DepartureDate']
            preco = data['Quotes'][0]['MinPrice']
            direto = data['Quotes'][0]['Direct']

            with open('prices.csv', 'a+') as csvprecos:
                writer = csv.DictWriter(csvprecos, fieldnames=fieldnames)
                writer.writerow({'Origem': origem, 'Destino': destino, 'DataPesquisa': datapesquisa,
                                 'DataCotacao': datacotacao, "DataViagem": dataviagem, "Preco": preco,
                                 "Direto": direto})
        else:
            with open('prices.csv', 'a+') as csvprecos:
                writer = csv.DictWriter(csvprecos, fieldnames=fieldnames)
                writer.writerow({'Origem': origem, 'Destino': destino, 'DataPesquisa': datapesquisa,
                             'DataCotacao': "NAO ENCONTRADA"})
