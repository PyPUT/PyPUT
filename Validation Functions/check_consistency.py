def check_consistency(file_name):

    '''
    @gt
    this fucntion takes in as parameter an aux file
    informs if consistency succeded
    if not, prints missing files
    :param file_name: str
    :return
    '''
    
    files = [".nodes", ".nets", ".wts", ".pl", ".scl", ".shapes", ".route"]
    
    is_included = [False, False, False, False, False, False, False]
    
    with open(file_name + ".aux") as f:
            
        for i, line in enumerate(f):
            line = line.strip()
            if line:
                if line.split()[0] == "RowBasedPlacement":
                    if ".nodes" in line:
                        is_included[0] = True
                    if ".nets" in line:
                        is_included[1] = True
                    if ".wts" in line:
                        is_included[2] = True
                    if ".pl" in line:
                        is_included[3] = True
                    if ".scl" in line:
                        is_included[4] = True
                    if ".shapes" in line:
                        is_included[5] = True
                    if ".route" in line:
                        is_included[6] = True
                                            
    if False not in is_included:
        print(file_name + " consistency check completed succesfully")
    else:
        missing = []
        for i in range(len(is_included)):
            if is_included[i] is False:
                missing.append(i)
            
    print(file_name + " consistency check failed, missing files: ")
    for index in missing:
        print(files[index])