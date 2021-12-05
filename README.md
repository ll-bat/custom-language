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
    VAR x, y : INTEGER;
    VAR s    : REAL; 
```

##### Assignment statements 
```javascript
    x = 1 * 2 + 3 - 4 / 5 * (1 + 2)
```

#### Function declaration 
```javascript
    function foo(s: STRING) {
        VAR c : STRING = s 
    }   
```

#### Builtin functions
```javascript
    function foo(s: STRING) {
        ... 
        print(s) 
    }   
```

#### Function call 
```javascript
    foo("Custom" + " " + "language");
```


#### Comments 
```
    {{ This is one line comment }}
    {{
        This is multi-line comment
    }}
```

#### Program snippet
```javascript
    PROGRAM Part10
        {
            VAR y : REAL;
                        
            function printSomething()
            {
                print(y)
            }
            
            y = 1.5 * 2 + 1;
            
            printSomething(); {{ "prints 4" }}
        }
```

### Currently, language does not support many features, but it's in development process 
<br />
Language is made for learning purposes