# Importing random to generate
# random string sequence
import random

# Importing string library function
import string

def rand_pass(size, scope = string.ascii_letters + string.digits):

    # Takes random choices from ascii_letters and digits
    generate_pass = ''.join([random.choice(scope)
                             for n in range(size)])

    return generate_pass

# Driver Code

x = int(input("Enter number of pins you want:"))

for i in range(x):
    print(rand_pass(10, 'Geeks3F0rgeeKs'))
