import xlsxwriter


class DataComparing:

    def __init__(self, betano_data, bwin_data):

        self.main(betano_data, bwin_data)

    def paired_data(self, betano_data, bwin_data):

        paired_data = {}

        for be_name in betano_data:

            for bw_name in bwin_data:

                ls_be_names = sorted(be_name.split(' vs '))
                ls_bw_names = sorted(bw_name.split(' vs '))

                if ls_be_names == ls_bw_names:

                    game_dic = {}

                    for be_score in betano_data[be_name]:

                        for bw_score in bwin_data[bw_name]:

                            if be_score == bw_score:

                                game_dic[be_score] = [betano_data[be_name][be_score][0], betano_data[be_name][be_score][1],
                                                      bwin_data[bw_name][bw_score][0], bwin_data[bw_name][bw_score][1]]

                    paired_data[be_name] = game_dic

        return paired_data

    def find_arb(self, odds):

        odd1 = 0
        odd2 = 0

        if odds[0] > odds[2]:
            odd1 = odds[0]
        else:
            odd1 = odds[2]

        if odds[1] > odds[3]:
            odd2 = odds[1]
        else:
            odd2 = odds[3]

        arb = float(f"{(100 / odd1) + (100 / odd2):.2f}")

        return arb

    def find_highest_odds(self, odds):

        odd1 = 0
        odd2 = 0

        if odds[0] > odds[2]:
            odd1 = odds[0]
        else:
            odd1 = odds[2]

        if odds[1] > odds[3]:
            odd2 = odds[1]
        else:
            odd2 = odds[3]

        return odd1, odd2

    def write_to_excel(self, paired_data):

        # Opens the excel file
        workbook = xlsxwriter.Workbook('Total Score.xlsx')
        worksheet = workbook.add_worksheet()

        headers_border_1 = workbook.add_format()
        headers_border_1.set_bottom(2)
        headers_border_1.set_right(2)
        headers_border_1.set_top(2)
        headers_border_1.set_bold(True)
        headers_border_1.set_color('#000000')
        headers_border_1.set_align('center')
        headers_border_1.set_align('vcenter')

        headers_border_2 = workbook.add_format()
        headers_border_2.set_bottom(2)
        headers_border_2.set_top(2)
        headers_border_2.set_bold(True)
        headers_border_2.set_color('#000000')
        headers_border_2.set_align('center')
        headers_border_2.set_align('vcenter')

        center_format = workbook.add_format()
        center_format.set_align('center')
        center_format.set_align('vcenter')

        center_format_w = workbook.add_format()
        center_format_w.set_align('center')
        center_format_w.set_align('vcenter')
        center_format_w.set_fg_color("yellow")

        bottom_border = workbook.add_format()
        bottom_border.set_bottom(2)
        bottom_border.set_color('#000000')
        bottom_border.set_align('center')
        bottom_border.set_align('vcenter')

        bottom_border_w = workbook.add_format()
        bottom_border_w.set_bottom(2)
        bottom_border_w.set_color('#000000')
        bottom_border_w.set_align('center')
        bottom_border_w.set_align('vcenter')
        bottom_border_w.set_fg_color("yellow")

        bottom_right_border = workbook.add_format()
        bottom_right_border.set_bottom(2)
        bottom_right_border.set_right(2)
        bottom_right_border.set_color('#000000')
        bottom_right_border.set_align('center')
        bottom_right_border.set_align('vcenter')

        arb_win_format = workbook.add_format()
        arb_win_format.set_fg_color("#47d147")
        arb_win_format.set_bottom(2)
        arb_win_format.set_right(2)
        arb_win_format.set_color('#000000')
        arb_win_format.set_align('center')
        arb_win_format.set_align('vcenter')

        arb_lose_format = workbook.add_format()
        arb_lose_format.set_bottom(2)
        arb_lose_format.set_right(2)
        arb_lose_format.set_color('#000000')
        arb_lose_format.set_align('center')
        arb_lose_format.set_align('vcenter')

        row_counter = 1

        for game in paired_data:

            worksheet.write(f"A{row_counter}", game, headers_border_2)
            worksheet.write(f"B{row_counter}", "Betano", headers_border_2)
            worksheet.write(f"C{row_counter}", "Bwin", headers_border_2)
            worksheet.write(f"D{row_counter}", "Arb", headers_border_1)
            worksheet.set_row(row_counter - 1, 25)

            row_add = 1

            for score in paired_data[game]:
                current_row = row_counter + row_add
                odds = [float(x) for x in paired_data[game][score]]
                arb = self.find_arb(odds)
                h_odd1, h_odd2 = self.find_highest_odds(odds)

                worksheet.merge_range(f'A{current_row}:A{current_row + 1}', 'Merged Range', bottom_border)
                worksheet.merge_range(f'D{current_row}:D{current_row + 1}', 'Merged Range', bottom_right_border)
                worksheet.set_column(0, 0, 40)

                worksheet.write(f"A{current_row}", float(score), bottom_border)

                if arb < 100:

                    if h_odd1 == odds[0]:
                        worksheet.write(f"B{current_row}", odds[0], center_format_w)
                        worksheet.write(f"C{current_row}", odds[2], center_format)
                    else:
                        worksheet.write(f"B{current_row}", odds[0], center_format)
                        worksheet.write(f"C{current_row}", odds[2], center_format_w)

                    if h_odd2 == odds[1]:
                        worksheet.write(f"B{current_row + 1}", odds[1], bottom_border_w)
                        worksheet.write(f"C{current_row + 1}", odds[3], bottom_border)
                    else:
                        worksheet.write(f"B{current_row + 1}", odds[1], bottom_border)
                        worksheet.write(f"C{current_row + 1}", odds[3], bottom_border_w)

                    worksheet.write(f"D{current_row}", arb, arb_win_format)

                else:

                    worksheet.write(f"B{current_row}", odds[0], center_format)
                    worksheet.write(f"B{current_row + 1}", odds[1], bottom_border)

                    worksheet.write(f"C{current_row}", odds[2], center_format)
                    worksheet.write(f"C{current_row + 1}", odds[3], bottom_border)

                    worksheet.write(f"D{current_row}", arb, arb_lose_format)

                row_add += 2

            row_counter += row_add + 5


        workbook.close()

    def main(self, betano_data, bwin_data):

        paired_data = self.paired_data(betano_data, bwin_data)

        self.write_to_excel(paired_data)




if __name__ == '__main__':
    DataComparing()
