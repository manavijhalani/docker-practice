from flask import Flask
test=Flask(__name__)

@test.route('/')
def hi():
    return "{\"message\":\"Hey there python\"}"

if __name__=="__main__":
    test.run(host="0.0.0.0", port=int("3000"),debug=True)


