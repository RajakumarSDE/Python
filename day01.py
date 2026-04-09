# this is a  5 type of input i get from a user here i getting input from multiple data types like (int , str , float)

firstname = str(input("Enter Your First Name : "))
lastname = str(input("Enter Your Last Name : "))
age = int(input("Enter Your Age : "))
salary = float(input("Enter Your LPA : "))
role = str(input("Enter your designation : "))

# here i will will the user data on the print message

print("hello", firstname, "below i will mention the data i will collect from you check them and if you want to change anything pleace contact the developer")
print("Your Full Name is ", firstname, lastname)
print("your current age is ", age)
print("your yearly package is ", salary)
print("You are a ", role)
print("kindly verify the all your data and let us know if there is any problem")
