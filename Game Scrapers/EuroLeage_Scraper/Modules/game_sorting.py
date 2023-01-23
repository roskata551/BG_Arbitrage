import sqlite3
import xlsxwriter


class GameSorting:

    def __init__(self):
        # Creates a connection with the database
        self.con = sqlite3.connect("EuroLeague.db")

        # Creates a cursor to operate in the database
        self.cur = self.con.cursor()

        # Creates a list with the name of the sites
        self.names = ["bet365", "betano", "bwin", "efbet", "sesame"]

        self.main()

    def read_games(self):

        # Creates a dictionary for the games of the sites
        games_dict = {}

        # Goes through the site names
        for name in self.names:
            # Selects the table with the site name
            self.cur.execute(f"""SELECT * FROM {name}_games""")

            # Gets all the data from the table
            games = self.cur.fetchall()

            # Adds a row to the games dict with the site name as a key and a list for the games
            games_dict.update({f"{name}": []})

            # Adds the games to the row created
            for game in games:
                ls = [game[0], game[1], game[2], game[3]]

                games_dict[f"{name}"].append(ls)

        return games_dict

    def get_name_dict(self):
        # Selects the table with the site name
        self.cur.execute(f"""SELECT * FROM name_dictionary""")

        # Gets all the data from the table
        name_dict = self.cur.fetchall()

        return name_dict

    def change_names(self, games_dict, name_dict):

        # Goes through the names of the sites
        for site_name in self.names:

            # Goes through the games list from the game dictionaries
            for game in games_dict[site_name]:

                # Goes through the names tuples from the names dictionary
                for name_list in name_dict:

                    if game[0] in name_list:
                        game[0] = name_list[0]

                    if game[1] in name_list:
                        game[1] = name_list[0]

    def arrange_names(self, games_dict):

        for betano_game in games_dict["betano"]:

            for name in self.names:

                if name == "betano":
                    continue

                for game in games_dict[f"{name}"]:

                    if betano_game[0] == game[0] or betano_game[0] == game[1]:

                        if betano_game[1] == game[0] or betano_game[1] == game[1]:

                            if betano_game[0] != game[0]:

                                game[0], game[1] = game[1], game[0]
                                game[2], game[3] = game[3], game[2]

        return

    def match_games(self, games_dict):

        arb_list = []

        for betano_game in games_dict["betano"]:

            game_info = [betano_game[0], betano_game[1], "betano", betano_game[2], betano_game[3]]

            for site_name in self.names:

                if site_name == "betano":
                    continue

                for game in games_dict[site_name]:

                    if game[0] == betano_game[0] and game[1] == betano_game[1]:

                        game_info.append(site_name)
                        game_info.append(game[2])
                        game_info.append(game[3])

            arb_list.append(game_info)

        return arb_list

    def write_excel(self, arb_list):

        # Opens the excel file
        workbook = xlsxwriter.Workbook('EuroLeague SpreadSheet.xlsx')
        worksheet = workbook.add_worksheet()

        # Variable for the row in wich to write on
        row_counter = 1

        data_counter = 0

        for game in arb_list:

            odds = []

            for item in game:
                if type(item) != str:
                    odds.append(item)

            odds_1 = []
            odds_2 = []

            i = 0

            for odd in odds:
                i += 1

                if i % 2 != 0:
                    odds_1.append(odd)
                else:
                    odds_2.append(odd)

            odds_1.sort()
            odds_2.sort()

            biggest_1 = odds_1[-1]
            biggest_2 = odds_2[-1]

            arb = (100 / biggest_1) + (100 / biggest_2)

            cell_format = workbook.add_format()
            cell_format.set_bg_color("yellow")

            if arb < 100:
                worksheet.write(f"A{row_counter}", f"{arb:.2f}", cell_format)
            else:
                worksheet.write(f"A{row_counter}", f"{arb:.2f}")

            worksheet.write(f"A{row_counter + 1}", game[0])
            worksheet.write(f"A{row_counter + 2}", game[1])

            worksheet.write(f"B{row_counter}", game[2])

            if game[3] == biggest_1:
                worksheet.write(f"B{row_counter + 1}", game[3], cell_format)
            else:
                worksheet.write(f"B{row_counter + 1}", game[3])

            if game[4] == biggest_2:
                worksheet.write(f"B{row_counter + 2}", game[4], cell_format)
            else:
                worksheet.write(f"B{row_counter + 2}", game[4])

            if len(game) == 5:
                row_counter += 4
                continue

            worksheet.write(f"C{row_counter}", game[5])

            if game[6] == biggest_1:
                worksheet.write(f"C{row_counter + 1}", game[6], cell_format)
            else:
                worksheet.write(f"C{row_counter + 1}", game[6])

            if game[7] == biggest_2:
                worksheet.write(f"C{row_counter + 2}", game[7], cell_format)
            else:
                worksheet.write(f"C{row_counter + 2}", game[7])

            if len(game) == 8:
                row_counter += 4
                continue

            worksheet.write(f"D{row_counter}", game[8])

            if game[9] == biggest_1:
                worksheet.write(f"D{row_counter + 1}", game[9], cell_format)
            else:
                worksheet.write(f"D{row_counter + 1}", game[9])

            if game[10] == biggest_2:
                worksheet.write(f"D{row_counter + 2}", game[10], cell_format)
            else:
                worksheet.write(f"D{row_counter + 2}", game[10])

            if len(game) == 11:
                row_counter += 4
                continue

            worksheet.write(f"E{row_counter}", game[11])

            if game[12] == biggest_1:
                worksheet.write(f"E{row_counter + 1}", game[12], cell_format)
            else:
                worksheet.write(f"E{row_counter + 1}", game[12])

            if game[13] == biggest_2:
                worksheet.write(f"E{row_counter + 2}", game[13], cell_format)
            else:
                worksheet.write(f"E{row_counter + 2}", game[13])

            if len(game) == 14:
                row_counter += 4
                continue

            worksheet.write(f"F{row_counter}", game[14])

            if game[15] == biggest_1:
                worksheet.write(f"F{row_counter + 1}", game[15], cell_format)
            else:
                worksheet.write(f"F{row_counter + 1}", game[15])

            if game[16] == biggest_2:
                worksheet.write(f"F{row_counter + 2}", game[16], cell_format)
            else:
                worksheet.write(f"F{row_counter + 2}", game[16])

            if len(game) == 17:
                row_counter += 4
                continue

            worksheet.write(f"G{row_counter}", game[17])

            if game[18] == biggest_1:
                worksheet.write(f"G{row_counter + 1}", game[18], cell_format)
            else:
                worksheet.write(f"G{row_counter + 1}", game[18])

            if game[19] == biggest_2:
                worksheet.write(f"G{row_counter + 2}", game[19], cell_format)
            else:
                worksheet.write(f"G{row_counter + 2}", game[19])

            if len(game) == 20:
                row_counter += 4
                continue

            worksheet.write(f"H{row_counter}", game[20])

            if game[21] == biggest_1:
                worksheet.write(f"H{row_counter + 1}", game[21], cell_format)
            else:
                worksheet.write(f"H{row_counter + 1}", game[21])

            if game[22] == biggest_2:
                worksheet.write(f"H{row_counter + 2}", game[22], cell_format)
            else:
                worksheet.write(f"H{row_counter + 2}", game[22])

            if len(game) == 23:
                row_counter += 4
                continue

            worksheet.write(f"I{row_counter}", game[23])

            if game[24] == biggest_1:
                worksheet.write(f"I{row_counter + 1}", game[24], cell_format)
            else:
                worksheet.write(f"I{row_counter + 1}", game[24])

            if game[25] == biggest_2:
                worksheet.write(f"I{row_counter + 2}", game[25], cell_format)
            else:
                worksheet.write(f"I{row_counter + 2}", game[25])

            if len(game) == 26:
                row_counter += 4
                continue

            worksheet.write(f"J{row_counter}", game[26])

            if game[27] == biggest_1:
                worksheet.write(f"J{row_counter + 1}", game[27], cell_format)
            else:
                worksheet.write(f"J{row_counter + 1}", game[27])

            if game[28] == biggest_2:
                worksheet.write(f"J{row_counter + 2}", game[28], cell_format)
            else:
                worksheet.write(f"J{row_counter + 2}", game[28])

            row_counter += 4

        workbook.close()

    def main(self):
        games_dict = self.read_games()

        name_dict = self.get_name_dict()

        self.change_names(games_dict, name_dict)

        self.arrange_names(games_dict)

        arb_list = self.match_games(games_dict)

        self.write_excel(arb_list)


def start():
    scraper = GameSorting()

if "__main__" == __name__:
    start()


