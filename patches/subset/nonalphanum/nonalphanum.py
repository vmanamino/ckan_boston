with open('titles.txt') as titles:
    with open('nonalphnum.txt', 'w') as nonalphanum:
        with open('dataset_ids.txt', 'w') as id_list:
            lines = titles.read().splitlines()
            count = 0
            for line in lines:
                if count:
                    # print('greater than zero: %s' % count)
                    string = line.replace(' ', '')
                    if not string.isalnum():
                        # print('%s\n'%string)
                        nonalphanum.write('%s\n' % line)
                    else:
                        id = line.replace(' ', '-')
                        id_list.write('%s\n' % id)
                count += 1
                
            
with open('nonalphnum.txt') as stringtolist:
    with open('cleaned_up.txt', 'w') as cleaned:
        nonalphanum = []   
        lines =  stringtolist.read().splitlines()
        id = ''
        count = 0
        for line in lines:
            id = ''
            string = line.replace(' ', '')
            characters = list(string)
            for char in characters:
                if not char.isalnum():
                    if char not in nonalphanum:
                        nonalphanum.append(char)
                        
            # both check and remove duplicates once
            for ch in nonalphanum:
                if ch in line:
                    print('character %s in id %s' % (ch, line))
                    line = line.replace(ch, '')
                    
            print(line)
            
               
                 
            

        
        