import date_utils.calendar_util

# Returns the weekday from a given hebrew date (0 for Sunday,
# 1 for Monday,...)


def getWeekdayOfHebrewDate(hebDay, hebMonth, hebYear):
    # Calculating the julian date
    julian = date_utils.calendar_util.hebrew_to_jd(hebYear, hebMonth, hebDay)
    weekday = (int(julian) + 2) % 7
    return weekday


def calculate_holiday(g_day, g_month, g_year, diaspora):
    julian = date_utils.calendar_util.gregorian_to_jd(g_year, g_month, g_day)
    hebYear, hebMonth, hebDay = date_utils.calendar_util.jd_to_hebrew(julian)

    listHolidays = []

    # Holidays in Nisan

    hagadolDay = 14
    while getWeekdayOfHebrewDate(hagadolDay, 1, hebYear) != 6:
        hagadolDay -= 1
    if hebDay == hagadolDay and hebMonth == 1:
        listHolidays.append("Shabat Hagadol")

    if hebDay == 14 and hebMonth == 1:
        listHolidays.append("Erev Pesach")
    if hebDay == 15 and hebMonth == 1:
        listHolidays.append("Pesach I")
    if hebDay == 16 and hebMonth == 1:
        if diaspora:
            listHolidays.append("Pesach II")
        else:
            listHolidays.append("Chol Hamoed")
    if hebDay == 17 and hebMonth == 1:
        listHolidays.append("Chol Hamoed")
    if hebDay == 18 and hebMonth == 1:
        listHolidays.append("Chol Hamoed")
    if hebDay == 19 and hebMonth == 1:
        listHolidays.append("Chol Hamoed")
    if hebDay == 20 and hebMonth == 1:
        listHolidays.append("Chol Hamoed")
    if hebDay == 21 and hebMonth == 1:
        if not diaspora:
            listHolidays.append("Pesach VII (Yizkor)")
        else:
            listHolidays.append("Pesach VII")
    if hebDay == 22 and hebMonth == 1:
        if diaspora:
            listHolidays.append("Pesach VIII (Yizkor)")

    # Yom Hashoah

    if getWeekdayOfHebrewDate(27, 1, hebYear) == 5:
        if hebDay == 26 and hebMonth == 1:
            listHolidays.append("Yom Hashoah")
    elif hebYear >= 5757 and getWeekdayOfHebrewDate(27, 1, hebYear) == 0:
        if hebDay == 28 and hebMonth == 1:
            listHolidays.append("Yom Hashoah")
    else:
        if hebDay == 27 and hebMonth == 1:
            listHolidays.append("Yom Hashoah")

    # Holidays in Iyar

    # Yom Hazikaron

    # If 4th of Iyar is a Thursday ...
    if getWeekdayOfHebrewDate(4, 2, hebYear) == 5:
        if hebDay == 2 and hebMonth == 2:  # ... then Yom Hazicaron is on 2th of Iyar
            listHolidays.append("Yom Hazikaron")
    elif getWeekdayOfHebrewDate(4, 2, hebYear) == 4:
        if hebDay == 3 and hebMonth == 2:
            listHolidays.append("Yom Hazikaron")
    elif hebYear >= 5764 and getWeekdayOfHebrewDate(4, 2, hebYear) == 0:
        if hebDay == 5 and hebMonth == 2:
            listHolidays.append("Yom Hazikaron")
    else:
        if hebDay == 4 and hebMonth == 2:
            listHolidays.append("Yom Hazikaron")

    # Yom Ha'Azmaut

    if getWeekdayOfHebrewDate(5, 2, hebYear) == 6:
        if hebDay == 3 and hebMonth == 2:
            listHolidays.append("Yom Ha'Atzmaut")
    elif getWeekdayOfHebrewDate(5, 2, hebYear) == 5:
        if hebDay == 4 and hebMonth == 2:
            listHolidays.append("Yom Ha'Atzmaut")
    elif hebYear >= 5764 and getWeekdayOfHebrewDate(4, 2, hebYear) == 0:
        if hebDay == 6 and hebMonth == 2:
            listHolidays.append("Yom Ha'Atzmaut")
    else:
        if hebDay == 5 and hebMonth == 2:
            listHolidays.append("Yom Ha'Atzmaut")

    if hebDay == 14 and hebMonth == 2:
        listHolidays.append("Pesach Sheni")
    if hebDay == 18 and hebMonth == 2:
        listHolidays.append("Lag B'Omer")
    if hebDay == 28 and hebMonth == 2:
        listHolidays.append("Yom Yerushalayim")

    # Holidays in Sivan

    if hebDay == 5 and hebMonth == 3:
        listHolidays.append("Erev Shavuot")
    if hebDay == 6 and hebMonth == 3:
        if diaspora:
            listHolidays.append("Shavuot I")
        else:
            listHolidays.append("Shavuot\n(Yizkor)")
    if hebDay == 7 and hebMonth == 3:
        if diaspora:
            listHolidays.append("Shavuot II\n(Yizkor)")

    # Holidays in Tammuz

    if getWeekdayOfHebrewDate(17, 4, hebYear) == 6:
        if hebDay == 18 and hebMonth == 4:
            listHolidays.append("Fast of Tammuz")
    else:
        if hebDay == 17 and hebMonth == 4:
            listHolidays.append("Fast of Tammuz")

    # Holidays in Av

    if getWeekdayOfHebrewDate(9, 5, hebYear) == 6:
        if hebDay == 10 and hebMonth == 5:
            listHolidays.append("Fast of Av")
    else:
        if hebDay == 9 and hebMonth == 5:
            listHolidays.append("Fast of Av")
    if hebDay == 15 and hebMonth == 5:
        listHolidays.append("Tu B'Av")

    # Holidays in Elul

    if hebDay == 29 and hebMonth == 6:
        listHolidays.append("Erev Rosh Hashana")

    # Holidays in Tishri

    if hebDay == 1 and hebMonth == 7:
        listHolidays.append("Rosh Hashana I")
    if hebDay == 2 and hebMonth == 7:
        listHolidays.append("Rosh Hashana II")
    if getWeekdayOfHebrewDate(3, 7, hebYear) == 6:
        if hebDay == 4 and hebMonth == 7:
            listHolidays.append("Tzom Gedaliah")
    else:
        if hebDay == 3 and hebMonth == 7:
            listHolidays.append("Tzom Gedaliah")
    if hebDay == 9 and hebMonth == 7:
        listHolidays.append("Erev Yom Kippur")
    if hebDay == 10 and hebMonth == 7:
        listHolidays.append("Yom Kippur\n(Yizkor)")
    if hebDay == 14 and hebMonth == 7:
        listHolidays.append("Erev Sukkot")
    if hebDay == 15 and hebMonth == 7:
        if diaspora:
            listHolidays.append("Sukkot I")
        else:
            listHolidays.append("Sukkot")
    if hebDay == 16 and hebMonth == 7:
        if diaspora:
            listHolidays.append("Sukkot II")
        else:
            listHolidays.append("Chol Hamoed")
    if hebDay == 17 and hebMonth == 7:
        listHolidays.append("Chol Hamoed")
    if hebDay == 18 and hebMonth == 7:
        listHolidays.append("Chol Hamoed")
    if hebDay == 19 and hebMonth == 7:
        listHolidays.append("Chol Hamoed")
    if hebDay == 20 and hebMonth == 7:
        listHolidays.append("Chol Hamoed")
    if hebDay == 21 and hebMonth == 7:
        listHolidays.append("Hoshana Raba")
    if hebDay == 22 and hebMonth == 7:
        if not diaspora:
            listHolidays.append("Shemini Atzereth\n(Yizkor)")
            listHolidays.append("Simchat Torah")
        else:
            listHolidays.append("Shemini Atzereth\n(Yizkor)")
    if hebDay == 23 and hebMonth == 7:
        if diaspora:
            listHolidays.append("Simchat Torah")

    # Holidays in Kislev

    if hebDay == 25 and hebMonth == 9:
        listHolidays.append("Chanukka I")
    if hebDay == 26 and hebMonth == 9:
        listHolidays.append("Chanukka II")
    if hebDay == 27 and hebMonth == 9:
        listHolidays.append("Chanukka III")
    if hebDay == 28 and hebMonth == 9:
        listHolidays.append("Chanukka IV")
    if hebDay == 29 and hebMonth == 9:
        listHolidays.append("Chanukka V")
    # Holidays in Tevet

    if hebDay == 10 and hebMonth == 10:
        listHolidays.append("Fast of Tevet")

    if date_utils.calendar_util.hebrew_month_days(hebYear, 9) == 30:
        if hebDay == 30 and hebMonth == 9:
            listHolidays.append("Chanukka VI")
        if hebDay == 1 and hebMonth == 10:
            listHolidays.append("Chanukka VII")
        if hebDay == 2 and hebMonth == 10:
            listHolidays.append("Chanukka VIII")
    if date_utils.calendar_util.hebrew_month_days(hebYear, 9) == 29:
        if hebDay == 1 and hebMonth == 10:
            listHolidays.append("Chanukka VI")
        if hebDay == 2 and hebMonth == 10:
            listHolidays.append("Chanukka VII")
        if hebDay == 3 and hebMonth == 10:
            listHolidays.append("Chanukka VIII")

    # Holidays in Shevat

    if hebDay == 15 and hebMonth == 11:
        listHolidays.append("Tu B'Shevat")

    # Holidays in Adar (I)/Adar II

    if date_utils.calendar_util.hebrew_leap(hebYear):
        monthEsther = 13
    else:
        monthEsther = 12

    if getWeekdayOfHebrewDate(13, monthEsther, hebYear) == 6:
        if hebDay == 11 and hebMonth == monthEsther:
            listHolidays.append("Fast of Esther")
    else:
        if hebDay == 13 and hebMonth == monthEsther:
            listHolidays.append("Fast of Esther")

    if hebDay == 14 and hebMonth == monthEsther:
        listHolidays.append("Purim")
    if hebDay == 15 and hebMonth == monthEsther:
        listHolidays.append("Shushan Purim")

    if date_utils.calendar_util.hebrew_leap(hebYear):
        if hebDay == 14 and hebMonth == 12:
            listHolidays.append("Purim Katan")
        if hebDay == 15 and hebMonth == 12:
            listHolidays.append("Shushan Purim Katan")

    return listHolidays
