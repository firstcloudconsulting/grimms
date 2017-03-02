import re
import string

def main():
    expression = input('Enter a Search Term: ')
    expression_halfnormalized = expression.strip(string.punctuation + string.whitespace)
    expression_fullynormalized = expression_halfnormalized.lower()


    current_title = []
    story_titles = []

    stoplines = []
    with open('C:\\Users\ccs\Desktop\stopwords.txt') as stopfile:
        stoplines.append('\n')
        for lines in stopfile:
            line = lines.rstrip()
            words = line.split()
            stoplines.append(words)

        # Add words without newline to dictionary

    infile = open('C:\\Users\ccs\Desktop\grimms.txt', 'r')
    grimm_lines = infile.readlines()  # reads everything into infile
    histogram = {}

    lnum = 0
    for lines in grimm_lines:
        lnum += 1
        match = re.search(r'^[A-Z,\ _-]+$', lines)
        if match:
            current_title = match.group()
            print(current_title)
        elif lines.strip() == "*****": #
            infile.close()
            break
        else:
            lines = lines.replace('-', ' ')
            for line in lines.rsplit():
                #line = line.strip(string.punctuation + string.whitespace)
                line = line.lower()
                if lnum >= 124 and line not in stoplines:
                    print(histogram.setdefault(line, {}).setdefault(current_title, [].append(lnum))) #keeps returning None over and over

                    #exclude "and" & "or" from this method
    if expression_fullynormalized in histogram:
        search_term = (histogram[expression_fullynormalized])
        for (keys,values) in search_term.items(): #.items() returns keys and values as a pair
            search_term_line_number = 1 #iterates line numbers
            j = 1
            for j in values:
                if j == 1:
                    #print(keys)
                    j +=1

                    print(j,lines[search_term_line_number - 1].replace(expression_fullynormalized,"**" + expression_fullynormalized.upper() + "**"))
                else:
                    print('--')



                #
                # if expression_fullynormalized.find("and") == 0:
                #     and_expression1 = expression_fullynormalized[0]
                #     and_expression2 = expression_fullynormalized[2]
                #     if and_expression1 and and_expression2 in histogram:
                #         and_search_term1 = (histogram[and_expression1])
                #         for (keys, values) in and_search_term1.items():
                #             story_titles.append(keys)
                #         andlist_1, andlist_2 = zip(*and_search_term1.items()) #change list names
                #         and_search_term2 = (histogram[and_expression2])
                #         for (keys, values) in and_search_term2.items():
                #             story_titles.append(keys)
                #         andlist_3, andlist_4 = zip(*and_search_term2.items()) #change list names
                #     elif and_expression1 and and_expression2 not in histogram:
                #         print('--')
                #
                #     set_story_titles = set(story_titles)
                #     for story_titles in set_story_titles:
                #         if story_titles in andlist_1 and andlist_3:
                #             number_set_1 = (histogram[and_expression1][story_titles])
                #             for i in number_set_1:
                #                 print(i, stopword.replace(and_expression1, "**" + and_expression1.upper() + "**"))
                #             number_set_2 = (histogram[and_expression2][story_titles])
                #             for i in number_set_2:
                #                 print(i, stopword.replace(and_expression2, "**" + and_expression2.upper() + "**"))
                #         elif story_titles not in andlist_1 and andlist_3:
                #             print("Error: Story Title Not Found")
                #
                # if expression_fullynormalized.find("or") == -1:
                #         or_expression1 = expression_fullynormalized[0]
                #         or_expression2 = expression_fullynormalized[2]
                #         if or_expression1 or or_expression2 not in histogram:
                #             print("--")
                #         elif or_expression1 or or_expression2 in histogram:
                #             if or_expression1 in histogram:
                #                 or_search_term1 = (histogram[or_expression1][story_titles])
                #                 for (keys, values) in or_search_term1.items():
                #                     story_titles.append('keys')
                #                 or_list1, or_list2 = zip(*or_search_term1.items())
                #             elif or_expression1 not in histogram:
                #                 or_expression1_list = []
                #             if or_expression2 in histogram:
                #                 or_search_term2 = (histogram[or_expression2][story_titles])
                #             elif or_expression2 not in histogram:
                #                 or_expression2_list = []
                #                 for (keys, values) in or_search_term2.items():
                #                     story_titles.append(keys)
                #
                #             for story_titles in set_story_titles:
                #                 if story_titles in or_expression1_list:
                #                     histogram_add = (histogram[or_expression1][story_titles])
                #                     for i in histogram_add:
                #                         print(i, stopword.replace(or_expression1, "**" + or_expression1.upper() + "**"))
                #                 elif story_titles not in or_expression1_list:
                #                     print("--")








main()