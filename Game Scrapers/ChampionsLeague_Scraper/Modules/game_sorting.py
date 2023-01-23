import sqlite3
import xlsxwriter


class GameSorting:

    def __init__(self):
        # Creates a connection with the database
        self.con = sqlite3.connect("ChamoinsLeague.db")

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

        letter_dict = {
            1: "A",
            2: "B",
            3: "C",
            4: "D",
            5: "E",
            6: "F",
            7: "G",
            8: "H",
            9: "I",
            10: "J"
        }

        # Opens the excel file
        workbook = xlsxwriter.Workbook('Champions League SpreadSheet.xlsx')
        worksheet = workbook.add_worksheet()

        # Variable for the row in wich to write on
        row_counter = 1

        cell_format = workbook.add_format()
        cell_format.set_bg_color("yellow")

        for game in arb_list:

            # Extract the odds from the game list
            odds = []
            for item in game:
                if type(item) != str:
                    odds.append(item)

            # Divide the odds in two lists for odd1 and odd2
            odds_1 = []
            odds_2 = []

            i = 0

            for odd in odds:
                i += 1

                if i % 2 != 0:
                    odds_1.append(odd)
                else:
                    odds_2.append(odd)

            # Find the biggest odds
            odds_1.sort()
            odds_2.sort()

            biggest_1 = odds_1[-1]
            biggest_2 = odds_2[-1]

            # Write the arbitrage value
            arb = (100 / biggest_1) + (100 / biggest_2)

            if arb < 100:
                worksheet.write(f"A{row_counter}", f"{arb:.2f}", cell_format)
            else:
                worksheet.write(f"A{row_counter}", f"{arb:.2f}")

            # Write the team names
            worksheet.write(f"A{row_counter + 1}", game[0])
            worksheet.write(f"A{row_counter + 2}", game[1])

            column_num = 1
            row_addition = 0

            for item in game[2:]:

                # If the item is a string its the site name and we update the number of the column and the row_addition
                if type(item) == str:
                    row_addition = 0
                    column_num += 1
                    worksheet.write(f"{letter_dict[column_num ]}{row_counter}", item)
                else:
                    row_addition += 1

                    if row_addition == 1:

                        if float(item) == biggest_1:
                            worksheet.write(f"{letter_dict[column_num ]}{row_counter + row_addition}", item, cell_format)
                        else:
                            worksheet.write(f"{letter_dict[column_num ]}{row_counter + row_addition}", item)

                    elif row_addition == 2:

                        if float(item) == biggest_2:
                            worksheet.write(f"{letter_dict[column_num ]}{row_counter + row_addition}", item, cell_format)
                        else:
                            worksheet.write(f"{letter_dict[column_num ]}{row_counter + row_addition}", item)

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


