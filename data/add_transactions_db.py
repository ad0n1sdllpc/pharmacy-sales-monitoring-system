import random
from datetime import datetime, timedelta
import sqlite3
from random import randint

connection = sqlite3.connect('transactions.db')
cursor = connection.cursor()

medicine_data = {
    "1001": {
        "name": "Biogesic",
        "quantity": 60,
        "bin no": "B1",
        "expiry date": "2024-12-23",
        "cost": 8
    },
    "1002": {
        "name": "Neozep",
        "quantity": 57,
        "bin no": "B1",
        "expiry date": "2026-08-14",
        "cost": 8
    },
    "1003": {
        "name": "Cetirizine",
        "quantity": 45,
        "bin no": "B2",
        "expiry date": "2025-07-23",
        "cost": 8
    },
    "1004": {
        "name": "Strepsils",
        "quantity": 44,
        "bin no": "B4",
        "expiry date": "2025-04-14",
        "cost": 5
    },
    "1005": {
        "name": "Desoft eye drops",
        "quantity": 11,
        "bin no": "B3",
        "expiry date": "2022-12-23",
        "cost": 20
    },
    "1006": {
        "name": "Rantac",
        "quantity": 36,
        "bin no": "B3",
        "expiry date": "2023-04-14",
        "cost": 2
    },
    "1007": {
        "name": "Soframycin",
        "quantity": 100,
        "bin no": "B5",
        "expiry date": "2022-12-23",
        "cost": 25
    },
    "1008": {
        "name": "Epiduo",
        "quantity": 60,
        "bin no": "B6",
        "expiry date": "2023-04-14",
        "cost": 100
    },
    "1009": {
        "name": "Decolgen",
        "quantity": 100,
        "bin no": "B7",
        "expiry date": "2022-12-23",
        "cost": 11
    },
    "1010": {
        "name": "Alaxan",
        "quantity": 2,
        "bin no": "B8",
        "expiry date": "2026-04-14",
        "cost": 11
    },
    "1011": {
        "name": "Bioflu",
        "quantity": 28,
        "bin no": "B2",
        "expiry date": "2024-09-30",
        "cost": 15
    },
    "1012": {
        "name": "Salabat",
        "quantity": 50,
        "bin no": "B3",
        "expiry date": "2025-06-15",
        "cost": 5
    },
    "1013": {
        "name": "Calpol",
        "quantity": 70,
        "bin no": "B4",
        "expiry date": "2024-11-10",
        "cost": 10
    },
    "1014": {
        "name": "Mefenamic Acid",
        "quantity": 37,
        "bin no": "B5",
        "expiry date": "2025-03-22",
        "cost": 7
    },
    "1015": {
        "name": "Loperamide",
        "quantity": 25,
        "bin no": "B6",
        "expiry date": "2023-08-18",
        "cost": 6
    },
    "1016": {
        "name": "Betadine",
        "quantity": 60,
        "bin no": "B7",
        "expiry date": "2024-05-12",
        "cost": 12
    },
    "1017": {
        "name": "Vicks Vaporub",
        "quantity": 20,
        "bin no": "B8",
        "expiry date": "2023-12-30",
        "cost": 8
    },
    "1018": {
        "name": "Enervon",
        "quantity": 86,
        "bin no": "B9",
        "expiry date": "2024-07-25",
        "cost": 18
    },
    "1019": {
        "name": "Dolfenal",
        "quantity": 15,
        "bin no": "B10",
        "expiry date": "2025-02-05",
        "cost": 9
    },
    "1020": {
        "name": "Gelmicin",
        "quantity": 55,
        "bin no": "B11",
        "expiry date": "2023-11-15",
        "cost": 25
    },
    "1021": {
        "name": "Biogesic PM",
        "quantity": 35,
        "bin no": "B12",
        "expiry date": "2024-10-15",
        "cost": 10
    },
    "1022": {
        "name": "Decutan",
        "quantity": 22,
        "bin no": "B13",
        "expiry date": "2025-04-01",
        "cost": 35
    },
    "1023": {
        "name": "Ascof Lagundi",
        "quantity": 60,
        "bin no": "B14",
        "expiry date": "2024-12-28",
        "cost": 18
    },
    "1024": {
        "name": "Nasatapp",
        "quantity": 30,
        "bin no": "B15",
        "expiry date": "2025-07-10",
        "cost": 14
    },
    "1025": {
        "name": "Dexa Rhinaspray",
        "quantity": 18,
        "bin no": "B16",
        "expiry date": "2023-09-22",
        "cost": 28
    },
    "1026": {
        "name": "Flanax",
        "quantity": 50,
        "bin no": "B17",
        "expiry date": "2024-02-14",
        "cost": 12
    },
    "1027": {
        "name": "Imodium",
        "quantity": 38,
        "bin no": "B18",
        "expiry date": "2023-10-30",
        "cost": 15
    },
    "1028": {
        "name": "Ceelin Plus",
        "quantity": 50,
        "bin no": "B19",
        "expiry date": "2024-05-18",
        "cost": 20
    },
    "1029": {
        "name": "Rhinocort Nasal Spray",
        "quantity": 25,
        "bin no": "B20",
        "expiry date": "2023-12-15",
        "cost": 30
    },
    "1030": {
        "name": "Biogesic Forte",
        "quantity": 15,
        "bin no": "B21",
        "expiry date": "2025-01-20",
        "cost": 12
    },
    "1031": {
        "name": "Dolocold",
        "quantity": 25,
        "bin no": "B8",
        "expiry date": "2024-11-30",
        "cost": 14
    },
    "1032": {
        "name": "Pharex Vitamin B-Complex",
        "quantity": 60,
        "bin no": "B3",
        "expiry date": "2024-09-10",
        "cost": 25
    },
    "1033": {
        "name": "Sinutab",
        "quantity": 27,
        "bin no": "B7",
        "expiry date": "2025-03-05",
        "cost": 18
    },
    "1034": {
        "name": "Omeprazole",
        "quantity": 35,
        "bin no": "B5",
        "expiry date": "2023-08-28",
        "cost": 8
    },
    "1035": {
        "name": "Vitabiotics Wellwoman",
        "quantity": 20,
        "bin no": "B2",
        "expiry date": "2025-06-20",
        "cost": 30
    },
    "1036": {
        "name": "Panadol Extend",
        "quantity": 30,
        "bin no": "B1",
        "expiry date": "2024-02-10",
        "cost": 15
    },
    "1037": {
        "name": "Bioflu Kids",
        "quantity": 40,
        "bin no": "B9",
        "expiry date": "2025-01-15",
        "cost": 12
    },
    "1038": {
        "name": "Betnovate Cream",
        "quantity": 15,
        "bin no": "B4",
        "expiry date": "2023-11-05",
        "cost": 22
    },
    "1039": {
        "name": "Redoxon",
        "quantity": 55,
        "bin no": "B10",
        "expiry date": "2024-07-22",
        "cost": 20
    },
    "1040": {
        "name": "Dulcolax",
        "quantity": 28,
        "bin no": "B6",
        "expiry date": "2023-10-18",
        "cost": 10
    },
    "1041": {
        "name": "Ampalaya Plus",
        "quantity": 27,
        "bin no": "B8",
        "expiry date": "2025-04-30",
        "cost": 16
    },
    "1042": {
        "name": "Naproxen",
        "quantity": 18,
        "bin no": "B1",
        "expiry date": "2023-09-12",
        "cost": 7
    },
    "1043": {
        "name": "Mosegor Vita",
        "quantity": 30,
        "bin no": "B3",
        "expiry date": "2024-05-25",
        "cost": 28
    },
    "1044": {
        "name": "Carbocisteine",
        "quantity": 23,
        "bin no": "B5",
        "expiry date": "2023-12-08",
        "cost": 15
    },
    "1045": {
        "name": "Gofen",
        "quantity": 40,
        "bin no": "B2",
        "expiry date": "2024-10-10",
        "cost": 11
    },
    "1046": {
        "name": "Stresstabs",
        "quantity": 65,
        "bin no": "B7",
        "expiry date": "2024-08-15",
        "cost": 28
    },
    "1047": {
        "name": "Poten-Cee + Zinc",
        "quantity": 42,
        "bin no": "B6",
        "expiry date": "2023-07-20",
        "cost": 14
    },
    "1048": {
        "name": "Advil",
        "quantity": 8,
        "bin no": "B9",
        "expiry date": "2025-02-28",
        "cost": 12
    },
    "1049": {
        "name": "Vicks Formula 44",
        "quantity": 30,
        "bin no": "B4",
        "expiry date": "2024-12-12",
        "cost": 16
    },
    "1050": {
        "name": "Bepanthen Ointment",
        "quantity": 15,
        "bin no": "B10",
        "expiry date": "2023-11-02",
        "cost": 18
    },
    "1051": {
        "name": "Lactacyd Feminine Wash",
        "quantity": 55,
        "bin no": "B8",
        "expiry date": "2024-06-18",
        "cost": 14
    },
    "1052": {
        "name": "Omnaris Nasal Spray",
        "quantity": 25,
        "bin no": "B5",
        "expiry date": "2023-10-30",
        "cost": 30
    },
    "1053": {
        "name": "Colchicine",
        "quantity": 15,
        "bin no": "B7",
        "expiry date": "2024-03-15",
        "cost": 15
    },
    "1054": {
        "name": "Centrum Silver",
        "quantity": 40,
        "bin no": "B3",
        "expiry date": "2025-05-20",
        "cost": 28
    },
    "1055": {
        "name": "Bisolvon",
        "quantity": 3,
        "bin no": "B9",
        "expiry date": "2023-12-10",
        "cost": 18
    },
    "1056": {
        "name": "Neutrogena Hydro Boost",
        "quantity": 30,
        "bin no": "B1",
        "expiry date": "2024-08-02",
        "cost": 25
    },
    "1057": {
        "name": "Rexidol Forte",
        "quantity": 33,
        "bin no": "B10",
        "expiry date": "2024-04-18",
        "cost": 10
    },
    "1058": {
        "name": "Calcium Sandoz",
        "quantity": 15,
        "bin no": "B4",
        "expiry date": "2023-09-05",
        "cost": 20
    },
    "1059": {
        "name": "Benadryl",
        "quantity": 20,
        "bin no": "B1",
        "expiry date": "2024-01-30",
        "cost": 8
    },
    "1060": {
        "name": "Salicylic Acid Ointment",
        "quantity": 20,
        "bin no": "B6",
        "expiry date": "2025-03-08",
        "cost": 12
    },
    "1061": {
        "name": "Dermovate Cream",
        "quantity": 22,
        "bin no": "B3",
        "expiry date": "2023-11-20",
        "cost": 25
    },
    "1062": {
        "name": "Antamin Syrup",
        "quantity": 2,
        "bin no": "B7",
        "expiry date": "2024-07-15",
        "cost": 14
    },
    "1063": {
        "name": "Otrivin Nasal Spray",
        "quantity": 18,
        "bin no": "B2",
        "expiry date": "2024-02-28",
        "cost": 10
    },
    "1064": {
        "name": "Pamprin",
        "quantity": 25,
        "bin no": "B5",
        "expiry date": "2025-06-10",
        "cost": 18
    },
    "1065": {
        "name": "Dermovate Ointment",
        "quantity": 33,
        "bin no": "B8",
        "expiry date": "2024-10-28",
        "cost": 22
    },
    "1066": {
        "name": "Tranexamic Acid",
        "quantity": 28,
        "bin no": "B4",
        "expiry date": "2023-12-15",
        "cost": 15
    },
    "1067": {
        "name": "Benzydamine",
        "quantity": 15,
        "bin no": "B9",
        "expiry date": "2024-05-02",
        "cost": 28
    },
    "1068": {
        "name": "Celecoxib",
        "quantity": 30,
        "bin no": "B2",
        "expiry date": "2023-09-18",
        "cost": 12
    },
    "1069": {
        "name": "Calmoseptine Ointment",
        "quantity": 45,
        "bin no": "B6",
        "expiry date": "2024-03-30",
        "cost": 16
    },
    "1070": {
        "name": "Diclofenac Gel",
        "quantity": 20,
        "bin no": "B10",
        "expiry date": "2025-01-12",
        "cost": 14
    },
    "1071": {
        "name": "Ceelin Drops",
        "quantity": 18,
        "bin no": "B8",
        "expiry date": "2023-07-22",
        "cost": 12
    },
    "1072": {
        "name": "Tums",
        "quantity": 35,
        "bin no": "B4",
        "expiry date": "2024-11-05",
        "cost": 8
    },
    "1073": {
        "name": "Zyrtec",
        "quantity": 55,
        "bin no": "B1",
        "expiry date": "2024-09-20",
        "cost": 18
    },
    "1074": {
        "name": "Betadine Mouthwash",
        "quantity": 42,
        "bin no": "B7",
        "expiry date": "2023-10-10",
        "cost": 14
    },
    "1075": {
        "name": "Lansoprazole",
        "quantity": 4,
        "bin no": "B2",
        "expiry date": "2025-02-28",
        "cost": 10
    },
    "1076": {
        "name": "Multivitamins with Iron",
        "quantity": 22,
        "bin no": "B9",
        "expiry date": "2024-08-15",
        "cost": 20
    },
    "1077": {
        "name": "Dermoplast",
        "quantity": 25,
        "bin no": "B6",
        "expiry date": "2023-12-30",
        "cost": 16
    },
    "1078": {
        "name": "Mucinex",
        "quantity": 40,
        "bin no": "B4",
        "expiry date": "2024-06-18",
        "cost": 22
    },
    "1079": {
        "name": "Ibuprofen",
        "quantity": 33,
        "bin no": "B8",
        "expiry date": "2024-04-10",
        "cost": 10
    },
    "1080": {
        "name": "Tretinoin Cream",
        "quantity": 20,
        "bin no": "B1",
        "expiry date": "2023-11-22",
        "cost": 28
    },
    "1081": {
        "name": "Dexamethasone",
        "quantity": 18,
        "bin no": "B7",
        "expiry date": "2024-05-05",
        "cost": 25
    },
    "1082": {
        "name": "Neozep Forte",
        "quantity": 45,
        "bin no": "B2",
        "expiry date": "2025-01-18",
        "cost": 16
    },
    "1083": {
        "name": "Salonpas",
        "quantity": 3,
        "bin no": "B10",
        "expiry date": "2024-07-02",
        "cost": 14
    },
    "1084": {
        "name": "Isopropyl Alcohol",
        "quantity": 22,
        "bin no": "B5",
        "expiry date": "2023-10-15",
        "cost": 5
    },
    "1085": {
        "name": "Berocca",
        "quantity": 35,
        "bin no": "B3",
        "expiry date": "2024-02-28",
        "cost": 20
    },
    "1086": {
        "name": "Minoxidil",
        "quantity": 28,
        "bin no": "B6",
        "expiry date": "2023-08-10",
        "cost": 30
    },
    "1088": {
        "name": "Claritin",
        "quantity": 30,
        "bin no": "B9",
        "expiry date": "2024-12-10",
        "cost": 18
    },
    "1089": {
        "name": "Mebendazole",
        "quantity": 25,
        "bin no": "B4",
        "expiry date": "2023-09-25",
        "cost": 8
    },
    "1090": {
        "name": "Mega-Malunggay",
        "quantity": 18,
        "bin no": "B10",
        "expiry date": "2024-04-12",
        "cost": 12
    },
    "1091": {
        "name": "Naproxen Sodium",
        "quantity": 33,
        "bin no": "B5",
        "expiry date": "2024-10-30",
        "cost": 14
    },
    "1092": {
        "name": "Ascorbic Acid",
        "quantity": 22,
        "bin no": "B3",
        "expiry date": "2023-11-15",
        "cost": 10
    },
    "1093": {
        "name": "Hydrogen Peroxide",
        "quantity": 28,
        "bin no": "B6",
        "expiry date": "2024-05-28",
        "cost": 5
    },
    "1094": {
        "name": "Moringa Capsules",
        "quantity": 40,
        "bin no": "B2",
        "expiry date": "2025-01-10",
        "cost": 18
    },
    "1095": {
        "name": "Voltaren Gel",
        "quantity": 15,
        "bin no": "B9",
        "expiry date": "2023-08-22",
        "cost": 22
    },
    "1096": {
        "name": "Folic Acid",
        "quantity": 45,
        "bin no": "B7",
        "expiry date": "2024-02-15",
        "cost": 8
    },
    "1097": {
        "name": "Vicks Vaporub",
        "quantity": 18,
        "bin no": "B4",
        "expiry date": "2023-12-10",
        "cost": 12
    },
    "1098": {
        "name": "Paracetamol",
        "quantity": 30,
        "bin no": "B10",
        "expiry date": "2024-07-18",
        "cost": 16
    },
    "1099": {
        "name": "Epsom Salt",
        "quantity": 25,
        "bin no": "B8",
        "expiry date": "2023-09-28",
        "cost": 14
    },
    "1100": {
        "name": "Gaviscon",
        "quantity": 4,
        "bin no": "B1",
        "expiry date": "2024-04-05",
        'cost': 20
    }
}


def generate_insert_queries(year, limit=1500):
    queries = []
    start_date = datetime(year, 1, 1, 0, 0)  # Start date without specific time
    end_date = datetime(year, 12, 31, 23, 59)  # End date with time

    for _ in range(limit):
        current_date = start_date + timedelta(days=randint(0, (end_date - start_date).days),
                                             hours=randint(0, 23),
                                             minutes=randint(0, 59))

        for medicine_id, data in medicine_data.items():
            quantity = random.randint(1, data["quantity"])
            amount = quantity * data["cost"]
            transaction_date = current_date.strftime('%Y-%m-%d %H:%M')

            query = f"INSERT INTO transactions (medicine_id, medicine_name, quantity, amount, transaction_date) VALUES ({medicine_id}, '{data['name']}', {quantity}, {amount}, '{transaction_date}');"
            queries.append(query)

            if len(queries) >= limit:
                break

    return queries

# ...

year_to_generate = 2010
insert_queries = generate_insert_queries(year_to_generate, limit=1500)

for query in insert_queries:
    cursor.execute(query)

# Commit the changes to the database
connection.commit()


# Close the database connection
connection.close()