with open('titles.txt') as titles:
    with open('nonalphnum.txt', 'w') as out:
        with open('dataset_ids.txt', 'w') as id_list:
            lines = titles.read().splitlines()
            count = 0
            for line in lines:
                if count:
                    # print('greater than zero: %s' % count)
                    string = line.replace(' ', '')
                    if not string.isalnum():
                        # print('%s\n'%string)
                        out.write('%s\n' % string)
                    else:
                        id = line.replace(' ', '-')
                        id_list.write('%s\n' % id)
                count += 1
                
            
# with open('nonalphnum.txt') as subset:
#     lines =  subset.read().splitlines()
#     for line in lines:
#         subset.write('%s\n' % line)
        
        