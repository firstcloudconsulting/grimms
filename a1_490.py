import re, sys

# Constants
AND = 0
OR = 1

def remove_lines(stories_dict, line_number):
    for story in stories_dict:
        for qt in stories_dict[story]:
            if line_number in stories_dict[story][qt]:
                del stories_dict[story][qt][line_number]

def query(histogram, term, lines, results=None, comparison=AND):
    # Normalize query
    q = re.sub(r'[^A-Za-z0-9 ]', ' ', term).lower().strip()

    if ' ' in q:
        print('Query only supports single terms. Too many values.')

        raise

    if not results:
        results = {}

    matches = 0

    if q in histogram:
        for story in histogram[q]:
            if story not in results:
                results[story] = {}

            if q not in results[story]:
                results[story][q] = {}

            for line_number in histogram[q][story]:
                matches += 1

                if line_number not in results[story]:
                    results[story][q][line_number] = lines[int(line_number) - 1].strip()

    # Let's strip out all non-intersecting items for AND conditions
    if comparison == AND:
        # Get list of all search terms in resultset
        query_terms = []

        for story in results:
            for q in results[story]:
                if q not in query_terms:
                    query_terms.append(q)

        # Check every line under every term
        stories_to_remove = []
        lines_to_remove = []

        for story in results:
            for q in results[story]:
                for line_number in results[story][q]:
                    # Ensure line number exists under every search term
                    for qt in query_terms:
                        if qt not in results[story]:
                            if story not in stories_to_remove:
                                stories_to_remove.append(story)
                        elif line_number not in results[story][qt]:
                            if line_number not in lines_to_remove:
                                lines_to_remove.append(line_number)

        # We couldn't remove keys while iterating them or the dict size would change and throw an error, we'll delete them now:
        for line_number in lines_to_remove:
            remove_lines(results, line_number)

        # Remove stories that no longer have any valid line numbers for an term
        for story in results:
            for qt in results[story]:
                if len(results[story][qt]) <= 0:
                    if story not in stories_to_remove:
                        stories_to_remove.append(story)

        for story in stories_to_remove:
            if story in results:
                del results[story]

    # For OR comparisons, we've already just added lines for the additional term to the original resultset
    elif comparison == OR:
        pass

    return results, matches

def print_results(results):
    # Get list of all search terms in resultset
    query_terms = []

    for story in results:
        for q in results[story]:
            if q not in query_terms:
                query_terms.append(q)

    for story in results:
        print('\t%s' % story.upper())

        for qt in results[story]:
            if len(query_terms) > 1:
                print('\t\t%s' % qt)

            for line_number in results[story][qt]:
                line_text = results[story][qt][line_number]

                # Capitalize instances of word
                line_text = line_text.replace(qt, '**%s**' % qt.upper())

                print('\t\t%s%s %s' % ('\t' if len(query_terms) > 1 else '', line_number, line_text))

def main():
    # Import stop words into list
    stopwords = []
    grimms_text = {}

    print('Loading stopwords...')

    with open('stopwords.txt') as stopfile:
        for word in stopfile:
            stopwords.append(word.lower().strip()) # Forces lower case, strips any whitespace

        stopfile.close()

    print(stopwords)

    # Index text
    w2s = {}
    stories = [] # Only using to count stories for output

    print("\nBuilding index...")

    with open('grimms.txt', 'r') as infile:
        project_details = True
        story = ''
        empty_lines = 0 # We're going to count empty lines, noticing that new stories have 4 preceding empty lines before the title
                        # This is how we're going to extract story titles since no other guidance was really provided

        # Enumerate will add a line index (zero-based). We'll add one to make this an actual line number for indexing
        for i, line in enumerate(infile):
            # Keep line data for reference in expression output
            grimms_text[i] = line

            # Skip project details at beginning/end of file
            if project_details:
                if ('START OF THIS PROJECT' in line):
                    project_details = False

                continue
            else:
                if ('END OF THIS PROJECT' in line):
                    project_details = True

                    continue

            if line.strip() == '':
                empty_lines += 1

                continue # Nothing to index
            else:
                # Check to see if we have a new story
                if empty_lines >= 4:
                    story = line.strip().upper()
                    stories.append(story)
                    empty_lines = 0

                    print('%s %s' % (len(stories), story))

                    continue # New story, but nothing to index

                empty_lines = 0 # Reset empty lines counter

            # Remove all characters that are not a letter, number, or space character
            line = re.sub(r'[^A-Za-z0-9 ]', ' ', line)
            tokens = line.split(' ') # Split line into list of tokens (words)

            for token in tokens:
                if token.strip() <= '':
                    continue # Skip empty tokens (could be caused by two spaces in a row, for example)

                # Don't index stopwords
                if token in stopwords:
                    continue

                # Ensure word is indexed
                if token not in w2s:
                    w2s[token] = {}

                # Ensure story where word is listed is indexed
                if story not in w2s[token]:
                    w2s[token][story] = []

                # Index line number where word is mentioned under correct story
                w2s[token][story].append(i+1)

        infile.close()

    # User input
    print("\n\nWelcome to the Grimms' Fairy Tales search system!")

    while True:
        # raw_input allows us to enter as string and not have to use quotes
        q = raw_input("\n\nPlease enter your query: ")

        # Normalize query
        qn = re.sub(r'[^A-Za-z0-9 ]', ' ', q).lower().strip()

        if qn =='qquit':
            sys.exit()

        # Normalize and parse query
        print('query = %s' % q)

        if ' ' not in qn:            # Single word query
            qt = [qn]
        elif ' or ' in qn:           # Two-word OR condition
            qt = qn.split(' or ')
            comparison_operator = OR
        elif ' and ' in qn:          # Two-word AND condition
            qt = qn.split(' and ')
            comparison_operator = AND
        elif q.count(' ') == 1:      # Both word query
            qt = qn.split(' ')
            comparison_operator = AND
        else:                        # All word query
            qt = qn.split(' ')
            comparison_operator = AND

        results = None

        for q in qt:
            if not results:
                results, matches = query(w2s, q, grimms_text)
            else:
                results, matches = query(w2s, q, grimms_text, results, comparison_operator)

        if matches == 0:
            print('\t--')
        else:
            print_results(results)

main()
