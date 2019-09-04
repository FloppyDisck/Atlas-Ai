with open('data/locations/allCountries-unformated.txt') as dataset:
    writeFile = open('data/locations/countriesLookupNOCAPS.txt', 'w')
    for data in dataset:
        dataList = data.split("\t")
        if int(dataList[14]) > 5000:
            print(dataList[2])
            writeFile.write(dataList[2].lower() + '\n')
    writeFile.close()