import shlex, subprocess, json, argparse, re


# GitHub functionality
def get_issue_list():
    # Get list of all issues in repository
    get_issue_list = "gh issue list -s all -L 10000 --json title,number"
    list_args = shlex.split(get_issue_list)
    issue_list = json.loads(subprocess.check_output(list_args))

    return issue_list


def get_issue_numbers_from_exceptions(issue_list, exceptions):
    # Get remaining issues from list of exceptions
    numbers = []
    exceptions = exceptions.split(',')

    if exceptions[0].isdigit():
        exceptions_int = []
        for exception in exceptions:
            exceptions_int.insert(len(exceptions_int),int(exception))
        for issue in issue_list:
            if issue["number"] not in exceptions_int:
                numbers.insert(len(numbers), issue["number"])

    else:
        for issue in issue_list:
            if issue["title"].split(" |")[0] not in exceptions:
                numbers.insert(len(numbers),issue["number"])

    return numbers


def get_issue_numbers(issue_list, countries):
        # Get issue numbers for desired countries
        numbers = []

        if countries == "all":
            for issue in issue_list:
                numbers.insert(len(numbers),issue["number"])

        else:
            for issue in issue_list:
                if issue["title"].split(" |")[0] in countries:
                    numbers.insert(len(numbers),issue["number"])
    
        return numbers


def add_message_to_top(numbers, addition):
    for i in numbers:
        try:
            # Get current issue body
            view_body = "gh issue view " + str(i)
            print(view_body)
            view_args = shlex.split(view_body)

            body = subprocess.check_output(view_args, stderr=subprocess.STDOUT).decode('utf-8')
            body = body.split("--")[1]

            # Create new issue body
            new_body = ">" + addition + "\n" + body

            # Update issue body
            update_code = "gh issue edit " + str(i) + " --body"
            print(update_code)
            split_update_code = shlex.split(update_code)
            split_update_code.insert(len(split_update_code),new_body)

            subprocess.run(split_update_code, stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as e:
            if "GraphQL: Could not resolve to an issue or pull request with the number of" in e.output.decode('utf-8'):
                e = "Issue could not be found"
            print(f"Error in processing Issue #{i}: {e}")
        except Exception as e:
            print(f"Error in processing Issue #{i}: {e}")


def delete_message_from_top(numbers):
    for i in numbers:
        try:
            # Get current issue body
            view_body = "gh issue view " + str(i)
            print(view_body)
            view_args = shlex.split(view_body)

            body = subprocess.check_output(view_args, stderr=subprocess.STDOUT).decode('utf-8')
            body = body.split("--")[1]

            # Create new issue body
            new_body = body
            if ">" in new_body[:2]:
                new_body = body[body.index("\n", 1)+1:].lstrip()

            # Update issue body
            update_code = "gh issue edit " + str(i) + " --body"
            print(update_code)
            split_update_code = shlex.split(update_code)
            split_update_code.insert(len(split_update_code),new_body)

            subprocess.run(split_update_code, stderr=subprocess.STDOUT)

        except subprocess.CalledProcessError as e:
            if "GraphQL: Could not resolve to an issue or pull request with the number of" in e.output.decode('utf-8'):
                e = "Issue could not be found"
            print(f"Error in processing Issue #{i}: {e}")
        except Exception as e:
            print(f"Error in processing Issue #{i}: {e}")

def find_and_replace(numbers, find, replace):
    for i in numbers:
        try:
            # Get current issue body
            view_body = "gh issue view " + str(i)
            print(view_body)
            view_args = shlex.split(view_body)

            body = subprocess.check_output(view_args, stderr=subprocess.STDOUT).decode('utf-8')
            body = body.split("--")[1]

            # Find and replace phrase
            result = re.subn(find, replace, body)
            if result[1] == 0:
                raise Exception("Phrase '" + find + "' could not be found.")
            else:
                new_body = result[0]

            # Update issue body
            update_code = "gh issue edit " + str(i) + " --body"
            print(update_code)
            if result[1] == 1:
                print("1 replacement was made.")
            else:
                print(str(result[1]) + " replacements were made.")
            split_update_code = shlex.split(update_code)
            split_update_code.insert(len(split_update_code),new_body)

            subprocess.run(split_update_code, stderr=subprocess.STDOUT)
        
        except subprocess.CalledProcessError as e:
            if "GraphQL: Could not resolve to an issue or pull request with the number of" in e.output.decode('utf-8'):
                e = "Issue could not be found"
            print(f"Error in processing Issue #{i}: {e}")
        except Exception as e:
            print(f"Error in processing Issue #{i}: {e}")


# Command Line Functionality
def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='command_testing',
                                     description='Edits GitHub issues from command line')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Indicates that all issues should be edited.', required=False)
    parser.add_argument('-c', '--countries',
                        help='Comma separated list of counties to edit. Names longer than 1 word must be in quotes.', required=False)
    parser.add_argument('-d', '--delete', action='store_true',
                        help='Indicates that message at top should be deleted.', required=False)
    parser.add_argument('-e', '--exceptions',
                        help='Comma separated list of issue numbers NOT to edit.', required=False)
    parser.add_argument('-f', '--find',
                        help='File with body of text to find.', required=False)
    parser.add_argument('-m', '--message', type=str,
                        help='Message to add to top of issue description. Must be in quotes.', required=False)
    parser.add_argument('-n', '--numbers',
                        help='Comma separated list of issue numbers to edit.', required=False)
    parser.add_argument('-r', '--replace',
                        help='File with body of text to replace previous body of text.', required=False)

    args = parser.parse_args()
    if (args.replace is None and not args.find is None) or (args.find is None and not args.replace is None):
        raise Exception("If you wish to find and replace a phrase, please provide both a phrase to find (-f) and a phrase to use as replacement (-r). Otherwise please remove the -f or -r input.")
    if (not args.replace is None and args.delete) or (not args.replace is None and not args.message is None) or (args.delete and not args.message is None):
        raise Exception("You cannot delete the message at the top, find and replace a phrase, or add a message to the top simultaneously. Please either choose -d, provide a message using -m, or provide phrases to find and replace using -r.")
    if not args.delete and args.message is None and args.replace is None:
        raise Exception("Please indicate that the message at the top should be deleted, provide a message to be added, or provide phrases to find and replace.")
    if (args.all and not args.countries is None) or (args.all and not args.numbers is None) or (not args.numbers is None and not args.countries is None) or (not args.exceptions is None and args.all) or (not args.exceptions is None and not args.countries is None) or (not args.exceptions is None and not args.numbers is None):
        raise Exception("You cannot provide issue numbers, countries, exceptions, or all issues simultaneously. Please either indicate a list of issue numbers, a list of countries, a list of exceptions, or all issues.")
    if args.countries is None and args.numbers is None and not args.all and args.exceptions is None:
        raise Exception("Please indicate --all or provide a list of countries or a list of issue numbers.")
    elif args.countries is None and not args.numbers is None:
        args.numbers = args.numbers.split(',')
    elif args.numbers is None and not args.countries is None:
        args.countries = args.countries.split(',')
    
    return args


def main():
    args = parse_arguments()
    with open(args.find) as f:
        find = f.read()
    with open(args.replace) as f:
        replace = f.read()

    if not args.countries is None:
        issue_list = get_issue_list()
        number_list = get_issue_numbers(issue_list, args.countries)
        if args.delete:
            delete_message_from_top(number_list)
        if not args.message is None:
            add_message_to_top(number_list, args.message)
        if not args.replace is None:
            find_and_replace(number_list, find, replace)

    if not args.numbers is None:
        if args.delete:
            delete_message_from_top(args.numbers)
        if not args.message is None:
            add_message_to_top(args.numbers, args.message)
        if not args.replace is None:
            find_and_replace(args.numbers, find, replace)

    if args.all:
        issue_list = get_issue_list()
        number_list = get_issue_numbers(issue_list, "all")
        if args.delete:
            delete_message_from_top(number_list)
        if not args.message is None:
            add_message_to_top(number_list, args.message)
        if not args.replace is None:
            find_and_replace(number_list, find, replace)

    if not args.exceptions is None:
        issue_list = get_issue_list()
        number_list = get_issue_numbers_from_exceptions(issue_list, args.exceptions)
        if args.delete:
            delete_message_from_top(number_list)
        if not args.message is None:
            add_message_to_top(number_list, args.message)
        if not args.replace is None:
            find_and_replace(number_list, find, replace)



main()
