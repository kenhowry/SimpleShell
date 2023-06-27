"""
Simple Shell (File System Tree)
Implementation of a simple terminal program

File Name: howry_simple_shell.py
Author: Ken Howry
Date: 2.6.23
Course: COMP 1353
Assignment: Project V
Collaborators: N/A
Internet Source: N/A
"""
#imports
import pickle

class TreeNode:
    #class variable assignment
    children = []

    def __init__(self, name, parent, is_directory):
        """
            Description:
                initializes a new TreeNode Object
            Parameters:
                name: name of the node
                parent: the parent of the node
                value: the value for is_directory
            Return:
                None
        """
        self.name = name
        self.parent = parent
        self.is_directory = is_directory

        #setting the to either a list or None
        if self.is_directory:
            self.children = []
        else:
            self.children = None

    def __str__(self):
        """
            Description:
                returns a string representation of TreeNode
            Parameters:
                None
            Return:
                str
        """
        #indicating if the node is a directory or not
        if self.is_directory == True:
            return f"{str(self.name)} <directory>"
        else:
            return str(self.name)

    def append_child(self, name, is_directory):
        """
            Description:
                appends a TreeNode object to self.children
            Parameters:
                name: name of the child
                is_directory: bool; directory status of the child 
            Return:
        """
        if self.is_directory == True:
            self.children.append(TreeNode(name, self, is_directory))
        else:
            raise ValueError(f"{name} is not a directory")

    def is_root(self):
        """
            Description:
                return True if the is the root, False otherwise
            Parameters:
                None
            Return:
                bool
        """
        return self.parent is None

    def path(self):
        """
            Description:
                returns the ancestors of the node using recursion
            Parameters:
                None
            Return:
                str
        """
        if self.parent is None:
            return f"/{self.name}/"
        else:
            return self.parent.path() + self.name + "/"

class FileSystem:
    def __init__(self):
        """
            Description:
                initializes the filesystem
            Parameters:
                None
            Return:
                None
        """
        self.root = TreeNode("", None, True)
        self.current_directory = self.root

    def check_make_file(self, name):
        """
            Description:
                checks if the name exists in the current directory
            Parameters:
                name: name of the file to check
            Return:
                None
        """
        for child in self.current_directory.children:
            if child.name == name:
                raise ValueError("Name already exists in current directory.")

    def ls(self):
        """
            Description:
                prints all the children of the current directory
            Parameters:
                None
            Return:
                None
        """
        for child in self.current_directory.children:
            print(child)

    def mkdir(self, dirname):
        """
            Description:
                adds a new directory child node to the current directory
            Parameters:
                dirname: the name of the new directory
            Return:
                None
        """
        #checking if the name exists in the current directory
        self.check_make_file(dirname)

        #appending the directory
        self.current_directory.append_child(dirname, True)

    def touch(self, name):
        """
            Description:
                adds a new file child node to the current directory
            Parameters:
                name: the name of the new file
            Return:
                None
        """
        #checking if the name exists in the current directory        
        self.check_make_file(name)

        #appending the file
        self.current_directory.append_child(name, False)

    def cd(self, name):
        """
            Description:
            Parameters:
            Return:
        """    
        #special handling for ..
        if name == "..":
            if not self.current_directory.is_root():
                self.current_directory = self.current_directory.parent
        else:
            #variable assignment
            #determines if the directory has been found
            found = False

            #iterating through the children of the current directory
            for child in self.current_directory.children:
                if child.name == name and child.is_directory:
                    self.current_directory = child
                    found = True
                    break
                    
            #raise ValueError if the directory cannot be found
            if not found:
                raise ValueError(f"Directory '{name}' cannot be found.")

    def rm(self, filename):
        """
            Description:
                removes the file, filename
            Parameters:
                filename: the name of the file to be removed
            Return:
                None
        """
        #variable assignment
        #determines if the file has been found
        found = False

        #iterating through current_directory.children
        for child in self.current_directory.children:
            if child.name == filename:
                if child.is_directory:
                    raise ValueError(f"{filename} is a directory.")
                self.current_directory.children.remove(child)
                found = True
                break
        
        #raise ValueError if the file does not exist
        if not found:
            raise ValueError(f"File '{filename}' not found.")

    def rmdir(self, dirname):
        """
            Description:
                removes the directory, dirname
            Parameters:
                dirname: name of the directory
            Return:
                None
        """ 
        #variable assignment
        #determines if the directory has been found
        found = False

        #iterating through current_directory.children
        for child in self.current_directory.children:
            if child.name == dirname:
                if not child.is_directory:
                    raise ValueError(f"{dirname} is not a directory.")
                if child.children != []:
                    raise ValueError(f"{dirname} is not empty.")
                self.current_directory.children.remove(child)
                found = True
                break
        
        #raising ValueError if the directory does not exist
        if not found:
            raise ValueError(f"Directory '{dirname}' not found.")
    
    def pwd(self):
        """
            Description:
                returns the full path name of the current directory starting with root
            Parameters:
                None
            Return:
                str
        """
        return self.current_directory.path()
    
    def tree_helper(self, directory, level):
        """
            Description:
                recursively prints the current directory tree
                -preorder output
                -recursive function
            Parameters:
                directory: TreeNode object
                    -the root node of the tree
                level: integer
            Return:
                None
        """
        print(level * "  " + str(directory.name))

        #printing the children
        if directory.children:
            for child in directory.children:
                self.tree_helper(child, level + 1)

    def tree(self):
        """
        Description:
            returns the string representation of the tree
        Parameters:
            None
        Return:
            None
        """
        self.tree_helper(self.current_directory, 0)

def __main__():
    #checking is there is a file system
    #if not, creating a new one
    try:
        with open("file_system.bin", "rb") as file_source:
            file_system = pickle.load(file_source)
            print("File System loaded")
    except:
        print("Creating a new file system: file doesn't exist or data file is out of date because FileSystem class changed")
        file_system = FileSystem()

    quit_program = False

    #taking user-input and responding appropriately
    while not quit_program:
        user_input = input("").lower()

        if user_input == "cd":
            dirname = input("Enter directory name: ")
            file_system.cd(dirname)

        elif user_input == "ls":
            file_system.ls()
        
        elif user_input == "touch":
            filename = input("Enter file name: ")
            file_system.touch(filename)
        
        elif user_input == "mkdir":
            dirname = input("Enter directory name: ")
            file_system.mkdir(dirname)
        
        elif user_input == "pwd":
            print(file_system.pwd())
        
        elif user_input == "rm":
            filename = input("Enter file name: ")
            file_system.rm(filename)
        
        elif user_input == "rmdir":
            dirname = input("Enter directory name: ")
            file_system.rmdir(dirname)
        
        elif user_input == "tree":
            return file_system.tree()
        
        elif user_input == "quit":
            quit_program = True
        
        else:
            print("Invalid command")

    #saving the file system
    with open("file_system.bin", "wb") as file_destination:
        pickle.dump(file_system, file_destination)
        print("File system saved")

if __name__ == "__main__":
    __main__()