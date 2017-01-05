"""
This is a script to help create ids of datasets to be patched from
a list of dataset titles as they are/were on Socrata which have been
migrated to Boston Open Data Hub.
It does this by first identifying those dataset names/titles whose
only nonalphnumeric character is the space.  From those titles
ids are created by replacing the space with a dash, in this way
creating dataset ids in the format required by CKAN.  However,
actual ids needed for patching could be different.  So,
my forming of ids in this manner is a best effort to get close
to the ids of the datasets which I need to patch.

Secondly, I isoloate into a separate 'cleaned up' file
those dataset names/titles which have other
nonalphanumeric character than the space.  The patterns in which those 
characters appear are very irregular and the number of those dataset titles
is very small.  So, manually forming the ids will be quicker, but i have made the job easier
by removing all nonalphanumeric characters. except the space.  However,
for a larger set of title, a program would be more efficient.
Warning, the ids formed through this script are guesses at the ids.
The script to patch will create a report of what was actually patched.

MAKE SURE to make all letters lowercase, you will have more success with your ids that way!

"""



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
                        line = line.lower()
                        nonalphanum.write('%s\n' % line)
                    else:
                        id = line.replace(' ', '-')
                        id = id.lower()
                        id_list.write('%s\n' % id)
                count += 1
                
            
with open('nonalphnum.txt') as stringtolist:
    with open('cleaned_up.txt', 'w') as cleaned:
        cleaned.write('these are the titles to formatted into ids by separating words with a single dash.\nCopy and paste into a separate text file called cleaned_and_formatted.txt and format.  Then add to dataset_ids.txt file\n\n')
        with open('cleaned_up_report.txt', 'w') as report:
            nonalphanum = []   
            lines =  stringtolist.read().splitlines()
            id = ''
            count = 0
            for line in lines:
                count += 1
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
                        report.write('character %s in title %s\n' % (ch, line))
                        line = line.replace(ch, '')
                # report.write('\n\n')
                
                # keep count of titles cleaned
                report.write('%s\n\n' % count)
                line = line.replace(' ', '-')
                cleaned.write('%s\n' % line)
             
            # total cleaned   
            report.write('\n\ntotal cleaned:\n%s' % count)
            
               
                 
            

        
        