# Document-Automation-DSL

This repository contains the **Lexer**, **Parser** and the **Interpreter** of a DSL for **template processing**. Using this designed language, a user can create very custom template functions. The input to the function is a set of num, boolean, date, or text literals. The output of the template function is a **pdf** **document**.

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

### Multiple pdf template definitions will be concatenated 
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

### Introducing placeholders
The placeholder must be defined as a parameter variable in the begining of the template definition. It is further substituted with the template argument given on the time template function is called.

In this example, `#guess` is a variable placeholder and will be substituted on pdf generation.

``` test = {\courier Question 1: Is the 7-th fibonacci number \magenta #guess \?};```

### All the text decoration keywords:
Some such tags do not require a closing `\`, some do.

1. Text colors:

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

2. Text decorations:
* `\u text \` - underline
* `\i text \` - italic
* `\b text \`  - bold
* `\ibu text` \ or `(\bui  \uib \biu \iub \ubi)` - underline, italic, and bold
* `\ui text \` or `\iu text \`  - underline and italic
* `\bi text \` or  `\ib text \` -  italic and bold
* `\bu text \` or `\ub text\ ` - underline and bold

3. Font:
* `\courier`
* `\arial`
* `\helvetica`
* `\times`

4. Font size:
* `\100` - must be a valid uint

5. Special keywords:
* `\resetsize` - reset font size of text
* `\resetcolor` - reset color of text to black
* `\resetfont` - reset font
* `\line` - add an empty page line in template
* `\t` - a tab
* `\center text \` - align center a text
* `\left text \` - align to left of the page
* `\right text \` - align to right of the page

## Demo

#### Example program
```
create template LegalAgreement:
    params [
        initialMon, tax, finalMon, guess: num
        ans: bool
        mainText, test, answer, nameSeller, nameBuyer :text 
        dateWritten : date

]
    tax = 100*((tax/100)+(1/100));
    finalMon = initialMon + initialMon*(tax/100);

    mainText = { \20 \times \center Auto Bill of Sale \  \line 
    \16 \t I, 
\bu #nameSeller\, hereby sell, transfer and convey
\cred\b all\\resetcolor 
rights, title and interest in the following described vehicle to
\bu #nameBuyer\ 
for and in consideration of the total sum of 
\IU #initialMon $\
, inclusive of all sales tax \ibu ( #tax % ) \
, paid in the form of
\iu #finalMon $\, the receipt and sufficiency of which is hereby acknowledged.\line 
\12 *This sum represents the
\ib mutually\ agreed upon purchase price of the vehicle, between both
\cblue\i Seller\\resetcolor and the
\cgreen\ibu Purchaser\\resetcolor\.\\line \line \line
\16 Signature: \iu insert signature\
\13 \helvetica \right Date of issue: #dateWritten\\line};

    test = {\25 \times \brown Question 1:\ \resetcolor Is\courier the 7-th\resetfont fibonacci number\magenta #guess\?};
    initialMon = 0;
    finalMon = 1;
    tax = 0;
    
    do {
        tax = finalMon;
        finalMon = initialMon + finalMon;
        initialMon = tax;
        tax = 0;
    } until finalMon<8 ;

    if (finalMon == guess) {
        ans = "true";
        answer = {\cblue Answer: \u #ans\!\resetcolor};
    }else {
        ans = "false";
        answer = {\cred Answer: \u #ans\! It was #finalMon .\resetcolor};
    };

    print(mainText)

end template

actions:
    params[
        a: num
    ]

    a=5+7;
    if a!=100 {
        LegalAgreement(12500,15,0,8,"false","mainText", "test", "answer","Joe","Ben Parkins", "2022.05.31");
    }
```

#### Output:

![ast](https://github.com/EliriaT/Document_Automation_DSL/blob/main/ProgramExamples/demo.png)
