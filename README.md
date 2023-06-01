# Document-Automation-DSL

This repository contains the Lexer, Parser and the Interpreter of a DSL for **template processing**. Using this designed language, a user can create very custom template functions. The input to the function is a set of num, boolean, date, or text literals. The output of the template function is a pdf document.

## Introduction

A domain-specific language (DSL) is a specific programming language that is optimisеd for a specific field of problems. Domain-specific languages support a narrow set of tasks in a chosen domain.  

This DSL for **Document Automation** allows for:
* defining variables
* evaluating expresions
* defining template functions
* text replacement
* loops -  while loop, do while loop.
* conditional evaluation
* flexible text styling:
  1. Setting the color of a subtext
  2. Setting the font of a subtext
  3. Setting the font-size of subtext
  4. Setting the text-decoration of a subtext
  5. Aligning the text


The user can create **template functions** which will represent the general draft of the document. 

Inside the template function, the user can set the parameters that must be submitted to the template. 

These submitted parameters will be replaced at the marked place in the provided text.

All the text defined inside `{ styled text with #parameters }` will be included in the final output pdf.

## How to Use this DSL

### The main entry point

Each template function must have the following similar structure:
```
create template MotivateAbsence:
    params [
        test :text
        mon : num
]
    
    test = {\green  Hello\ \line  World! };
    if(mon>16) print(mon);

end template

actions:
    MotivateAbsence("",19);
```

Each program must have a template function definition and the main entry point of the program.

The main entry point in the program is under the `actions:` block of code. 

### The template function 
 To define a template function

```
create template NameOfTemplate:
// a list of params in the form of 
// IDENTIFIER : TYPE

    params [
        test: text
        mon: num
    ]

// template body

end template
```
### To call the template function in the main entry point
```
actions:
    MotivateAbsence("",19);
```

### Simple variables and expressions

```
create template NameOfTemplate:
    params [
        initialMon, finalMon:  num
 
    ]

// template body
  tax = 100*((tax/100)+(1/100));
  finalMon = initialMon + initialMon*(tax/100);
end template

actions:
   NameOfTemplate(50,100);
```

### Until loop
```
  until (mon<20)
    {
        mon = mon+1;
        print(mon);
    };
 ```
 
 ### Do Until loop
```
   do {
        tax = finalMon;
        finalMon = initialMon + finalMon;
        initialMon = tax;
        tax = 0;
    } until finalMon<8 ;
 ```
### If Else
```
if(mon>16) print(mon);
   else  print ("Less than 16");
```
### Constructing the template pdf
```
test = {  Hello Word };
```

### Multiple definitions will be concatenated 
```
test = {  Hello Word };
test = {  Wish you a sunny day };
```

### Adding color
```
   test = {\green Hello! };
```

### Setting the font globally
```
   test = {\courier Hello!  };
```

### Resetting the font 
```
   test = {\courier Hello! \resetfont world!  };
```

### Setting the font size
```
   test = {\50 Hello!  world!  };
```

### Text decoration 
Bold and underline: 
```
   test = {\bu Hello!  world!  };
```
### Print in terminal something
This is allowed for now only in template definition
```print(expression);```

### All the text decoration keywords:
Some such tags do not require a closing `\`, some do.

Text colors:

* `\red  text \`
* `\blue  text \`
* `\green text \`
* `\magenta text \`
* `\white text \`
* `\yellow text \`
* `\brown text \`
* `\grey text \`
* `\black text \`

Prefix the text color with `c`, to set the global text color. Example: `\cred`

Text decorations:
* `\u text \` - underline
* `\i text \` - italic
* `\b text \`  - bold
* `\ibu text` \ or `(\bui  \uib \biu \iub \ubi)` - underline, italic, and bold
* `\ui text \` or `\iu text \`  - underline and italic
* `\bi text \` or  `\ib text \` -  italic and bold
* `\bu text \` or `\ub text\ ` - underline and bold

Font:
* \courier
* \arial
* \helvetica
* \times

Font size:
* \1-100 - a valid uint

Special keywords:
* \resetsize - reset font size of text
* \resetcolor - reset color of text to black
* \resetfont - reset font
* \line - add an empty page line in template
* \t - a tab
* \center text \ - align center a text
* \left text \ - align to left of the page
* \right text \ - align to right of the page
