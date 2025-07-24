import os
import math


def load_database(filename="tools_database.txt"):
    """
    Loads the tool database from a comma-separated .txt file.
    Format: Name,Type,Developer,Price,Tags (semicolon-separated)
    """
    try:
        with open(filename, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found.")
        print("Please make sure the database file is in the same directory.")
        return []

    database = []
    for line in lines:
        if not line.strip():
            continue

        parts = [p.strip() for p in line.strip().split(',')]
        # Ensure the line has the correct number of parts (5)
        if len(parts) == 5:
            name, tool_type, developer, price, tags_str = parts
            tool = {
                'name': name,
                'type': tool_type,
                'developer': developer,
                'price': int(price),
                'tags': [tag.strip() for tag in tags_str.split(';')]  # Split tags by semicolon
            }
            database.append(tool)

    return database


def print_tool_details(tool):
    """Prints the details of a single tool in a nicely formatted way."""
    print(f"\n--- {tool['name']} ---")
    print(f"\tType: {tool['type']}")
    print(f"\tDeveloper: {tool['developer']}")
    price = "Free" if tool['price'] == 0 else f"${tool['price']}"
    print(f"\tPrice: {price}")
    print(f"\tTags: {', '.join(tool['tags'])}")  # Join tags with a comma for display
    print("-" * (len(tool['name']) + 8))


def display_paginated_results(results):
    """
    Displays a list of results in paginated form, allowing users to select a page.
    """
    page_size = 2
    # Use math.ceil to round up to the nearest whole number for total pages
    total_pages = math.ceil(len(results) / page_size)
    current_page = 1

    if total_pages == 0:
        return

    while True:
        # Add a large space for readability before displaying the next page
        print("\n\n\n")

        # Calculate the start and end index for the items on the current page
        start_index = (current_page - 1) * page_size
        end_index = start_index + page_size
        page_items = results[start_index:end_index]

        print(f"--- Page {current_page} of {total_pages} ---")
        for item in page_items:
            print_tool_details(item)

        if total_pages == 1:
            print("\n--- End of results ---")
            break

        try:
            prompt = f"\nEnter page number (1-{total_pages}) or 'q' to quit this view: "
            choice = input(prompt).lower()

            if choice == 'q':
                break

            # Convert user input to an integer page number
            next_page = int(choice)
            if 1 <= next_page <= total_pages:
                current_page = next_page
            else:
                # Handle cases where the number is out of the valid page range
                print(f"Invalid page number. Please enter a number between 1 and {total_pages}.")

        except ValueError:
            # Handle cases where the input is not a number or 'q'
            print("Invalid input. Please enter a page number or 'q'.")
        except KeyboardInterrupt:
            print("\nReturning to menu.")
            break


def smart_search(db):
    """
    Performs a keyword search across all tool details and prints the results.
    This is an offline alternative to the AI assistant.
    """
    while True:
        user_query = input("\nEnter keywords to search for (e.g., 'free ambient reverb'): ").lower()
        if not user_query:
            break

        query_words = set(user_query.split())

        # Handle special keywords 'free' and 'paid'
        is_free_search = 'free' in query_words
        is_paid_search = 'paid' in query_words

        # Remove special price keywords from the set so they aren't used in the text search
        if is_free_search:
            query_words.remove('free')
        if is_paid_search:
            query_words.remove('paid')

        found_tools = []
        for tool in db:
            # --- Price Filtering Logic ---
            if is_free_search and tool['price'] != 0:
                continue  # Skip this tool if we want free ones and this one is not
            if is_paid_search and tool['price'] == 0:
                continue  # Skip this tool if we want paid ones and this one is free

            # --- Keyword Matching Logic ---
            # Create a searchable text block for each tool
            search_text = f"{tool['name']} {tool['type']} {tool['developer']} {' '.join(tool['tags'])}".lower()

            # Check if all *remaining* keywords match the tool's details
            if all(word in search_text for word in query_words):
                found_tools.append(tool)

        if found_tools:
            print(f"\nFound {len(found_tools)} relevant tool(s) for '{user_query}':")
            display_paginated_results(found_tools)
        else:
            print(f"\nSorry, no tools found matching all keywords: '{user_query}'.")

        keep_searching = input("\nPerform another smart search? (y/n): ").lower()
        if keep_searching != 'y':
            break


def search_by_type(db):
    """Allows the user to search by type repeatedly."""
    while True:
        search_term = input("Enter the type to search for (e.g., EQ, Synth): ").lower()
        found = [tool for tool in db if search_term in tool['type'].lower()]
        if found:
            print(f"\nFound {len(found)} tool(s) of type '{search_term}':")
            display_paginated_results(found)
        else:
            print(f"\nSorry, no tools found of type '{search_term}'.")

        keep_searching = input("\nSearch for another type? (y/n): ").lower()
        if keep_searching != 'y':
            break


def find_free_plugins(db):
    """Finds all free plugins and displays them with pagination."""
    found = [tool for tool in db if tool['price'] == 0]
    if found:
        print(f"\nFound {len(found)} FREE tool(s):")
        display_paginated_results(found)
    else:
        print("\nSorry, no free tools found in the database.")

    input("\nPress Enter to return to the main menu.")


def find_by_tag(db):
    """Allows the user to search by tag repeatedly, with partial matching."""
    while True:
        search_term = input("Enter the tag to search for (e.g., vintage, paid): ").lower()
        found = []

        if search_term == 'paid':
            # Special case: find all tools that are not free
            for tool in db:
                if tool['price'] > 0:
                    found.append(tool)
        else:
            # Original logic for all other tags
            for tool in db:
                # Check if the search term is a substring of ANY tag in the list
                if any(search_term in tag for tag in tool['tags']):
                    found.append(tool)

        if found:
            print(f"\nFound {len(found)} tool(s) for the tag '{search_term}':")
            display_paginated_results(found)
        else:
            print(f"\nSorry, no tools found with the tag '{search_term}'.")

        keep_searching = input("\nSearch for another tag? (y/n): ").lower()
        if keep_searching != 'y':
            break


def main():
    """The main function that runs the tool finder bot."""
    database = load_database("tools_database.txt")
    if not database:
        return

    while True:
        print("\n===== Music Production Tool Finder =====")
        print("1. Search by Type (e.g., EQ, Synth)")
        print("2. Find FREE Plugins")
        print("3. Find Tools by Tag (e.g., 'vintage', 'paid')")
        print("4. Smart Search (Search all details)")
        print("5. Exit")

        choice = input("Please enter your choice (1-5): ")

        if choice == '1':
            search_by_type(database)
        elif choice == '2':
            find_free_plugins(database)
        elif choice == '3':
            find_by_tag(database)
        elif choice == '4':
            smart_search(database)
        elif choice == '5':
            print("\nHappy producing! Goodbye.\n")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
