class Person:
    def __init__(self, name, privacy, biography):
        # Normalize privacy to "public" / "private"
        self.name = name
        self.privacy = "private" if privacy.upper() == "P" else "public"
        self.biography = biography

    def __str__(self):
        return f"Person(Name: {self.name}, Privacy: {self.privacy}, Biography: {self.biography})"

    def get_name(self):
        return self.name

    def get_privacy(self):
        return self.privacy

    def get_biography(self):
        return self.biography


class UDGraph:
    def __init__(self):
        self.graph = {}

    def add_vertex(self, vertex):
        if vertex not in self.graph:
            self.graph[vertex] = []

    def add_edge(self, from_vertex, to_vertex):
        if from_vertex in self.graph and to_vertex in self.graph:
            if to_vertex not in self.graph[from_vertex]:  # prevent duplicate follows
                self.graph[from_vertex].append(to_vertex)

    def remove_edge(self, from_vertex, to_vertex):
        if from_vertex in self.graph:
            if to_vertex in self.graph[from_vertex]:
                self.graph[from_vertex].remove(to_vertex)
            else:
                raise ValueError("Edge does not exist")

    def get_vertices(self):
        return list(self.graph.keys())

    def list_outgoing_adjacent_vertex(self, vertex):
        return self.graph[vertex]

    def list_incoming_adjacent_vertex(self, target_vertex):
        incoming = []
        for from_node, to_node in self.graph.items():
            if target_vertex in to_node:
                incoming.append(from_node)
        return incoming


class MiniGram:  # <-- renamed here
    max_profiles = 10

    def __init__(self):
        self.my_graph = UDGraph()
        self.profile_count = 0

    def add_new_profile(self, name, privacy, biography):
        person = Person(name, privacy, biography)
        self.my_graph.add_vertex(person)
        self.profile_count += 1
        return person

    def add_follow(self, follower, following):
        self.my_graph.add_edge(follower, following)

    def remove_follow(self, follower, following):
        self.my_graph.remove_edge(follower, following)

    def display_profile(self, index):
        person = list(self.my_graph.get_vertices())[index - 1]
        print(f"Name: {person.get_name()}")
        if person.get_privacy() == "public":
            print(f"Biography: {person.get_biography()}")
        else:
            print(f"{person.get_name()} has a private profile")

    def display_all_profiles(self):
        for i, person in enumerate(self.my_graph.get_vertices()):
            print(f"{i + 1}.) {person.get_name()}")

    def display_neighbours(self, vertex):
        neighbours = self.my_graph.get_vertices()
        following = self.my_graph.list_outgoing_adjacent_vertex(vertex)
        for i, person in enumerate(neighbours):
            if person != vertex and person not in following:
                print(f"{i + 1} {person.get_name()}")

    def display_followers(self, vertex):
        followers = self.my_graph.list_incoming_adjacent_vertex(vertex)
        print("Followers List: ")
        for person in followers:
            print(f"- {person.get_name()}")

    def display_following(self, vertex):
        following = self.my_graph.list_outgoing_adjacent_vertex(vertex)
        print("Following List: ")
        for person in following:
            print(f"- {person.get_name()}")


def main():
    global gram
    gram = MiniGram()  # <-- also updated here

    # Create sample users
    karen = gram.add_new_profile("Karen Hathaway", "P", "Confidence is my best accessory")
    selina = gram.add_new_profile("Selina Kyle", "U", "In a world full of trends, be a classic")
    toby = gram.add_new_profile("Toby Marshall", "U", "Just an ordinary science student in New York")
    pete = gram.add_new_profile("Peter Parker", "U", "Great power comes with great responsibilities")
    robert = gram.add_new_profile("Robert Downey Jr", "P", "I am iron man")

    # Create some follow relationships
    gram.add_follow(karen, selina)
    gram.add_follow(karen, toby)
    gram.add_follow(karen, robert)
    gram.add_follow(robert, karen)
    gram.add_follow(robert, pete)
    gram.add_follow(toby, karen)
    gram.add_follow(toby, selina)

    main_menu()


def main_menu():
    while True:
        print("***********************************************")
        print("Welcome to MiniGram, Your World, Your Voice:")  # <-- updated
        print("***********************************************")
        print("1. View names of all profiles")
        print("2. View details for any profiles")
        print("3. View followers of any profile")
        print("4. View followed accounts of any profile")
        print("5. Add a user profile")
        print("6. Follow a user profile")
        print("7. Unfollow a user profile")
        print("8. Quit")
        print("***********************************************")

        try:
            opt = int(input("Enter your choice (1-8): "))
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")
            continue

        if opt == 1:
            opt1()
        elif opt == 2:
            opt2()
        elif opt == 3:
            opt3()
        elif opt == 4:
            opt4()
        elif opt == 5:
            opt5()
        elif opt == 6:
            opt6()
        elif opt == 7:
            opt7()
        elif opt == 8:
            print("Thank you for using MiniGram, have a great day!")
            break
        else:
            print("Wrong input. Please enter again")


def opt1():
    print("=======================================")
    print("View All Profile Names:")
    print("=======================================")
    gram.display_all_profiles()


def opt2():
    print("=======================================")
    print("View Details for Any Profile:")
    print("=======================================")
    gram.display_all_profiles()
    view = int(input("Select whose profile to view : "))
    gram.display_profile(view)


def opt3():
    print("=======================================")
    print("View Followers for Any Profile:")
    print("=======================================")
    gram.display_all_profiles()
    view = int(input("Select whose profile to view: "))
    person = list(gram.my_graph.get_vertices())[view - 1]
    gram.display_followers(person)


def opt4():
    print("=======================================")
    print("View Followed Accounts for Any Profile:")
    print("=======================================")
    gram.display_all_profiles()
    view = int(input("Select whose profile to view: "))
    person = list(gram.my_graph.get_vertices())[view - 1]
    gram.display_following(person)


def opt5():
    print("=======================================")
    print("Add User Profile:")
    print("=======================================")
    if gram.profile_count >= MiniGram.max_profiles:  # <-- updated
        print("Sorry, you can't add more users. Maximum profile limit (10) reached.")
    else:
        name = str(input("Please enter user name: "))
        while True:
            privacy = str(input("Please select your privacy (P - private || U - public): "))
            if privacy.upper() in ["P", "U"]:
                break
        biography = str(input("Please enter your biography: "))
        gram.add_new_profile(name, privacy, biography)
        print(f"{name} has been added")


def opt6():
    print("=======================================")
    print("Follow a User Profile:")
    print("=======================================")
    gram.display_all_profiles()
    from_profile = int(input("Select your profile: "))
    person1 = list(gram.my_graph.get_vertices())[from_profile - 1]
    gram.display_neighbours(person1)
    to_profile = int(input("Select the profile you wish to follow: "))
    person2 = list(gram.my_graph.get_vertices())[to_profile - 1]
    gram.add_follow(person1, person2)
    print(f"{person1.get_name()} now follows {person2.get_name()}")


def opt7():
    print("=======================================")
    print("Unfollow a User Profile:")
    print("=======================================")
    gram.display_all_profiles()
    from_profile = int(input("Select your profile: "))
    person1 = list(gram.my_graph.get_vertices())[from_profile - 1]
    gram.display_following(person1)
    to_profile = int(input("Select the profile you wish to unfollow: "))
    person2 = list(gram.my_graph.get_vertices())[to_profile - 1]
    gram.remove_follow(person1, person2)
    print(f"{person1.get_name()} unfollowed {person2.get_name()}")


if __name__ == "__main__":
    main()

