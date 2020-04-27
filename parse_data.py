import data_parser.parser

# Génére un fichier .csv par device, les fichiers sont modifiés pour être plus facilement utilisable :
# - On transforme les IDs des lieux en INT
# - On retire la colonne permettant d'identifier le device

FILE_PATH = "data/data_4.csv"
header, devices = data_parser.parser.parse(FILE_PATH)

for device in devices.keys():
    data_parser.parser.write_data("data/" + device + ".csv", devices[device], header)
