<p align="center">
    <h1 align="center">Custom Language</h1>
</p>


---

##### Program starts with "PROGRAM" keyword followed by "ID"(program name) </p>

 ```javascript
    PROGRAM Part10 { } 
```

#### Variable declaration
```javascript
    var x, y : integer;
    var s    : real; 
    var c    : string;
    var f    : boolean;
```

##### Assignment statements 
```javascript
    x = 1 * 2 + 3 - 4 / 5 * (1 + 2)
    f = true;
    s = 1.5;
    c = "My language"
```

##### Boolean expressions
```python
    flag = True and False or !False and (True and False)
    flag = 1 < 2 and 2 > 1 
```

#### Function declaration 
```javascript
    function foo(s: STRING) {
        VAR c : STRING;
    }   
```

#### Builtin functions
```javascript
    function foo(s: STRING) {
        ... 
        print(s) 
    
        function bar() {
            return 2;
        }
        
        return bar(); 
    }   
    
    print(foo("bar")); // prints 2
```

#### Function call 
```javascript
    foo("Custom" + " " + "language");
```


#### If statement
```python
    x = 10 
    if x > 5 
    {
        print("x is greater than 5");
    }
    elif x < 5
    {
        print("x is less than 5")
    }
    else
    {
        print("x equals to 5")
    }

    if true or false
    {
        print("true")
    }
    
    if true and !false
    {
        print("true")
    }
```

#### Comments 
```
    // This is one line comment 
    
    {{
        This is multi-line comment
    }}
```

#### Program snippet
```javascript
    PROGRAM PartN11
        {
            VAR y : REAL;
                        
            function printSomething()
            {
                print(y)
            }
            
            y = 1.5 * 2 + 1;
            
            printSomething(); // "prints 4" 
        }
```

### Currently, language does not support many features, but it's in development process 
<br />
Language is made for learning purposes