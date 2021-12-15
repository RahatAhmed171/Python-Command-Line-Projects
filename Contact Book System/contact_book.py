
from os import name


class InfoAlreadyExistsError(Exception):
    def __init__(self):
        print("Another contact exists with same information. Try Again")
        ContactMenu().quit()

class NotFoundError(Exception):
    def __init__(self):
        print(f'There is no name or number in contacts with given keyword')
        ContactMenu().quit()

class NoContactFieldError(Exception):
    def __init__(self):
        print("The required field you want to change doesn't exist in this contact")
        ContactMenu().quit()


''' 
To save your contacts in a file using this application,
create a txt file named "contact_file" in the same folder of this module

'''



class ContactMenu:

    def __init__(self):
        self.contactbook=ContactBook()
        self.matched_items=None
        self.a_contact=None
        self.contact_options={
            "E": self.edit_a_contact,
            "D": self.delete_a_contact,
            "Q": self.quit,
            "C": self.show_details_of_a_contact,
            "M": self.menu,
            "A": self.create_a_contact,
            "S": self.search_contacts
            }

    def menu(self):
        self.matched_items=None
        self.a_contact=None
        print('''
Press A to add a contact,
Press S to search contacts
Press Q to quit
        ''')
        
        func=self.choice_system(self.contact_options)
        func()
        

    def quit(self):
        raise SystemExit()
    
    def create_a_contact(self):
        number=input("Enter the number: ")
        name=input("Enter the name: ")
        print(''' 
Choose a category:
'F' for Family & Friends,
'B' for Business,
'R' for Random 
''')
        category_options={
            'F': "Family & Friends",
            'B': "Business",
            'R': "Random"
        }

        chosen_category=self.choice_system(category_options)
        
        try:
            contact_infos=[name,number,chosen_category]
            self.contactbook.create_a_contact(contact_infos)
        
        except InfoAlreadyExistsError as e:
            pass
        

    def search_contacts(self):
        query_word=input("Enter the name/number/category to find a contact: ")
        try:
            self.matched_items=self.contactbook.search_a_contact(query_word)
            
            print('''
Press C to show details of a contact,
Press M to return to main menu,
Press Q to quit
            ''')
            
            func=self.choice_system(self.contact_options)
            func()
        except NotFoundError as e:
            pass

            
    def show_details_of_a_contact(self):
        print(''' Select a contact no from the queried list to see its details''')
        a_contact=int(input("Enter the contact no to see its details: "))
        try:
            self.a_contact=self.matched_items[a_contact-1]
            self.contactbook.show_details_of_a_contact(self.a_contact)

            print('''
Press E to edit this contact
Press D to delete this contact
Press M to return to main menu
Press Q to exit''')
               
            func=self.choice_system(self.contact_options)
            func()
    
        except IndexError:
            print("The contact no you have entered does not exist")
            self.quit()
       
            
    def edit_a_contact(self):
        changeable_attributes={
            "NAME": 0,
            "NUMBER": 1,
        }
        print(''' 
Write 'Name' to edit the name of the contact
Write 'Number' to edit the number of the contact
        ''')
        chosen_attribute=self.choice_system(changeable_attributes)
        try:
            new_info=input(f'Enter the new info:')
            self.contactbook.edit_a_contact(self.a_contact,chosen_attribute,new_info)
        
        except InfoAlreadyExistsError as e:
            pass

        except NoContactFieldError as e:
            pass


    def delete_a_contact(self):
        self.contactbook.delete_a_contact(self.a_contact)

    
    def choice_system(self,choice_set):
        choice=input("Enter the choice: ").upper()
        try:
            result=choice_set[choice]
            return result
        except KeyError:
            print("{} is not a valid option".format(choice))
            self.quit()




class ContactBook:
    def __init__(self):
        self.contact_file=ContactStorage()
    
    def create_a_contact(self,contact_infos):

         for i in range (len(contact_infos)-1):
            is_an_info_duplicate=self.check_duplicate_info(contact_infos[i])
         
            if is_an_info_duplicate:
                
                raise InfoAlreadyExistsError()
            
         else:
            self.contact_file.add_a_contact_to_file(contact_infos)
            

    def search_a_contact(self,keyword):
        result_matched_items=self.contact_file.match_file_contents_with_keyword(keyword)
        if len(result_matched_items)==0:
            raise NotFoundError()
        else:
            self.sort_match_items(result_matched_items)
            return result_matched_items
    

    def sort_match_items(self,matched_items):
        matched_items.sort()
        item_counter=1
        for a_contact in matched_items:
            print(f'''
{item_counter}) Name : {a_contact[0]}
Phone : {a_contact[1]}
------------------------------------------
''')
            item_counter+=1
        
       
    def show_details_of_a_contact(self,a_contact):
        contact_fields=['Name',"Phone",'Category']
        length_of_a_contact=len(a_contact)
        for i in range(length_of_a_contact):
       
            print(f'''
{contact_fields[i]}: {a_contact[i]}
    ''')

    def edit_a_contact(self,the_contact,thing_to_change,the_word):
        is_it_duplicate=self.check_duplicate_info(the_word)
        if is_it_duplicate:
            raise InfoAlreadyExistsError()
        else:
            self.contact_file.edit_file_contents(the_contact,thing_to_change,the_word)

        
    def delete_a_contact(self,the_contact):
        self.contact_file.delete_file_contents(the_contact)
        print("Contact deleted successfully")

    
    def check_duplicate_info(self,word):
        result=self.contact_file.check_duplicate_words(word)
        return result


class ContactStorage:
    def __init__(self):
        self.file_location='contact_file.txt'
    

    def add_a_contact_to_file(self,contact_infos):
        with open(self.file_location,'r') as f:
            f_contents=f.read()
            if len(f_contents)==0:
                file_is_empty=True
            else:
                file_is_empty=False
                
            f.close()

            if file_is_empty:
                writing_mode='w'
                    
            else:
                writing_mode='a'

              
            f=open(self.file_location,writing_mode)
            f.writelines("%s\n" % i for i in contact_infos)    
            f.write("\n")
            f.close()
            print("Contact created sucessfully")
                
    
    def match_file_contents_with_keyword(self,keyword):
        with open(self.file_location,'r') as f:
          f_contents=f.readlines()
          info_of_a_person=[]
          matched_items=[]
          for items in f_contents:
              if items=='\n':
                  if str(keyword) in str(info_of_a_person):
                      matched_items.append(info_of_a_person)
                      info_of_a_person=[]  
                  else:
                     info_of_a_person=[]
              
              else:
                 info_of_a_person.append(items)
              
          f.close()
          
          return matched_items

          
          

    def edit_file_contents(self,the_contact,things_to_change,the_word):
            try:
                with open(self.file_location,'r') as f:
                    details=f.read()
                with open(self.file_location,'w') as f:
                    f.write(details.replace(str(the_contact[things_to_change]),str(the_word)+"\n"))
                    
                print("Contact Edited Succesfully") 
                f.close()
            except IndexError:
                raise NoContactFieldError()
            

    def delete_file_contents(self,the_contact):
        the_length_of_the_contact=len(the_contact)
        for things_to_change in range(the_length_of_the_contact):
            with open(self.file_location,'r') as f:
              details=f.read()
            with open(self.file_location,'w') as f:
              f.write(details.replace(str(the_contact[things_to_change]),str("#####")+"\n"))
            
        f.close()

    
    def check_duplicate_words(self,the_info):
         the_actual_word=the_info+'\n'
         with open(self.file_location,'r') as f:
          f_contents=f.readlines()
        
          for items in f_contents:
              if the_actual_word==items:
                  
                  return True
          else:
              return False
    


ContactMenu().menu()
        
        




            

       




    
    













