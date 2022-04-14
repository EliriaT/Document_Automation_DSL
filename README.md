# Document-Automation-DSL

## Introduction

A domain-specific language (DSL) is a specific programming language that has higher abstraction level and is specifically optimisеd for a specific field of problems. Domain-specific languages support a narrow set of tasks in a chosen domain.  This DSL for Document Automation allows conditional text as well as vаriable text, and manipulation of data commonly contained within a map of documents. The user can create **template functions** which will represent the general draft of the document. Inside the template function, the user can set the parameters that must be submitted to the template. These submitted parameter will be replaced at the marked place in the provided text. Furthermore, it is possible to have conditional text, error messages, and loops. Another feature which was considered important for this DSL, is the ability of the language to position text, and to adjust text design.

## Input
This DSL has the following types of inputs: plain text files(.txt, .doc,.docx), PDF files and CSV files(or XLSX).
**Plain text files(.txt, .doc,.docx, .pdf)** - will be used for creating a template from already an existing document. This is the case when the internal template parameters should be marked with the ‘#’ symbol in the readily made input document file. This is a fast method for creating templates and easier to understood by people who do not possess all the technical skills for understanding the DSL’s syntax.
**CSV files (or XLSX)** - the spreadsheets can be used as input data for templates. For example a user has a spreadsheet full of data of ten people and he wants to create contracts for them. He can use this data as input to the template function. As a result ten contracts will be generated filled with the data from the spreadsheet.
**Command line inputs** - command line inputs can be used to manually fill in data of a template. It can be used for testing purposes, to check input/output connection, to avoid exporting PDF for wrong input. It offers more of a command line application for users to submit data to the template functions.

## Output
The program can produce two types of outputs:
**Command line output** - in command line output the error information is shown and it is loged the status of a running program in case it has errors.
**PDF/Docs**  - the DSL’s main type of output is a PDF file or a Docs file. The user can create user-made templates to later use that template to produce a PDF file that is filled with data and is ready for export.

