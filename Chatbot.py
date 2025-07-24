import os

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
                'tags': [tag.strip() for tag in tags_str.split(';')] # Split tags by semicolon
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
    print(f"\tTags: {', '.join(tool['tags'])}") # Join tags with a comma for display
    print("-" * (len(tool['name']) + 8))

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
        found_tools = []
        for tool in db:
            # Create a searchable text block for each tool
            search_text = f"{tool['name']} {tool['type']} {tool['developer']} {' '.join(tool['tags'])}".lower()
            if all(word in search_text for word in query_words):
                found_tools.append(tool)
        
        if found_tools:
            print(f"\nFound {len(found_tools)} relevant tool(s) for '{user_query}':")
            for tool in found_tools:
                print_tool_details(tool)
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
            for tool in found: print_tool_details(tool)
        else:
            print(f"\nSorry, no tools found of type '{search_term}'.")
        
        keep_searching = input("\nSearch for another type? (y/n): ").lower()
        if keep_searching != 'y':
            break

def find_free_plugins(db):
    """Finds all free plugins and waits for user to continue."""
    found = [tool for tool in db if tool['price'] == 0]
    if found:
        print(f"\nFound {len(found)} FREE tool(s):")
        for tool in found: print_tool_details(tool)
    else:
        print("\nSorry, no free tools found in the database.")
    
    input("\nPress Enter to return to the main menu.")


def find_by_tag(db):
    """Allows the user to search by tag repeatedly."""
    while True:
        search_term = input("Enter the tag to search for (e.g., vintage, mastering): ").lower()
        found = [tool for tool in db if search_term in tool['tags']]
        if found:
            print(f"\nFound {len(found)} tool(s) with the tag '{search_term}':")
            for tool in found: print_tool_details(tool)
        else:
            print(f"\nSorry, no tools found with the tag '{search_term}'.")

        keep_searching = input("\nSearch for another tag? (y/n): ").lower()
        if keep_searching != 'y':
            break

def main():
    """The main function that runs the tool finder bot."""
    database = load_database()
    if not database:
        return

    while True:
        print("\n===== Music Production Tool Finder =====")
        print("1. Search by Type (e.g., EQ, Synth)")
        print("2. Find FREE Plugins")
        print("3. Find Tools by Tag (e.g., 'vintage')")
        print("4. Smart Search (Search all details)")
        print("5. Exit")
        
        choice = input("Please enter your choice (1-5): ")
        
        if choice == '1': search_by_type(database)
        elif choice == '2': find_free_plugins(database)
        elif choice == '3': find_by_tag(database)
        elif choice == '4': smart_search(database)
        elif choice == '5':
            print("\nHappy producing! Goodbye.\n")
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
