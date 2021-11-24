class LibraryItem:
    def __init__(self,title,upc,subject):
        self.title=title
        self.upc=upc
        self.subject=subject
        self.contributors=[]
    
    def add_contributors(self,contributors):
        for contributor in contributors:
            contributor_name=contributor[0]
            contributor_role=contributor[1]
            self.contributors.append(Contributortype(contributor_name,contributor_role))
 
    
    def get_contributors_of_the_item(self):
        total_contributors_of_the_item=''
        person_info=''
        last_person=self.contributors[-1]
        for person in self.contributors:
            person_info=person.type+" "+person.contributor.name
            if person==last_person:
                total_contributors_of_the_item=total_contributors_of_the_item+person_info+"."+" "
            else:
                total_contributors_of_the_item=total_contributors_of_the_item+person_info+","+" "
        return total_contributors_of_the_item

    def locate(self):
        pass




class Book(LibraryItem):
    def __init__(self,title,upc,subject,contributors,ISBN,DDS):
        super().__init__(title,upc,subject)
        super().add_contributors(contributors)
        
        self.ISBN=ISBN
        self.DDS=DDS
        self.type='Book'
    
    def locate(self):
        return f'Book DDS No: {self.DDS}'
        
        
class CD(LibraryItem):
    def __init__(self,title,upc,subject,contributors):
        super().__init__(title, upc, subject)
        super().add_contributors(contributors)
        self.type="CD Audio"

    def locate(self):
        return f"CD UPC No: {self.upc}"

class DVD(LibraryItem):
    def __init__(self,title,upc,subject,contributors,genre):
        super().__init__(title,upc,subject)
        super().add_contributors(contributors)
        self.genre=genre
        self.type="DVD"
    
    def locate(self):
       return f'Movie Genre: {self.genre}'
       

class Magazine(LibraryItem):
    def __init__(self,title,upc,subject,contributors,volume,issue):
        super().__init__(title,upc,subject)
        super().add_contributors(contributors)
        self.volume=volume
        self.issue=issue
        self.type="Magazine"

    def locate(self):
        return f'''Magazine Volume No: {self.volume}
                   Magazine Issue No: {self.issue}'''



class Contributortype:
   def __init__(self,name,type):
       self.contributor=Contributor(name)
       self.type=type

class Contributor:
    def __init__(self,name):
        self.name=name



class Matching:
    def __init__(self,all_library_items):
        self.items_list=all_library_items
    
    def match_by_title(self,keyword):
        return [item for item in self.items_list if keyword in item.title]
       
    def match_by_subject(self,keyword):
       return [item for item in self.items_list if keyword == item.subject]
    def match_by_contributors(self,keyword):
        items_that_matched_by_contributor_name=[]
        for a_item in self.items_list:
            for person in a_item.contributors:
                if keyword==person.contributor.name:
                    items_that_matched_by_contributor_name.append(a_item)
        return items_that_matched_by_contributor_name

            
               



class NotFoundError(Exception):
    def __init__(self,keyword):
        super().__init__(f'Sorry the word "{keyword}" does not match any items')

class InvalidChoiceError(Exception):
    def __init__(self,keyword):
        super().__init__(f'Sorry,"{keyword}" is an invalid option. Please put the correct option')

class Catalog:
    def __init__(self):
        self.catalog_list=[]
        self.populate_library_with_items()



    def populate_library_with_items(self):

        self.catalog_list.append(Book("Design Patterns Elements of Reusable Object-Oriented Software",906525213621,"Programming",
        [["Erich Gamma","Writer"],["Richard Helm","Writer"],["Ralph Johnson","writer"],["John Vlissides","writer"]],
        "0-3584-1796-1",600))

        self.catalog_list.append(Book("Clean Code",717586932677,"Computer Science",
        [["Bob Martin","Writer"]],
        "0-7356-6043-3",600))

        self.catalog_list.append(Book("Take Their Money",699487742442,"Writing",
        [["Kyle Milligan","Writer"],["Sean Vosler","Translator"]],
        "0-3700-2966-6",800))

        self.catalog_list.append(Magazine("Time Magazine",677364702753,"Miscellaneous",[["Richard Stengel","author"],["Mark Halperin","editor"]],
        153,3))

        self.catalog_list.append(Magazine("Harvard Business Review",293525470099,"Economy",[["Joshua Macht","publisher"],["Adi Ignatius","editor"],
        ["Thomas A. Stewart","editor"]],97,6))

        self.catalog_list.append(DVD("The Crusades: The Arab perspective",682878968193,"History",[["Aljazeera","producer"]],"Wars"))

        self.catalog_list.append(DVD("The Social Network",577857753565,"Science & Tech",[["Scott Rudin","producer"],
        ["Jesse Eisenberg","actor"],["Andrew Garfield","actor"]],"Programming"))

        self.catalog_list.append(DVD("The Bermuda Triangle",487476774145,"Science & Tech",[["René Cardona Jr","director"]],"Weather"))

        self.catalog_list.append(CD("Your Life is Worth Living",155478049394,"Religion",[["Fulton J Sheen","artist"],["Robert Barron","artist"]]))

        self.catalog_list.append(CD("Computer Concepts and C Programming",209935753996,"Programming",[["Gupta Vikas","artist"]]))


    def search(self,filter,search_method):

        matching_process=Matching(self.catalog_list)
        search_method_choices={
            "Title": matching_process.match_by_title(filter),
            "Subject": matching_process.match_by_subject(filter),
            "Contributor": matching_process.match_by_contributors(filter)
        }

        try:
            matched_items=search_method_choices[search_method]
            if len(matched_items)==0:
                raise NotFoundError(filter)
            else:
                return matched_items  
        
        except KeyError:
            raise InvalidChoiceError(search_method)
            
    

    def display_queried_items(self,queried_items):
        queried_library_items_no=1
        for an_item in queried_items:
            total_contributors_of_the_item=an_item.get_contributors_of_the_item()
            print(f'{queried_library_items_no}) {an_item.type}: {an_item.title} by {total_contributors_of_the_item}')
            queried_library_items_no+=1
    
    def locate_an_item(self,queried_items,item_no):
        try:
            chosen_item=queried_items[item_no-1]
            item_location=chosen_item.locate()
            
            print(f'''
The library item is at this information:
Item Name: {chosen_item.title}

{item_location}''')
        
        except IndexError:
            raise InvalidChoiceError(item_no)
        
            


class CommandInterface:
    def __init__(self):
        self.catalog=Catalog()
        self.choices={
            "1": self.search_an_item,
            "2": self.display_all_items,
            "3": self.quit
        }
    
    def display_all_items(self):
        self.catalog.display_queried_items(self.catalog.catalog_list)

    def quit(self):
        raise SystemExit()

    def search_an_item(self):
        try:
            print('''
There are three ways to search an item on our library
Write "Subject" to search an item on a particular subject.
            
Write "Title" to search an item through its name.
            
Write "Contributor" to search an item associated with a contributor

''')
            keyword=input("Enter the keyword:")
            search_method=input("Enter the search method:")
            
            items_that_matched=self.catalog.search(keyword,search_method)
            self.catalog.display_queried_items(items_that_matched)
            print("\n")
            chosed_item=int(input("Enter the library item no to find it on Library shelf="))
            self.catalog.locate_an_item(items_that_matched,chosed_item)

        except InvalidChoiceError as e:
            print(e)

        except NotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
    
    def menu(self):
        try:
            answer = ""
            while True:
                print('''
--------------------------------------------------------------------
Welcome to the Demo University Online Library System.
This Online Library System will help you find your desired library items.
                         
Press 1 to search your desired library item.
                         
Press 2 to display all the library items.
                         
Press 3 to exit the library system

''')

                answer = input("enter a choice=")
                try:
                    func = self.choices[answer]
                except KeyError:
                    print("{} is not a valid option".format(answer))
                else:
                    func()
        finally:
            print("Thank you for visiting our online library")



CommandInterface().menu()

