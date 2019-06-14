charcount = 0
inQuote = False
c = '?'
str_count = 0
str_list = []

outFile = open("/Users/joshua/dev/school/hospital/ERlast2yearsOut.csv", "w")

with open("/Users/joshua/dev/school/hospital/ERlast2years.csv", "r") as f:
    while True:
        previousChar = c
        c = f.read(1)
        charcount += 1

        if str_count > 1000000:
            outFile.write(''.join(str_list))
            str_list = []
            str_count = 0
            print("Entered: ",charcount, " ", str_count)

        if not c:
            outFile.write(''.join(str_list))
            outFile.close()
            print("Reached EOF")
            exit()
            
        if c == "\n" and inQuote:
            str_list.append("¡")
            str_count += 1
        elif c == '"' and not inQuote:
            inQuote = not inQuote
            str_list.append(c)
            str_count += 1
        elif c == '"' and inQuote:
            d = f.read(1)
            charcount += 1
            
            if not d:
                str_list.append(c)
                outFile.write(''.join(str_list))
                outFile.close()
                print("Reached EOF")
                exit()
            elif d == '"':
                str_list.append(c)
                str_list.append(d)
                str_count += 2
            else:
                inQuote = not inQuote
                str_list.append(c)
                str_list.append(d)
                str_count += 2
        else:
            str_list.append(c)
            str_count += 1


print("done")
