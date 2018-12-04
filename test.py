catdog = {
    'cat1' : ['dog1', 'dog2', 'dog3'],
    'cat2' : ['dog4', 'dog5', 'dog6'],
    'cat3' : ['dog7', 'dog8', 'dog9'],
    'cat4': ['dog10', 'dog11', 'dog12']
}

for cats, dogs in catdog.items():
    print("cats and dogs", cats, dogs)
    for dog in dogs:
        print("woof!", dog) 

if "cat4" not in catdog:
    catdog["cat4"] = ['dog10', 'dog11', 'dog12']
    print(catdog)
elif "cat4" in catdog:
    arr = catdog.get('cat4')
    arr.append('dog13')
    catdog["cat4"] = arr
    print("dog13 added", catdog)
else:
    print("This shoudln't happen!")