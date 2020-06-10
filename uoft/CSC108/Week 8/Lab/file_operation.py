f = open("data2.txt")
write_f = open("output.txt", "w")
for line in f:
    if line.lower().find("lol") != -1:
        print line,
        write_f.write(line)
write_f.close()
        
        
        
    