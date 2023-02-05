from flask_app import app


import os
print(os.getcwd())
print(app)

def test_helloworld():

    # a = 1 + 3
    # c = a + 2
    hello = "hello"
    print(app)
    assert hello == "hello"
    
def test_helloworld2():
    hello = "hello"
    assert hello == "hello"



